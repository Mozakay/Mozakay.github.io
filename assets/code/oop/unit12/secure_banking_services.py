from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple

from core_banking import Account, InsufficientFundsError, _validate_amount as validate_amount
from security_layer import (
    AccountNotFoundError,
    AuthSession,
    BoundedSecurityEventStore,
    CriticalEventPublisher,
    EventStatus,
    IAccountAuditLogger,
    IAlertMonitor,
    IAuditDiagnosticsReader,
    IAuditLoggerFactory,
    IAuthorizationPolicy,
    IClock,
    IDiagnosticAuditLoggerFactory,
    IFraudDetectionEngine,
    IObserverFailureSink,
    ISecurityEventFactory,
    ISecurityEventRecorder,
    ISecurityOperationPipeline,
    ISessionAwareAuthService,
    ITransactionMonitor,
    InMemoryObserverFailureSink,
    ObserverNotificationFailure,
    PERM_DEPOSIT,
    PERM_TRANSFER,
    PERM_VIEW_BALANCE,
    PERM_WITHDRAW,
    RateLimiter,
    SecurityAction,
    SecurityEvent,
    SecurityEventFactory,
    SecurityEventRecorder,
    SecurityObserver,
    SecurityOperationPipelineFactory,
    Severity,
    SystemClock,
    User,
)

if TYPE_CHECKING:
    from security_reporting import (
        ThreatReport,
        IThreatReportGenerator,
        ISystemReportAssembler,
    )


_DEFAULT_MAX_EVENTS_PER_ACCOUNT = 5_000


def _unwrap_transfer_account(account: Account) -> Account:
    if not isinstance(account, Account):
        raise TypeError("account must implement Account")

    current = account
    seen_ids: set[int] = set()

    while hasattr(current, "_wrapped") and id(current) not in seen_ids:
        seen_ids.add(id(current))
        wrapped = getattr(current, "_wrapped")
        if not isinstance(wrapped, Account):
            break
        current = wrapped

    return current

def _run_core_transfer(source: Account, destination: Account, amount: float) -> None:
    if not isinstance(source, Account):
        raise TypeError("source must implement Account")
    if not isinstance(destination, Account):
        raise TypeError("destination must implement Account")

    source_account = _unwrap_transfer_account(source)
    destination_account = _unwrap_transfer_account(destination)

    if source_account.account_number == destination_account.account_number:
        raise ValueError("Cannot transfer to the same account")

    amount = validate_amount(amount)

    transfer_method = getattr(source_account, "transfer_to", None)
    if not callable(transfer_method):
        raise TypeError(
            f"Account {source_account.account_number} does not support transfer_to(). "
            "Use a transfer-capable core account such as BankAccount."
        )

    transfer_method(destination_account, amount)

class IAccountOperationAdapter(ABC):
    @property
    @abstractmethod
    def account_number(self) -> int:
        pass

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass


class AccountOperationAdapter(IAccountOperationAdapter):
    def __init__(self, wrapped: Account) -> None:
        if not isinstance(wrapped, Account):
            raise TypeError("wrapped must implement Account")
        self._wrapped = wrapped

    @property
    def account_number(self) -> int:
        return self._wrapped.account_number

    def deposit(self, amount: float) -> None:
        self._wrapped.deposit(amount)

    def withdraw(self, amount: float) -> None:
        self._wrapped.withdraw(amount)

    def get_balance(self) -> float:
        return self._wrapped.get_balance()

