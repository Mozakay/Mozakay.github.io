from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

from security_layer import (
    AuthAction,
    AuthEvent,
    EventAmount,
    EventStatus,
    IAccountAuditLogger,
    IClock,
    ISecurityEventSource,
    SecurityAction,
    SecurityEvent,
    Severity,
    SystemClock,
    _format_datetime,
    _normalize_datetime,
    _normalize_username,
)

# =============================================================================
# SECTION 8 — THREAT REPORTING (BUILDER PATTERN)
# =============================================================================

_AUTH_ACTION_TO_SECURITY_ACTION: Mapping[AuthAction, SecurityAction] = MappingProxyType(
    {
        AuthAction.LOGIN: SecurityAction.AUTH_LOGIN,
        AuthAction.LOGOUT: SecurityAction.AUTH_LOGOUT,
        AuthAction.LOCKOUT: SecurityAction.AUTH_LOCKOUT,
        AuthAction.BLOCKED_LOGIN: SecurityAction.AUTH_BLOCKED_LOGIN,
    }
)

_AUTH_STATUS_TO_EVENT_STATUS: Mapping = MappingProxyType(
    {
        "PASS": EventStatus.PASS,
        "FAILED": EventStatus.FAILED,
        "LOCKED": EventStatus.LOCKED,
        "BLOCKED": EventStatus.BLOCKED,
    }
)

_AUTH_STATUS_TO_SEVERITY: Mapping = MappingProxyType(
    {
        "PASS": Severity.INFO,
        "FAILED": Severity.WARNING,
        "BLOCKED": Severity.WARNING,
        "LOCKED": Severity.CRITICAL,
    }
)


@dataclass(frozen=True, slots=True)
class ThreatReport:
    generated_at: datetime
    total_events: int
    counts_by_severity: Mapping[Severity, int]
    flagged_accounts: Tuple[int, ...]
    locked_accounts: Tuple[int, ...]
    locked_users: Tuple[str, ...]
    rate_limited_accounts: Tuple[int, ...]
    fraud_events: Tuple[SecurityEvent, ...]
    critical_events: Tuple[SecurityEvent, ...]
    summary: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "generated_at",
            _normalize_datetime(self.generated_at, "generated_at"),
        )

        if not isinstance(self.total_events, int) or self.total_events < 0:
            raise ValueError("total_events must be a non-negative integer")
        if not isinstance(self.summary, str):
            raise TypeError("summary must be a string")
        if not isinstance(self.counts_by_severity, Mapping):
            raise TypeError("counts_by_severity must be a mapping")

        raw_counts = dict(self.counts_by_severity)
        normalized_counts: Dict[Severity, int] = {level: 0 for level in Severity}
        for key, value in raw_counts.items():
            if not isinstance(key, Severity):
                raise TypeError("counts_by_severity keys must be Severity values")
            if not isinstance(value, int) or value < 0:
                raise ValueError(
                    "counts_by_severity values must be non-negative integers"
                )
            normalized_counts[key] = value

        normalized_flagged_accounts: List[int] = []
        for account in self.flagged_accounts:
            if not isinstance(account, int):
                raise TypeError("flagged_accounts must contain int values")
            normalized_flagged_accounts.append(account)

        normalized_locked_accounts: List[int] = []
        for account in self.locked_accounts:
            if not isinstance(account, int):
                raise TypeError("locked_accounts must contain int values")
            normalized_locked_accounts.append(account)

        normalized_locked_users: List[str] = []
        for username in self.locked_users:
            if not isinstance(username, str):
                raise TypeError("locked_users must contain str values")
            normalized_locked_users.append(_normalize_username(username))

        normalized_rate_limited_accounts: List[int] = []
        for account in self.rate_limited_accounts:
            if not isinstance(account, int):
                raise TypeError("rate_limited_accounts must contain int values")
            normalized_rate_limited_accounts.append(account)

        for event in self.fraud_events:
            if not isinstance(event, SecurityEvent):
                raise TypeError("fraud_events must contain SecurityEvent values")

        for event in self.critical_events:
            if not isinstance(event, SecurityEvent):
                raise TypeError("critical_events must contain SecurityEvent values")

        object.__setattr__(
            self,
            "counts_by_severity",
            MappingProxyType(normalized_counts),
        )
        object.__setattr__(
            self,
            "flagged_accounts",
            tuple(sorted(set(normalized_flagged_accounts))),
        )
        object.__setattr__(
            self,
            "locked_accounts",
            tuple(sorted(set(normalized_locked_accounts))),
        )
        object.__setattr__(
            self,
            "locked_users",
            tuple(sorted(set(normalized_locked_users))),
        )
        object.__setattr__(
            self,
            "rate_limited_accounts",
            tuple(sorted(set(normalized_rate_limited_accounts))),
        )
        object.__setattr__(self, "fraud_events", tuple(self.fraud_events))
        object.__setattr__(self, "critical_events", tuple(self.critical_events))


