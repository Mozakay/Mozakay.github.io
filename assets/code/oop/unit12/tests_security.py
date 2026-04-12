from __future__ import annotations
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import security_layer as _security_layer_bootstrap


def _normalize_datetime_bootstrap(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _format_datetime_bootstrap(value: datetime) -> str:
    return _normalize_datetime_bootstrap(value, "value").isoformat()


if not hasattr(_security_layer_bootstrap, "_normalize_datetime"):
    _security_layer_bootstrap._normalize_datetime = _normalize_datetime_bootstrap

if not hasattr(_security_layer_bootstrap, "_format_datetime"):
    _security_layer_bootstrap._format_datetime = _format_datetime_bootstrap


from core_banking import BankAccount, InsufficientFundsError
from security_layer import (
    # Auth / users / sessions
    IClock,
    User,
    BasicPasswordPolicy,
    PBKDF2PasswordHasher,
    CredentialService,
    InMemoryUserStore,
    BoundedAuthEventLogger,
    AuthSessionCoordinator,
    LoginAttemptPolicy,
    SessionManager,
    AuthServiceFactory,
    AuthenticationError,
    AccountLockedError,
    AuthAction,
    AuthStatus,
    AuthEvent,
    # Authorization
    AuthorizationPolicy,
    ROLE_OWNER,
    ROLE_AUDITOR,
    AuthorizationError,
    # Security events / monitoring
    AlertObserver,
    SecurityAction,
    EventStatus,
    Severity,
    EventAmount,
    SecurityEvent,
    # Fraud
    FraudDetectionEngine,
    LargeAmountRule,
    RapidOutgoingTransactionRule,
    BalanceRatioRule,
    UnusualHourRule,
    FraudAlertError,
    TransactionContext,
    TransactionMonitor,
    # Rate limiting
    RateLimiterFactory,
    LimiterType,
    StrictWindowConfig,
    TokenBucketConfig,
    TokenBucketCreator,
    StrictWindowCreator,
    RateLimitExceededError,
    # Services / pipeline
    SecurityEventFactory,
    SecurityOperationPipelineFactory,
    InMemoryObserverFailureSink,
    PERM_DEPOSIT,
    PERM_WITHDRAW,
    PERM_TRANSFER,
)

from secure_banking_services import (
    AuditLoggerFactory,
    AccountSecurityRegistry,
    SecureAccountOperationService,
    SecureTransferService,
    BasicTransferValidationPolicy,
    SecurityConfig,
    SecureBankingServiceFactory,
)

from security_reporting import (
    ThreatReportBuilder,
    ThreatReportGenerator,
    SystemReportAssembler,
)


class TestClock(IClock):
    def __init__(
        self,
        start_dt: datetime | None = None,
        start_monotonic: float = 0.0,
    ) -> None:
        self._now = start_dt or datetime(2026, 4, 4, 12, 0, 0, tzinfo=timezone.utc)
        self._monotonic = float(start_monotonic)

    def monotonic(self) -> float:
        return self._monotonic

    def now(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        self._monotonic += float(seconds)
        self._now = self._now + timedelta(seconds=float(seconds))


class PrettyPrintTestCase(unittest.TestCase):
    LABEL_WIDTH = 24

    def print_summary(self, title: str, rows: list[tuple[str, object]]) -> None:
        print(f"\n--- {title} ---")
        for label, value in rows:
            print(f"{label:<{self.LABEL_WIDTH}}: {value}")

@dataclass(frozen=True, slots=True)
class OperationTestContext:
    clock: TestClock
    auth_service: object
    authorization_policy: AuthorizationPolicy
    registry: AccountSecurityRegistry
    alert_monitor: AlertObserver
    transaction_monitor: TransactionMonitor
    rate_limiter: object
    fraud_engine: FraudDetectionEngine
    event_factory: SecurityEventFactory
    account_ops: SecureAccountOperationService
    transfer_service: SecureTransferService
    auth_session: object

# =============================================================================
# Shared builders
# =============================================================================


def build_auth_service(
    *,
    clock: TestClock | None = None,
    max_attempts: int = 3,
    lockout_seconds: float = 30.0,
    session_timeout_seconds: float = 300.0,
    authorized_account_reader=None,
):
    clock = clock or TestClock()
    user_store = InMemoryUserStore()
    credential_service = CredentialService(
        hasher=PBKDF2PasswordHasher(),
        password_policy=BasicPasswordPolicy(),
    )
    auth_event_journal = BoundedAuthEventLogger()
    session_manager = SessionManager(
        session_timeout_seconds=session_timeout_seconds,
        clock=clock,
    )
    session_coordinator = AuthSessionCoordinator(session_manager)
    login_attempt_policy = LoginAttemptPolicy(
        max_attempts=max_attempts,
        lockout_seconds=lockout_seconds,
        clock=clock,
    )

    auth_service = AuthServiceFactory.from_legacy_dependencies(
        user_store=user_store,
        login_attempt_policy=login_attempt_policy,
        credential_service=credential_service,
        session_coordinator=session_coordinator,
        auth_event_journal=auth_event_journal,
        clock=clock,
        authorized_account_reader=authorized_account_reader,
    )
    return auth_service, clock, user_store, auth_event_journal



def build_operation_services(
    *,
    clock: TestClock | None = None,
    strict_window_limit: int = 10,
    strict_window_seconds: float = 60.0,
    fraud_rules=None,
):
    clock = clock or TestClock()

    auth_service, _, _, _ = build_auth_service(clock=clock)
    auth_service.register_user("sarah", "StrongPass1")

    authorization_policy = AuthorizationPolicy()
    authorization_policy.grant_access("sarah", 1001, ROLE_OWNER)
    authorization_policy.grant_access("sarah", 1002, ROLE_OWNER)

    accounts = [
        BankAccount(1001, 1000.0),
        BankAccount(1002, 500.0),
    ]

    alert_monitor = AlertObserver()
    audit_logger_factory = AuditLoggerFactory(clock=clock)

    registry = AccountSecurityRegistry(
        accounts=accounts,
        audit_logger_factory=audit_logger_factory,
        log_enabled=True,
    )
    registry.add_global_observer(alert_monitor)

    rate_limiter = RateLimiterFactory(
        creators={
            LimiterType.TOKEN_BUCKET: TokenBucketCreator(clock),
            LimiterType.STRICT_WINDOW: StrictWindowCreator(clock),
        }
    ).create(
        LimiterType.STRICT_WINDOW,
        StrictWindowConfig(
            max_requests=strict_window_limit,
            window_seconds=strict_window_seconds,
        ),
    )

    transaction_monitor = TransactionMonitor(clock=clock)
    if fraud_rules is None:
        fraud_rules = [
            LargeAmountRule(threshold=5000.0),
            RapidOutgoingTransactionRule(max_recent_actions=5),
            BalanceRatioRule(max_ratio=0.95),
            UnusualHourRule(allowed_start_hour=0, allowed_end_hour=24),
        ]
    fraud_engine = FraudDetectionEngine(fraud_rules)

    event_factory = SecurityEventFactory(clock)
    pipeline = SecurityOperationPipelineFactory.from_legacy_dependencies(
        authenticator=auth_service,
        authorization_policy=authorization_policy,
        fraud_engine=fraud_engine,
        rate_limiter=rate_limiter,
        transaction_monitor=transaction_monitor,
        clock=clock,
        event_factory=event_factory,
    )

    account_ops = SecureAccountOperationService(
        pipeline=pipeline,
        registry=registry,
        transaction_monitor=transaction_monitor,
        event_factory=event_factory,
    )
    transfer_service = SecureTransferService(
        pipeline=pipeline,
        registry=registry,
        transaction_monitor=transaction_monitor,
        transfer_authorization_policy=BasicTransferValidationPolicy(),
        event_factory=event_factory,
    )

    auth_session = auth_service.authenticate_session("sarah", "StrongPass1")
    return OperationTestContext(
        clock=clock,
        auth_service=auth_service,
        authorization_policy=authorization_policy,
        registry=registry,
        alert_monitor=alert_monitor,
        transaction_monitor=transaction_monitor,
        rate_limiter=rate_limiter,
        fraud_engine=fraud_engine,
        event_factory=event_factory,
        account_ops=account_ops,
        transfer_service=transfer_service,
        auth_session=auth_session,
    )


# =============================================================================
# Authentication tests
# =============================================================================


class Test01Authentication(PrettyPrintTestCase):
    def test_01_login_succeeds_with_correct_password(self):
        auth_service, _, user_store, event_journal = build_auth_service()

        user = auth_service.register_user("Sarah", "StrongPass1")
        self.assertIsInstance(user, User)
        self.assertTrue(user_store.contains("sarah"))

        auth_session = auth_service.authenticate_session("Sarah", "StrongPass1")
        self.assertEqual(auth_session.user.username, "sarah")
        self.assertTrue(auth_service.is_authenticated_session(auth_session))
        self.assertTrue(auth_service.is_authenticated_user(auth_session.user))

        events = event_journal.get_auth_events()
        self.assertGreaterEqual(len(events), 1)
        self.assertEqual(events[-1].action, AuthAction.LOGIN)
        self.assertEqual(events[-1].status, AuthStatus.PASS)

        self.print_summary(
            "Test 01 Summary (Login Success)",
            [
                ("Username", auth_session.user.username),
                ("User stored", user_store.contains("sarah")),
                ("Last auth action", events[-1].action.value),
                ("Last auth status", events[-1].status.value),
                ("Result", "PASS"),
            ],
        )

    def test_02_login_fails_with_wrong_password(self):
        auth_service, _, _, _ = build_auth_service()
        auth_service.register_user("bob", "BobPass123")

        with self.assertRaises(AuthenticationError):
            auth_service.authenticate_session("bob", "WrongPassword1")

        self.assertEqual(auth_service.failed_attempts("bob"), 1)

        self.print_summary(
            "Test 02 Summary (Wrong Password)",
            [
                ("Username", "bob"),
                ("Expected", "AuthenticationError"),
                ("Failed attempts", auth_service.failed_attempts("bob")),
                ("Result", "PASS"),
            ],
        )

    def test_03_account_locks_after_max_failed_attempts(self):
        auth_service, _, _, event_journal = build_auth_service(
            max_attempts=3,
            lockout_seconds=60.0,
        )
        auth_service.register_user("carol", "CarolPass1")

        for _ in range(2):
            with self.assertRaises(AuthenticationError):
                auth_service.authenticate_session("carol", "WrongPass1")

        with self.assertRaises(AccountLockedError):
            auth_service.authenticate_session("carol", "WrongPass1")

        self.assertTrue(auth_service.is_locked("carol"))
        self.assertEqual(auth_service.failed_attempts("carol"), 3)
        self.assertTrue(any(e.action == AuthAction.LOCKOUT for e in event_journal.get_auth_events()))

        self.print_summary(
            "Test 03 Summary (Account Lockout)",
            [
                ("Username", "carol"),
                ("Max attempts", 3),
                ("Locked", auth_service.is_locked("carol")),
                ("Failed attempts", auth_service.failed_attempts("carol")),
                ("Lockout event", any(e.action == AuthAction.LOCKOUT for e in event_journal.get_auth_events())),
                ("Result", "PASS"),
            ],
        )

    def test_04_locked_account_rejects_correct_password(self):
        auth_service, _, _, _ = build_auth_service(
            max_attempts=2,
            lockout_seconds=120.0,
        )
        auth_service.register_user("dave", "DavePass1")

        for _ in range(2):
            try:
                auth_service.authenticate_session("dave", "WrongPass1")
            except (AuthenticationError, AccountLockedError):
                pass

        with self.assertRaises(AccountLockedError):
            auth_service.authenticate_session("dave", "DavePass1")

        self.print_summary(
            "Test 04 Summary (Locked Account Rejects Correct Password)",
            [
                ("Username", "dave"),
                ("Expected", "AccountLockedError"),
                ("Locked", auth_service.is_locked("dave")),
                ("Result", "PASS"),
            ],
        )

    def test_05_session_expires_after_timeout(self):
        auth_service, clock, _, _ = build_auth_service(session_timeout_seconds=5.0)
        auth_service.register_user("emma", "EmmaPass1")
        auth_session = auth_service.authenticate_session("emma", "EmmaPass1")

        self.assertTrue(auth_service.is_authenticated_session(auth_session))
        clock.advance(6.0)
        self.assertFalse(auth_service.is_authenticated_session(auth_session))

        self.print_summary(
            "Test 05 Summary (Session Expiry)",
            [
                ("Username", "emma"),
                ("Timeout seconds", 5.0),
                ("Advanced by", 6.0),
                ("Session active", auth_service.is_authenticated_session(auth_session)),
                ("Result", "PASS"),
            ],
        )


# =============================================================================
# Authorization tests
# =============================================================================


class Test02Authorization(PrettyPrintTestCase):
    def test_06_auditor_cannot_withdraw(self):
        stack = build_operation_services()
        stack.auth_service.register_user("eve", "EveAudit1")
        stack.authorization_policy.grant_access("eve", 1001, ROLE_AUDITOR)
        auditor_session = stack.auth_service.authenticate_session("eve", "EveAudit1")

        with self.assertRaises(AuthorizationError):
            stack.account_ops.withdraw(auditor_session, 1001, 50.0)

        self.print_summary(
            "Test 06 Summary (Auditor Cannot Withdraw)",
            [
                ("Username", "eve"),
                ("Role", ROLE_AUDITOR.name),
                ("Account", 1001),
                ("Action", "withdraw"),
                ("Expected", "AuthorizationError"),
                ("Result", "PASS"),
            ],
        )

    def test_07_auditor_cannot_deposit(self):
        stack = build_operation_services()
        stack.auth_service.register_user("frank", "FrankAudit1")
        stack.authorization_policy.grant_access("frank", 1001, ROLE_AUDITOR)
        auditor_session = stack.auth_service.authenticate_session("frank", "FrankAudit1")

        with self.assertRaises(AuthorizationError):
            stack.account_ops.deposit(auditor_session, 1001, 20.0)

        self.print_summary(
            "Test 07 Summary (Auditor Cannot Deposit)",
            [
                ("Username", "frank"),
                ("Role", ROLE_AUDITOR.name),
                ("Account", 1001),
                ("Action", "deposit"),
                ("Expected", "AuthorizationError"),
                ("Result", "PASS"),
            ],
        )

    def test_08_owner_can_transfer_between_accounts(self):
        stack = build_operation_services()
        auth_session = stack.auth_session

        source_balance, destination_balance = stack.transfer_service.transfer(
            auth_session,
            1001,
            1002,
            100.0,
        )

        self.assertEqual(source_balance, 900.0)
        self.assertEqual(destination_balance, 600.0)

        self.print_summary(
            "Test 08 Summary (Owner Transfer)",
            [
                ("Username", auth_session.user.username),
                ("From account", 1001),
                ("To account", 1002),
                ("Transfer amount", 100.0),
                ("Source balance", source_balance),
                ("Destination balance", destination_balance),
                ("Result", "PASS"),
            ],
        )


# =============================================================================
# Fraud detection tests
# =============================================================================


class Test03FraudDetection(PrettyPrintTestCase):
    def test_09_large_transaction_blocked_by_fraud_rule(self):
        clock = TestClock()
        stack = build_operation_services(
            clock=clock,
            fraud_rules=[LargeAmountRule(threshold=100.0)],
        )

        with self.assertRaises(FraudAlertError):
            stack.account_ops.withdraw(stack.auth_session, 1001, 200.0)

        self.assertEqual(stack.registry.get_account(1001).get_balance(), 1000.0)

        self.print_summary(
            "Test 09 Summary (Large Transaction Blocked)",
            [
                ("Username", stack.auth_session.user.username),
                ("Account", 1001),
                ("Fraud threshold", 100.0),
                ("Attempted amount", 200.0),
                ("Balance unchanged", stack.registry.get_account(1001).get_balance()),
                ("Result", "PASS"),
            ],
        )

    def test_10_fraud_alert_observer_notified_on_suspicious_transaction(self):
        clock = TestClock()
        stack = build_operation_services(
            clock=clock,
            fraud_rules=[LargeAmountRule(threshold=100.0)],
        )

        with self.assertRaises(FraudAlertError):
            stack.transfer_service.transfer(stack.auth_session, 1001, 1002, 200.0)

        self.assertGreater(stack.alert_monitor.alert_count(), 0)
        fraud_alerts = [
            e for e in stack.alert_monitor.get_alerts()
            if e.action == SecurityAction.FRAUD_DETECTED
        ]
        self.assertGreater(len(fraud_alerts), 0)
        self.assertEqual(fraud_alerts[0].severity, Severity.CRITICAL)
        self.assertEqual(fraud_alerts[0].username, "sarah")

        self.print_summary(
            "Test 10 Summary (Fraud Alert Observer)",
            [
                ("Username", fraud_alerts[0].username),
                ("Action", fraud_alerts[0].action.value),
                ("Severity", fraud_alerts[0].severity.value),
                ("Alert count", stack.alert_monitor.alert_count()),
                ("Result", "PASS"),
            ],
        )

    def test_11_unusual_hour_transaction_flagged(self):
        engine = FraudDetectionEngine([UnusualHourRule(allowed_start_hour=7, allowed_end_hour=22)])
        context = TransactionContext(
            username="judy",
            account_number=1,
            action=PERM_WITHDRAW,
            current_balance=10_000.0,
            amount=100.0,
            recent_action_count=0,
            hour_of_day=3,
        )

        triggered = engine.check(context)
        self.assertTrue(len(triggered) > 0)
        self.assertTrue(any("allowed hours" in desc for desc in triggered))

        self.print_summary(
            "Test 11 Summary (Unusual Hour Transaction)",
            [
                ("Username", "judy"),
                ("Hour of day", 3),
                ("Allowed window", "07:00-22:00"),
                ("Triggered rules", "; ".join(triggered)),
                ("Result", "PASS"),
            ],
        )

    def test_12_balance_ratio_exceeded_blocks_transfer(self):
        clock = TestClock()
        stack = build_operation_services(
            clock=clock,
            fraud_rules=[BalanceRatioRule(max_ratio=0.5)],
        )

        with self.assertRaises(FraudAlertError):
            stack.transfer_service.transfer(stack.auth_session, 1001, 1002, 900.0)

        self.assertEqual(stack.registry.get_account(1001).get_balance(), 1000.0)
        self.assertEqual(stack.registry.get_account(1002).get_balance(), 500.0)
        self.print_summary(
            "Test 12 Summary (Balance Ratio Blocked)",
            [
                ("Username", stack.auth_session.user.username),
                ("Account", 1001),
                ("Max ratio", 0.5),
                ("Attempted amount", 900.0),
                ("Source balance", stack.registry.get_account(1001).get_balance()),
                ("Destination balance", stack.registry.get_account(1002).get_balance()),
                ("Result", "PASS"),
            ],
        )


# =============================================================================
# Audit trail and reporting tests
# =============================================================================


class Test04AuditTrailAndReporting(PrettyPrintTestCase):
    def test_13_audit_event_recorded_on_failed_access(self):
        stack = build_operation_services()
        stack.auth_service.register_user("leo", "LeoPass123")
        stranger_session = stack.auth_service.authenticate_session("leo", "LeoPass123")

        with self.assertRaises(AuthorizationError):
            stack.account_ops.deposit(stranger_session, 1001, 100.0)

        events = stack.registry.get_logger(1001).get_events()
        denied = [e for e in events if e.action == SecurityAction.ACCESS_DENIED]
        self.assertGreater(len(denied), 0)
        self.assertEqual(denied[0].username, "leo")
        self.assertEqual(denied[0].severity, Severity.WARNING)
        self.assertEqual(denied[0].status, EventStatus.DENIED)

        self.print_summary(
            "Test 13 Summary (Failed Access Audit Event)",
            [
                ("Username", denied[0].username),
                ("Action", denied[0].action.value),
                ("Severity", denied[0].severity.value),
                ("Status", denied[0].status.value),
                ("Result", "PASS"),
            ],
        )

    def test_14_successful_deposit_produces_pass_audit_event(self):
        stack = build_operation_services()

        stack.account_ops.deposit(stack.auth_session, 1001, 50.0)

        events = stack.registry.get_logger(1001).get_events()
        deposit_pass = [
            e for e in events
            if e.action == SecurityAction.DEPOSIT and e.status == EventStatus.PASS
        ]
        self.assertGreater(len(deposit_pass), 0)
        self.assertEqual(deposit_pass[0].username, "sarah")
        self.assertEqual(deposit_pass[0].severity, Severity.INFO)

        self.print_summary(
            "Test 14 Summary (Successful Deposit Audit Event)",
            [
                ("Username", deposit_pass[0].username),
                ("Action", deposit_pass[0].action.value),
                ("Severity", deposit_pass[0].severity.value),
                ("Status", deposit_pass[0].status.value),
                ("Result", "PASS"),
            ],
        )

    def test_15_rate_limit_exceeded_produces_warning_audit_event(self):
        stack = build_operation_services(
            strict_window_limit=1,
            strict_window_seconds=60.0,
        )

        stack.account_ops.deposit(stack.auth_session, 1001, 10.0)
        with self.assertRaises(RateLimitExceededError):
            stack.account_ops.deposit(stack.auth_session, 1001, 10.0)

        events = stack.registry.get_logger(1001).get_events()
        rl_events = [e for e in events if e.action == SecurityAction.RATE_LIMIT_EXCEEDED]
        self.assertGreater(len(rl_events), 0)
        self.assertEqual(rl_events[0].severity, Severity.WARNING)
        self.assertEqual(rl_events[0].username, "sarah")

        self.print_summary(
            "Test 15 Summary (Rate Limit Audit Event)",
            [
                ("Username", rl_events[0].username),
                ("Action", rl_events[0].action.value),
                ("Severity", rl_events[0].severity.value),
                ("Window limit", 1),
                ("Result", "PASS"),
            ],
        )

    def test_16_threat_report_builder_summarises_events(self):
        clock = TestClock()
        events = [
            SecurityEvent.create(
                clock=clock,
                username="sarah",
                account_number=1001,
                action=SecurityAction.GET_BALANCE,
                amount=EventAmount.balance(1000.0),
                status=EventStatus.PASS,
                message="Balance enquiry",
                severity=Severity.INFO,
            ),
            SecurityEvent.create(
                clock=clock,
                username="sarah",
                account_number=1001,
                action=SecurityAction.FRAUD_DETECTED,
                amount=EventAmount.transaction(600.0),
                status=EventStatus.FLAGGED,
                message="Triggered rules: amount too large",
                severity=Severity.CRITICAL,
            ),
            SecurityEvent.create(
                clock=clock,
                username="sarah",
                account_number=1001,
                action=SecurityAction.RATE_LIMIT_EXCEEDED,
                amount=EventAmount.none(),
                status=EventStatus.BLOCKED,
                message="Request rate limit exceeded",
                severity=Severity.WARNING,
            ),
        ]

        report = (
            ThreatReportBuilder(clock=clock)
            .from_events(events)
            .with_lock_context(locked_accounts=[1001], locked_users=["Sarah"])
            .build()
        )

        self.assertEqual(report.total_events, 3)
        self.assertEqual(report.flagged_accounts, (1001,))
        self.assertEqual(report.locked_accounts, (1001,))
        self.assertEqual(report.locked_users, ("sarah",))
        self.assertEqual(report.rate_limited_accounts, (1001,))
        self.assertIn("HIGH RISK", report.summary)

        self.print_summary(
            "Test 16 Summary (Threat Report Builder)",
            [
                ("Total events", report.total_events),
                ("Flagged accounts", report.flagged_accounts),
                ("Locked accounts", report.locked_accounts),
                ("Locked users", report.locked_users),
                ("Rate limited accounts", report.rate_limited_accounts),
                ("Result", "PASS"),
            ],
        )

    def test_17_system_report_assembler_merges_security_and_auth_events(self):
        stack = build_operation_services()
        stack.account_ops.deposit(stack.auth_session, 1001, 10.0)

        auth_events = [
            AuthEvent(
                timestamp=stack.clock.now(),
                username="sarah",
                action=AuthAction.LOCKOUT,
                status=AuthStatus.LOCKED,
                message="Account locked after failed attempts",
                affected_accounts=(1001,),
            )
        ]

        assembler = SystemReportAssembler(clock=stack.clock)
        report = assembler.build(
            loggers=stack.registry.all_loggers(),
            auth_events=auth_events,
        )

        self.assertIn("sarah", report.locked_users)
        self.assertIn(1001, report.locked_accounts)
        self.assertGreaterEqual(report.total_events, 2)

        self.print_summary(
            "Test 17 Summary (System Report Assembler)",
            [
                ("Locked users", report.locked_users),
                ("Locked accounts", report.locked_accounts),
                ("Total events", report.total_events),
                ("Result", "PASS"),
            ],
        )

    def test_18_threat_report_generator_builds_report_from_logger(self):
        stack = build_operation_services()
        stack.account_ops.deposit(stack.auth_session, 1001, 25.0)

        report = ThreatReportGenerator(clock=stack.clock).generate(
            stack.registry.get_logger(1001)
        )
        self.assertGreaterEqual(report.total_events, 1)

        self.print_summary(
            "Test 18 Summary (Threat Report Generator)",
            [
                ("Account", 1001),
                ("Total events", report.total_events),
                ("Summary", report.summary),
                ("Result", "PASS"),
            ],
        )


# =============================================================================
# Registry and limiter tests
# =============================================================================


class Test05RegistryAndLimiters(PrettyPrintTestCase):
    def test_19_duplicate_account_numbers_are_rejected(self):
        clock = TestClock()
        with self.assertRaises(ValueError):
            AccountSecurityRegistry(
                accounts=[
                    BankAccount(1001, 100.0),
                    BankAccount(1001, 200.0),
                ],
                audit_logger_factory=AuditLoggerFactory(clock=clock),
                log_enabled=True,
            )

        self.print_summary(
            "Test 19 Summary (Duplicate Accounts Rejected)",
            [
                ("Account number", 1001),
                ("Expected", "ValueError"),
                ("Result", "PASS"),
            ],
        )

    def test_20_token_bucket_refills_after_time_advance(self):
        clock = TestClock()
        limiter = RateLimiterFactory(
            creators={
                LimiterType.TOKEN_BUCKET: TokenBucketCreator(clock),
                LimiterType.STRICT_WINDOW: StrictWindowCreator(clock),
            }
        ).create(
            LimiterType.TOKEN_BUCKET,
            TokenBucketConfig(capacity=2, refill_rate=1.0),
        )

        self.assertTrue(limiter.is_allowed("sarah", PERM_DEPOSIT))
        self.assertTrue(limiter.is_allowed("sarah", PERM_DEPOSIT))
        self.assertFalse(limiter.is_allowed("sarah", PERM_DEPOSIT))

        clock.advance(1.1)
        self.assertTrue(limiter.is_allowed("sarah", PERM_DEPOSIT))

        self.print_summary(
            "Test 20 Summary (Token Bucket Refill)",
            [
                ("Username", "sarah"),
                ("Capacity", 2),
                ("Refill rate", 1.0),
                ("Time advanced", 1.1),
                ("Final request", "Allowed"),
                ("Result", "PASS"),
            ],
        )

# =============================================================================
# Final composition root integration test
# =============================================================================
class Test06FinalCompositionRoot(PrettyPrintTestCase):
    def test_21_secure_banking_service_factory_builds_full_service(self):
        clock = TestClock()
        auth_service, _, _, _ = build_auth_service(clock=clock)
        auth_service.register_user("sarah", "StrongPass1")

        authorization_policy = AuthorizationPolicy()
        authorization_policy.grant_access("sarah", 1001, ROLE_OWNER)
        authorization_policy.grant_access("sarah", 1002, ROLE_OWNER)

        alert_monitor = AlertObserver()
        observer_failure_sink = InMemoryObserverFailureSink()
        report_generator = ThreatReportGenerator(clock=clock)

        rate_limiter = RateLimiterFactory(
            creators={
                LimiterType.TOKEN_BUCKET: TokenBucketCreator(clock),
                LimiterType.STRICT_WINDOW: StrictWindowCreator(clock),
            }
        ).create(
            LimiterType.STRICT_WINDOW,
            StrictWindowConfig(max_requests=10, window_seconds=60.0),
        )

        fraud_engine = FraudDetectionEngine(
            [LargeAmountRule(threshold=5000.0)]
        )
        transaction_monitor = TransactionMonitor(clock=clock)

        config = SecurityConfig(
            authenticator=auth_service,
            authorization_policy=authorization_policy,
            transfer_authorization_policy=BasicTransferValidationPolicy(),
            fraud_engine=fraud_engine,
            rate_limiter=rate_limiter,
            report_generator=report_generator,
            transaction_monitor=transaction_monitor,
            alert_monitor=alert_monitor,
            observer_failure_sink=observer_failure_sink,
            clock=clock,
            log_enabled=True,
        )

        service = SecureBankingServiceFactory.create(
            config=config,
            accounts=[
                BankAccount(1001, 1000.0),
                BankAccount(1002, 500.0),
            ],
        )

        auth_session = auth_service.authenticate_session("sarah", "StrongPass1")
        balance = service.deposit(auth_session, 1001, 50.0)
        system_report = service.generate_system_report()

        self.assertEqual(balance, 1050.0)
        self.assertGreaterEqual(system_report.total_events, 1)

        self.print_summary(
            "Test 21 Summary (Final Composition Root)",
            [
                ("Service created", True),
                ("Balance after deposit", balance),
                ("System report events", system_report.total_events),
                ("Result", "PASS"),
            ],
        )
# =============================================================================
# Flow demonstration test
# =============================================================================
class Test07FlowDemonstration(PrettyPrintTestCase):
    def test_22_withdrawal_request_at_3am_flow_demo(self):
        clock = TestClock(
            start_dt=datetime(2026, 4, 4, 3, 0, 0, tzinfo=timezone.utc)
        )

        stack = build_operation_services(
            clock=clock,
            strict_window_limit=20,
            strict_window_seconds=60.0,
            fraud_rules=[
                LargeAmountRule(threshold=5000.0),
                RapidOutgoingTransactionRule(max_recent_actions=5),
                BalanceRatioRule(max_ratio=0.5),
                UnusualHourRule(allowed_start_hour=7, allowed_end_hour=22),
            ],
        )

        username = stack.auth_session.user.username
        account_number = 1001
        amount = 900.0

        print("\n=== Test 22 Flow Demonstration: High-Risk Withdrawal Request at 3 AM ===")

        print("\nStage 1: request entry")
        print(
            f"Incoming high-risk request -> user={username}, action=withdraw, "
            f"account={account_number}, amount={amount}, time={clock.now().strftime('%H:%M')}"
        )

        print("\nStage 2: authenticated session valid")
        session_valid = stack.auth_service.is_authenticated_session(stack.auth_session)
        print(f"Authenticated session valid -> {session_valid}")
        self.assertTrue(session_valid)

        fraud_message = ""
        blocked_by = ""

        try:
            stack.account_ops.withdraw(stack.auth_session, account_number, amount)
            self.fail("Expected FraudAlertError for high-risk withdrawal request at 3 AM")
        except FraudAlertError as exc:
            fraud_message = str(exc)
            blocked_by = "FraudCheckStep"
        except AuthorizationError as exc:
            self.fail(f"Request stopped too early at authorisation layer: {exc}")
        except RateLimitExceededError as exc:
            self.fail(f"Request stopped too early at rate-limiting layer: {exc}")

        final_balance = stack.registry.get_account(account_number).get_balance()
        logger_events = stack.registry.get_logger(account_number).get_events()

        fraud_events = [
            event for event in logger_events
            if event.action == SecurityAction.FRAUD_DETECTED
        ]

        print("\nStage 3: authorisation result")
        print("Authorisation result -> PASS")

        print("\nStage 4: rate limiting result")
        print("Rate limiting result -> PASS")

        print("\nStage 5: fraud rule evaluation")
        print("LargeAmountRule(5000.0) -> not triggered")
        print("RapidOutgoingTransactionRule(5) -> not triggered")
        print("BalanceRatioRule(0.5) -> TRIGGERED")
        print("UnusualHourRule(07:00–22:00) -> TRIGGERED")
        print(f"Fraud triggers -> {fraud_message}")

        self.assertGreaterEqual(len(fraud_events), 1)
        self.assertIn("Amount exceeds 50% of current balance", fraud_message)
        self.assertIn("Transaction outside allowed hours 07:00–22:00", fraud_message)
        self.assertNotIn("Amount exceeds 5000.00", fraud_message)
        self.assertNotIn("Rapid outgoing transaction frequency >= 5", fraud_message)

        print("\nStage 6: execution blocked")
        print(f"Execution blocked by -> {blocked_by}")
        print(f"Balance after blocked request -> {final_balance}")
        self.assertEqual(final_balance, 1000.0)

        print("\nStage 7: logging and alerts")
        print(f"Fraud events -> {len(fraud_events)}")
        print(f"Critical alerts -> {stack.alert_monitor.alert_count()}")
        self.assertGreaterEqual(stack.alert_monitor.alert_count(), 1)

        self.print_summary(
            "Test 22 Summary (High-Risk Withdrawal Request at 3 AM)",
            [
                ("Username", username),
                ("Account", account_number),
                ("Requested amount", amount),
                ("Request time", clock.now().strftime("%H:%M")),
                ("Session valid", session_valid),
                ("Authorisation", "PASS"),
                ("Rate limiting", "PASS"),
                ("LargeAmountRule", "NOT TRIGGERED"),
                ("RapidOutgoingRule", "NOT TRIGGERED"),
                ("BalanceRatioRule", "TRIGGERED"),
                ("UnusualHourRule", "TRIGGERED"),
                ("Blocked by", blocked_by),
                ("Alerts raised", stack.alert_monitor.alert_count()),
                ("Balance unchanged", final_balance),
                ("Result", "BLOCKED AND LOGGED"),
            ],
        )
if __name__ == "__main__":
    unittest.main(verbosity=0)