class AuditedAccountService(IAccountAuditLogger):
    def __init__(
        self,
        operation_adapter: IAccountOperationAdapter,
        recorder: ISecurityEventRecorder,
        event_factory: ISecurityEventFactory,
    ) -> None:
        if not isinstance(operation_adapter, IAccountOperationAdapter):
            raise TypeError("operation_adapter must implement IAccountOperationAdapter")
        if not isinstance(recorder, ISecurityEventRecorder):
            raise TypeError("recorder must implement ISecurityEventRecorder")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")

        self._event_factory = event_factory

        self._operations = operation_adapter
        self._recorder = recorder

    @property
    def account_number(self) -> int:
        return self._operations.account_number

    def record(self, event: SecurityEvent) -> None:
        self._recorder.record(event)

    def add_observer(self, observer: SecurityObserver) -> None:
        self._recorder.add_observer(observer)

    def get_events(self) -> List[SecurityEvent]:
        return self._recorder.get_events()

    def deposit(self, amount: float, username: str = "system") -> None:
        validate_amount(amount)
        try:
            self._operations.deposit(amount)
            self.record(
                self._event_factory.transaction_event(
                    username=username,
                    account_number=self.account_number,
                    action=SecurityAction.DEPOSIT,
                    amount=amount,
                    status=EventStatus.PASS,
                    message="Deposit completed successfully",
                    severity=Severity.INFO,
                )
            )
        except Exception as exc:
            self.record(
                self._event_factory.safe_transaction_event(
                    username=username,
                    account_number=self.account_number,
                    action=SecurityAction.DEPOSIT,
                    amount=amount,
                    status=EventStatus.FAILED,
                    message=str(exc),
                    severity=Severity.WARNING,
                )
            )
            raise

    def withdraw(self, amount: float, username: str = "system") -> None:
        validate_amount(amount)
        try:
            self._operations.withdraw(amount)
            self.record(
                self._event_factory.transaction_event(
                    username=username,
                    account_number=self.account_number,
                    action=SecurityAction.WITHDRAW,
                    amount=amount,
                    status=EventStatus.PASS,
                    message="Withdrawal completed successfully",
                    severity=Severity.INFO,
                )
            )
        except InsufficientFundsError as exc:
            self.record(
                self._event_factory.safe_transaction_event(
                    username=username,
                    account_number=self.account_number,
                    action=SecurityAction.WITHDRAW,
                    amount=amount,
                    status=EventStatus.FAILED,
                    message=str(exc),
                    severity=Severity.WARNING,
                )
            )
            raise
        except Exception as exc:
            self.record(
                self._event_factory.safe_transaction_event(
                    username=username,
                    account_number=self.account_number,
                    action=SecurityAction.WITHDRAW,
                    amount=amount,
                    status=EventStatus.FAILED,
                    message=str(exc),
                    severity=Severity.CRITICAL,
                )
            )
            raise

class AuditLoggerFactory(IDiagnosticAuditLoggerFactory):
    def __init__(
        self,
        clock: Optional[IClock] = None,
        failure_sink: Optional[IObserverFailureSink] = None,
        max_events_per_account: int = _DEFAULT_MAX_EVENTS_PER_ACCOUNT,
    ) -> None:
        resolved_failure_sink = (
            InMemoryObserverFailureSink() if failure_sink is None else failure_sink
        )
        resolved_clock = SystemClock() if clock is None else clock

        self._failure_sink = resolved_failure_sink
        self._clock = resolved_clock
        self._max_events_per_account = int(max_events_per_account)

        if not isinstance(self._clock, IClock):
            raise TypeError("clock must implement IClock")
        if not isinstance(self._failure_sink, IObserverFailureSink):
            raise TypeError("failure_sink must implement IObserverFailureSink")
        if self._max_events_per_account < 1:
            raise ValueError("max_events_per_account must be >= 1")

    def observer_failures(self) -> List[ObserverNotificationFailure]:
        return self._failure_sink.all()

    def create(self, account: Account, enabled: bool = True) -> IAccountAuditLogger:
        event_factory = SecurityEventFactory(self._clock)
        return AuditedAccountService(
            operation_adapter=AccountOperationAdapter(account),
            recorder=SecurityEventRecorder(
                event_store=BoundedSecurityEventStore(
                    max_events=self._max_events_per_account
                ),
                publisher=CriticalEventPublisher(
                    failure_sink=self._failure_sink,
                    clock=self._clock,
                ),
                enabled=enabled,
            ),
            event_factory=event_factory,
        )