class ThreatReportPrinter:
    def print(self, report: ThreatReport) -> None:
        if not isinstance(report, ThreatReport):
            raise TypeError("report must be a ThreatReport")

        sep = "=" * 70
        print(f"\n{sep}")
        print("  THREAT REPORT — SECURE BANKING SERVICE")
        print(sep)
        print(f"  Generated at : {_format_datetime(report.generated_at)}")
        print(f"  Total events : {report.total_events}")
        print()
        print("  SEVERITY BREAKDOWN")
        print(f"    INFO     : {report.counts_by_severity.get(Severity.INFO, 0)}")
        print(f"    WARNING  : {report.counts_by_severity.get(Severity.WARNING, 0)}")
        print(f"    CRITICAL : {report.counts_by_severity.get(Severity.CRITICAL, 0)}")
        print()
        print(f"  Locked accounts       : {list(report.locked_accounts) or 'None'}")
        print(f"  Locked users          : {list(report.locked_users) or 'None'}")
        print(f"  Flagged accounts      : {list(report.flagged_accounts) or 'None'}")
        print(
            f"  Rate-limited accounts : {list(report.rate_limited_accounts) or 'None'}"
        )

        if report.fraud_events:
            print("\n  FRAUD EVENTS")
            for event in report.fraud_events:
                print(f"    {event}")

        if report.critical_events:
            print("\n  ALL CRITICAL EVENTS")
            for event in report.critical_events:
                print(f"    {event}")

        print()
        print(f"  SUMMARY: {report.summary}")
        print(sep)


class ThreatReportJsonSerializer:
    def to_json(self, report: ThreatReport) -> str:
        if not isinstance(report, ThreatReport):
            raise TypeError("report must be a ThreatReport")

        return json.dumps(
            {
                "generated_at": _format_datetime(report.generated_at),
                "total_events": report.total_events,
                "counts_by_severity": {
                    severity.value: count
                    for severity, count in report.counts_by_severity.items()
                },
                "flagged_accounts": list(report.flagged_accounts),
                "locked_accounts": list(report.locked_accounts),
                "locked_users": list(report.locked_users),
                "rate_limited_accounts": list(report.rate_limited_accounts),
                "fraud_event_count": len(report.fraud_events),
                "critical_event_count": len(report.critical_events),
                "summary": report.summary,
            },
            indent=2,
        )


class ThreatReportBuilder:
    def __init__(self, clock: Optional[IClock] = None) -> None:
        resolved_clock = SystemClock() if clock is None else clock
        if not isinstance(resolved_clock, IClock):
            raise TypeError("clock must implement IClock")

        self._clock = resolved_clock
        self._events: Tuple[SecurityEvent, ...] = tuple()
        self._locked_accounts_override: Tuple[int, ...] = tuple()
        self._locked_users_override: Tuple[str, ...] = tuple()

    def from_logger(self, logger: ISecurityEventSource) -> "ThreatReportBuilder":
        if not isinstance(logger, ISecurityEventSource):
            raise TypeError("logger must implement ISecurityEventSource")
        return self.from_events(logger.get_events())

    def from_events(self, events: Iterable[SecurityEvent]) -> "ThreatReportBuilder":
        materialized = tuple(events)
        for event in materialized:
            if not isinstance(event, SecurityEvent):
                raise TypeError("All items must be SecurityEvent objects")
        self._events = materialized
        return self

    def with_lock_context(
        self,
        *,
        locked_accounts: Iterable[int] = (),
        locked_users: Iterable[str] = (),
    ) -> "ThreatReportBuilder":
        normalized_accounts: List[int] = []
        for account in locked_accounts:
            if not isinstance(account, int):
                raise TypeError("locked_accounts must contain int values")
            normalized_accounts.append(account)

        normalized_users: List[str] = []
        for username in locked_users:
            if not isinstance(username, str):
                raise TypeError("locked_users must contain str values")
            normalized_users.append(_normalize_username(username))

        self._locked_accounts_override = tuple(sorted(set(normalized_accounts)))
        self._locked_users_override = tuple(sorted(set(normalized_users)))
        return self

    def build(self) -> ThreatReport:
        counts: Dict[Severity, int] = {level: 0 for level in Severity}
        for event in self._events:
            counts[event.severity] += 1

        fraud_events = tuple(
            event
            for event in self._events
            if event.action == SecurityAction.FRAUD_DETECTED
        )
        critical_events = tuple(
            event
            for event in self._events
            if event.severity == Severity.CRITICAL
        )

        flagged_accounts = tuple(
            sorted(
                {
                    event.account_number
                    for event in fraud_events
                    if event.account_number is not None
                }
            )
        )

        rate_limited_accounts = tuple(
            sorted(
                {
                    event.account_number
                    for event in self._events
                    if event.action == SecurityAction.RATE_LIMIT_EXCEEDED
                    and event.account_number is not None
                }
            )
        )

        critical_count = counts.get(Severity.CRITICAL, 0)
        warning_count = counts.get(Severity.WARNING, 0)

        if critical_count > 0:
            summary = (
                f"HIGH RISK — {critical_count} critical event(s) detected. "
                "Immediate investigation is recommended."
            )
        elif warning_count > 0:
            summary = (
                f"MODERATE RISK — {warning_count} warning event(s) detected. "
                "Monitoring is recommended."
            )
        else:
            summary = (
                f"LOW RISK — {len(self._events)} informational event(s) recorded. "
                "No major threat indicators detected."
            )

        return ThreatReport(
            generated_at=self._clock.now(),
            total_events=len(self._events),
            counts_by_severity=counts,
            flagged_accounts=flagged_accounts,
            locked_accounts=self._locked_accounts_override,
            locked_users=self._locked_users_override,
            rate_limited_accounts=rate_limited_accounts,
            fraud_events=fraud_events,
            critical_events=critical_events,
            summary=summary,
        )