class IAccountOperationService(ABC):
    @abstractmethod
    def deposit(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        pass

    @abstractmethod
    def withdraw(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        pass

    @abstractmethod
    def get_balance(self, auth_session: AuthSession, account_number: int) -> float:
        pass


class ITransferService(ABC):
    @abstractmethod
    def transfer(
        self,
        auth_session: AuthSession,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> Tuple[float, float]:
        pass

class IAccountSecurityRegistry(ABC):
    @abstractmethod
    def get_account(self, account_number: int) -> Account:
        pass

    @abstractmethod
    def get_logger(self, account_number: int) -> IAccountAuditLogger:
        pass

    @abstractmethod
    def add_global_observer(self, observer: SecurityObserver) -> None:
        pass

    @abstractmethod
    def all_loggers(self) -> List[IAccountAuditLogger]:
        pass

class AccountSecurityRegistry(IAccountSecurityRegistry):
    def __init__(
        self,
        accounts: Iterable[Account],
        audit_logger_factory: IAuditLoggerFactory,
        log_enabled: bool,
    ) -> None:
        if not isinstance(audit_logger_factory, IAuditLoggerFactory):
            raise TypeError("audit_logger_factory must implement IAuditLoggerFactory")
        if not isinstance(log_enabled, bool):
            raise TypeError("log_enabled must be a bool")

        account_list = list(accounts)
        if not account_list:
            raise ValueError("accounts must contain at least one Account")

        self._accounts: Dict[int, Account] = {}
        self._loggers: Dict[int, IAccountAuditLogger] = {}

        for account in account_list:
            if not isinstance(account, Account):
                raise TypeError("all items in accounts must implement Account")
            if account.account_number in self._accounts:
                raise ValueError("Duplicate account numbers are not allowed")

            self._accounts[account.account_number] = account
            self._loggers[account.account_number] = audit_logger_factory.create(
                account,
                enabled=log_enabled,
            )

    def get_account(self, account_number: int) -> Account:
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        account = self._accounts.get(account_number)
        if account is None:
            raise AccountNotFoundError(f"Account {account_number} not found")
        return account

    def get_logger(self, account_number: int) -> IAccountAuditLogger:
        if not isinstance(account_number, int):
            raise TypeError("account_number must be an int")
        logger = self._loggers.get(account_number)
        if logger is None:
            raise AccountNotFoundError(f"Logger for account {account_number} not found")
        return logger

    def add_global_observer(self, observer: SecurityObserver) -> None:
        if not isinstance(observer, SecurityObserver):
            raise TypeError("observer must be a SecurityObserver")
        for logger in self._loggers.values():
            logger.add_observer(observer)

    def all_loggers(self) -> List[IAccountAuditLogger]:
        return list(self._loggers.values())



class SecureAccountOperationService(IAccountOperationService):
    def __init__(
        self,
        pipeline: ISecurityOperationPipeline,
        registry: IAccountSecurityRegistry,
        transaction_monitor: ITransactionMonitor,
        event_factory: ISecurityEventFactory,
    ) -> None:
        if not isinstance(pipeline, ISecurityOperationPipeline):
            raise TypeError("pipeline must implement ISecurityOperationPipeline")
        if not isinstance(registry, IAccountSecurityRegistry):
            raise TypeError("registry must implement IAccountSecurityRegistry")
        if not isinstance(transaction_monitor, ITransactionMonitor):
            raise TypeError("transaction_monitor must implement ITransactionMonitor")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")

        self._event_factory = event_factory

        self._pipeline = pipeline
        self._registry = registry
        self._monitor = transaction_monitor

    def deposit(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        validate_amount(amount)
        account = self._registry.get_account(account_number)
        logger = self._registry.get_logger(account_number)

        self._pipeline.secure_monetary_action(
            auth_session=auth_session,
            account_number=account_number,
            action=PERM_DEPOSIT,
            amount=amount,
            account=account,
            logger=logger,
        )

        logger.deposit(amount, auth_session.user.username)
        self._monitor.record(account_number, PERM_DEPOSIT, auth_session.user.username)
        return account.get_balance()

    def withdraw(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        validate_amount(amount)
        account = self._registry.get_account(account_number)
        logger = self._registry.get_logger(account_number)

        self._pipeline.secure_monetary_action(
            auth_session=auth_session,
            account_number=account_number,
            action=PERM_WITHDRAW,
            amount=amount,
            account=account,
            logger=logger,
        )

        logger.withdraw(amount, auth_session.user.username)
        self._monitor.record(account_number, PERM_WITHDRAW, auth_session.user.username)
        return account.get_balance()

    def get_balance(self, auth_session: AuthSession, account_number: int) -> float:
        account = self._registry.get_account(account_number)
        logger = self._registry.get_logger(account_number)

        self._pipeline.secure_read(
            auth_session=auth_session,
            account_number=account_number,
            action=PERM_VIEW_BALANCE,
            logger=logger,
        )

        balance = account.get_balance()
        logger.record(
            self._event_factory.balance_event(
                username=auth_session.user.username,
                account_number=account_number,
                action=SecurityAction.GET_BALANCE,
                balance=balance,
                status=EventStatus.PASS,
                message="Balance enquiry",
                severity=Severity.INFO,
            )
        )
        return balance
    
class ITransferAuthorizationPolicy(ABC):
    @abstractmethod
    def authorize(
        self,
        user: User,
        from_account_number: int,
        to_account_number: int,
    ) -> None:
        pass


class BasicTransferValidationPolicy(ITransferAuthorizationPolicy):

    def authorize(
        self,
        user: User,
        from_account_number: int,
        to_account_number: int,
    ) -> None:
        if not isinstance(user, User):
            raise TypeError("user must be a User")
        if not isinstance(from_account_number, int):
            raise TypeError("from_account_number must be an int")
        if not isinstance(to_account_number, int):
            raise TypeError("to_account_number must be an int")
        if from_account_number == to_account_number:
            raise ValueError("Cannot transfer to the same account")


class SecureTransferService(ITransferService):
    def __init__(
        self,
        pipeline: ISecurityOperationPipeline,
        registry: IAccountSecurityRegistry,
        transaction_monitor: ITransactionMonitor,
        transfer_authorization_policy: ITransferAuthorizationPolicy,
        event_factory: ISecurityEventFactory,
    ) -> None:
        if not isinstance(pipeline, ISecurityOperationPipeline):
            raise TypeError("pipeline must implement ISecurityOperationPipeline")
        if not isinstance(registry, IAccountSecurityRegistry):
            raise TypeError("registry must implement IAccountSecurityRegistry")
        if not isinstance(transaction_monitor, ITransactionMonitor):
            raise TypeError("transaction_monitor must implement ITransactionMonitor")
        if not isinstance(transfer_authorization_policy, ITransferAuthorizationPolicy):
            raise TypeError(
                "transfer_authorization_policy must implement ITransferAuthorizationPolicy")
        if not isinstance(event_factory, ISecurityEventFactory):
            raise TypeError("event_factory must implement ISecurityEventFactory")

        self._event_factory = event_factory

        self._pipeline = pipeline
        self._registry = registry
        self._monitor = transaction_monitor
        self._transfer_authorization_policy = transfer_authorization_policy

    def transfer(
        self,
        auth_session: AuthSession,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> Tuple[float, float]:
        validate_amount(amount)

        self._transfer_authorization_policy.authorize(
            user=auth_session.user,
            from_account_number=from_account_number,
            to_account_number=to_account_number,
        )

        source = self._registry.get_account(from_account_number)
        destination = self._registry.get_account(to_account_number)
        source_logger = self._registry.get_logger(from_account_number)
        destination_logger = self._registry.get_logger(to_account_number)

        self._pipeline.secure_monetary_action(
            auth_session=auth_session,
            account_number=from_account_number,
            action=PERM_TRANSFER,
            amount=amount,
            account=source,
            logger=source_logger,
        )

        try:
            _run_core_transfer(source, destination, amount)
        except InsufficientFundsError as exc:
            source_logger.record(
                self._event_factory.transaction_event(
                    username=auth_session.user.username,
                    account_number=from_account_number,
                    action=SecurityAction.TRANSFER_OUT,
                    amount=amount,
                    status=EventStatus.FAILED,
                    message=str(exc),
                    severity=Severity.WARNING,
                )
            )
            raise
        except Exception as exc:
            source_logger.record(
                self._event_factory.safe_transaction_event(
                    username=auth_session.user.username,
                    account_number=from_account_number,
                    action=SecurityAction.TRANSFER_OUT,
                    amount=amount,
                    status=EventStatus.FAILED,
                    message=str(exc),
                    severity=Severity.CRITICAL,
                )
            )
            raise

        self._monitor.record(from_account_number, PERM_TRANSFER, auth_session.user.username)

        source_logger.record(
            self._event_factory.transaction_event(
                username=auth_session.user.username,
                account_number=from_account_number,
                action=SecurityAction.TRANSFER_OUT,
                amount=amount,
                status=EventStatus.PASS,
                message=f"Transferred {amount:.2f} to account {to_account_number}",
                severity=Severity.INFO,
            )
        )
        destination_logger.record(
            self._event_factory.transaction_event(
                username=auth_session.user.username,
                account_number=to_account_number,
                action=SecurityAction.TRANSFER_IN,
                amount=amount,
                status=EventStatus.PASS,
                message=f"Received {amount:.2f} from account {from_account_number}",
                severity=Severity.INFO,
            )
        )

        return source.get_balance(), destination.get_balance()
    
    
@dataclass(frozen=True, slots=True)
class SecurityConfig:
    authenticator: ISessionAwareAuthService
    authorization_policy: IAuthorizationPolicy
    transfer_authorization_policy: ITransferAuthorizationPolicy
    fraud_engine: IFraudDetectionEngine
    rate_limiter: RateLimiter
    report_generator: IThreatReportGenerator
    transaction_monitor: ITransactionMonitor
    alert_monitor: IAlertMonitor
    observer_failure_sink: IObserverFailureSink = field(
        default_factory=InMemoryObserverFailureSink
    )
    audit_logger_factory: Optional[IDiagnosticAuditLoggerFactory] = None
    clock: IClock = field(default_factory=SystemClock)
    log_enabled: bool = True

    def __post_init__(self) -> None:
        from security_reporting import IThreatReportGenerator

        if not isinstance(self.authenticator, ISessionAwareAuthService):
            raise TypeError("authenticator must implement ISessionAwareAuthService")
        if not isinstance(self.authorization_policy, IAuthorizationPolicy):
            raise TypeError("authorization_policy must implement IAuthorizationPolicy")
        if not isinstance(self.transfer_authorization_policy, ITransferAuthorizationPolicy):
            raise TypeError("transfer_authorization_policy must implement ITransferAuthorizationPolicy")
        if not isinstance(self.fraud_engine, IFraudDetectionEngine):
            raise TypeError("fraud_engine must implement IFraudDetectionEngine")
        if not isinstance(self.rate_limiter, RateLimiter):
            raise TypeError("rate_limiter must implement RateLimiter")
        if not isinstance(self.report_generator, IThreatReportGenerator):
            raise TypeError("report_generator must implement IThreatReportGenerator")
        if not isinstance(self.transaction_monitor, ITransactionMonitor):
            raise TypeError("transaction_monitor must implement ITransactionMonitor")
        if not isinstance(self.alert_monitor, IAlertMonitor):
            raise TypeError("alert_monitor must implement IAlertMonitor")
        if not isinstance(self.observer_failure_sink, IObserverFailureSink):
            raise TypeError("observer_failure_sink must implement IObserverFailureSink")
        if not isinstance(self.clock, IClock):
            raise TypeError("clock must implement IClock")
        if not isinstance(self.log_enabled, bool):
            raise TypeError("log_enabled must be a bool")

        if self.audit_logger_factory is not None and not isinstance(
            self.audit_logger_factory,
            IDiagnosticAuditLoggerFactory,
        ):
            raise TypeError(
                "audit_logger_factory must implement IDiagnosticAuditLoggerFactory")
        
class SecureBankingService:
    """
    Thin façade responsible for coordinating security checks around the banking
    system. Core banking logic remains in core_banking.py.
    """
    def __init__(
        self,
        *,
        authenticator: ISessionAwareAuthService,
        report_generator: IThreatReportGenerator,
        alert_monitor: IAlertMonitor,
        rate_limiter: RateLimiter,
        audit_diagnostics_reader: IAuditDiagnosticsReader,
        registry: IAccountSecurityRegistry,
        account_ops: IAccountOperationService,
        transfer_service: ITransferService,
        system_report_assembler: ISystemReportAssembler,
    ) -> None:
        from security_reporting import IThreatReportGenerator, ISystemReportAssembler
        
        if not isinstance(authenticator, ISessionAwareAuthService):
            raise TypeError("authenticator must implement ISessionAwareAuthService")
        if not isinstance(report_generator, IThreatReportGenerator):
            raise TypeError("report_generator must implement IThreatReportGenerator")
        if not isinstance(alert_monitor, IAlertMonitor):
            raise TypeError("alert_monitor must implement IAlertMonitor")
        if not isinstance(rate_limiter, RateLimiter):
            raise TypeError("rate_limiter must implement RateLimiter")
        if not isinstance(audit_diagnostics_reader, IAuditDiagnosticsReader):
            raise TypeError(
                "audit_diagnostics_reader must implement IAuditDiagnosticsReader")
        if not isinstance(registry, IAccountSecurityRegistry):
            raise TypeError("registry must implement IAccountSecurityRegistry")
        if not isinstance(account_ops, IAccountOperationService):
            raise TypeError("account_ops must implement IAccountOperationService")
        if not isinstance(transfer_service, ITransferService):
            raise TypeError("transfer_service must implement ITransferService")
        if not isinstance(system_report_assembler, ISystemReportAssembler):
            raise TypeError("system_report_assembler must implement ISystemReportAssembler")

        self._auth = authenticator
        self._report_generator = report_generator
        self._alert_observer = alert_monitor
        self._limiter = rate_limiter
        self._audit_diagnostics_reader = audit_diagnostics_reader
        self._registry = registry
        self._account_ops = account_ops
        self._transfer_service = transfer_service
        self._system_report_assembler = system_report_assembler

    def deposit(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        return self._account_ops.deposit(auth_session, account_number, amount)

    def withdraw(self, auth_session: AuthSession, account_number: int, amount: float) -> float:
        return self._account_ops.withdraw(auth_session, account_number, amount)

    def transfer(
        self,
        auth_session: AuthSession,
        from_account_number: int,
        to_account_number: int,
        amount: float,
    ) -> Tuple[float, float]:
        return self._transfer_service.transfer(
            auth_session=auth_session,
            from_account_number=from_account_number,
            to_account_number=to_account_number,
            amount=amount,
        )

    def get_balance(self, auth_session: AuthSession, account_number: int) -> float:
        return self._account_ops.get_balance(auth_session, account_number)

    def logout(self, auth_session: AuthSession) -> None:
        if not isinstance(auth_session, AuthSession):
            raise TypeError("auth_session must be an AuthSession")
        self._auth.logout_session(auth_session.session_id)
        self._limiter.reset(auth_session.user.username)

    def get_events(self, account_number: int) -> List[SecurityEvent]:
        return self._registry.get_logger(account_number).get_events()

    def generate_account_report(self, account_number: int) -> ThreatReport:
        return self._report_generator.generate(self._registry.get_logger(account_number))

    def generate_system_report(self) -> ThreatReport:
        return self._system_report_assembler.build(
            loggers=self._registry.all_loggers(),
            auth_events=self._auth.get_auth_events(),
        )

    @property
    def alert_count(self) -> int:
        return self._alert_observer.alert_count()

    @property
    def alerts(self) -> List[SecurityEvent]:
        return self._alert_observer.get_alerts()

    @property
    def observer_failures(self) -> List[ObserverNotificationFailure]:
        return self._audit_diagnostics_reader.observer_failures()

class SecureBankingServiceFactory:
    @staticmethod
    def create(
        config: SecurityConfig,
        accounts: Iterable[Account],
    ) -> "SecureBankingService":
        from security_reporting import AuthEventToSecurityEventMapper, SystemReportAssembler
    
        if not isinstance(config, SecurityConfig):
            raise TypeError("config must be a SecurityConfig")

        event_factory = SecurityEventFactory(config.clock)

        resolved_audit_logger_factory = (
            AuditLoggerFactory(
                clock=config.clock,
                failure_sink=config.observer_failure_sink,
            )
            if config.audit_logger_factory is None
            else config.audit_logger_factory
        )

        registry = AccountSecurityRegistry(
            accounts=accounts,
            audit_logger_factory=resolved_audit_logger_factory,
            log_enabled=config.log_enabled,
        )
        registry.add_global_observer(config.alert_monitor)

        pipeline = SecurityOperationPipelineFactory.from_legacy_dependencies(
            authenticator=config.authenticator,
            authorization_policy=config.authorization_policy,
            fraud_engine=config.fraud_engine,
            rate_limiter=config.rate_limiter,
            transaction_monitor=config.transaction_monitor,
            clock=config.clock,
            event_factory=event_factory,
        )

        account_ops = SecureAccountOperationService(
            pipeline=pipeline,
            registry=registry,
            transaction_monitor=config.transaction_monitor,
            event_factory=event_factory,
        )

        transfer_service = SecureTransferService(
            pipeline=pipeline,
            registry=registry,
            transaction_monitor=config.transaction_monitor,
            transfer_authorization_policy=config.transfer_authorization_policy,
            event_factory=event_factory,
        )

        system_report_assembler = SystemReportAssembler(
            clock=config.clock,
            auth_event_mapper=AuthEventToSecurityEventMapper(),
        )   

        return SecureBankingService(
            authenticator=config.authenticator,
            report_generator=config.report_generator,
            alert_monitor=config.alert_monitor,
            rate_limiter=config.rate_limiter,
            audit_diagnostics_reader=resolved_audit_logger_factory,
            registry=registry,
            account_ops=account_ops,
            transfer_service=transfer_service,
            system_report_assembler=system_report_assembler,
        )