class IThreatReportGenerator(ABC):
    @abstractmethod
    def generate(self, logger: ISecurityEventSource) -> ThreatReport:
        pass


class ThreatReportGenerator(IThreatReportGenerator):
    def __init__(self, clock: Optional[IClock] = None) -> None:
        resolved_clock = SystemClock() if clock is None else clock
        if not isinstance(resolved_clock, IClock):
            raise TypeError("clock must implement IClock")
        self._clock = resolved_clock

    def generate(self, logger: ISecurityEventSource) -> ThreatReport:
        if not isinstance(logger, ISecurityEventSource):
            raise TypeError("logger must implement ISecurityEventSource")
        return ThreatReportBuilder(clock=self._clock).from_logger(logger).build()


class IAuthEventToSecurityEventMapper(ABC):
    @abstractmethod
    def map(self, event: AuthEvent) -> SecurityEvent:
        pass


class AuthEventToSecurityEventMapper(IAuthEventToSecurityEventMapper):
    def map(self, event: AuthEvent) -> SecurityEvent:
        if not isinstance(event, AuthEvent):
            raise TypeError("event must be an AuthEvent")

        action = _AUTH_ACTION_TO_SECURITY_ACTION[event.action]
        status = _AUTH_STATUS_TO_EVENT_STATUS[event.status.value]
        severity = _AUTH_STATUS_TO_SEVERITY[event.status.value]

        return SecurityEvent(
            timestamp=event.timestamp,
            username=event.username,
            account_number=None,
            action=action,
            amount=EventAmount.none(),
            status=status,
            message=event.message,
            severity=severity,
        )


class ISystemReportAssembler(ABC):
    @abstractmethod
    def build(
        self,
        loggers: Iterable[IAccountAuditLogger],
        auth_events: Iterable[AuthEvent],
    ) -> ThreatReport:
        pass


class SystemReportAssembler(ISystemReportAssembler):
    def __init__(
        self,
        clock: IClock,
        auth_event_mapper: Optional[IAuthEventToSecurityEventMapper] = None,
    ) -> None:
        if not isinstance(clock, IClock):
            raise TypeError("clock must implement IClock")

        resolved_mapper = (
            AuthEventToSecurityEventMapper()
            if auth_event_mapper is None
            else auth_event_mapper
        )
        if not isinstance(resolved_mapper, IAuthEventToSecurityEventMapper):
            raise TypeError(
                "auth_event_mapper must implement IAuthEventToSecurityEventMapper"
            )

        self._clock = clock
        self._auth_event_mapper = resolved_mapper

    def build(
        self,
        loggers: Iterable[IAccountAuditLogger],
        auth_events: Iterable[AuthEvent],
    ) -> ThreatReport:
        all_events: List[SecurityEvent] = []
        locked_users: set[str] = set()
        locked_accounts: set[int] = set()

        for logger in loggers:
            if not isinstance(logger, IAccountAuditLogger):
                raise TypeError("loggers must contain IAccountAuditLogger values")
            all_events.extend(logger.get_events())

        for event in auth_events:
            if not isinstance(event, AuthEvent):
                raise TypeError("auth_events must contain AuthEvent values")

            all_events.append(self._auth_event_mapper.map(event))

            if event.action == AuthAction.LOCKOUT:
                locked_users.add(_normalize_username(event.username))
                locked_accounts.update(event.affected_accounts)

        return (
            ThreatReportBuilder(clock=self._clock)
            .from_events(all_events)
            .with_lock_context(
                locked_accounts=locked_accounts,
                locked_users=locked_users,
            )
            .build()
        )