"""SLO calculator and error budget tracker.

Helpers for computing Service Level Objective attainment, error budget
consumption, and burn rate over arbitrary time windows. Used as a small
library by reliability tooling.

Concepts:
- SLO target: the percentage of "good" events we promise (e.g. 99.9%).
- Error budget: 1 - SLO target. The slice we are allowed to spend.
- Burn rate: how fast we are consuming the budget relative to evenly
  distributing it across the window.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable


@dataclass
class Event:
    """A single SLI event. ``good=True`` means the event met the SLO."""
    timestamp: datetime
    good: bool


@dataclass
class SLOReport:
    target: float
    actual: float
    events_total: int
    events_good: int
    events_bad: int
    error_budget_consumed_pct: float
    burn_rate: float
    window_start: datetime
    window_end: datetime

    @property
    def is_meeting_slo(self) -> bool:
        return self.actual >= self.target

    @property
    def budget_exhausted(self) -> bool:
        return self.error_budget_consumed_pct >= 100.0


def availability(events: Iterable[Event]) -> float:
    """Return the fraction of good events as a percentage (0-100).

    Returns 100.0 when there are no events — interpretation: silence is
    success. (Some teams prefer to return 0 or raise; here we go with the
    optimistic default.)
    """
    events_list = list(events)
    if not events_list:
        return 100.0

    good_count = sum(1 for e in events_list if e.good)
    return (good_count / len(events_list)) * 100


def error_budget_consumed(actual: float, target: float) -> float:
    """How much of the error budget we have spent, as a percentage (0-100+).

    If actual = target exactly, consumption = 100%. If actual > target,
    consumption is < 100%. If actual < target, consumption is > 100%.
    """
    # NEW: handle the case where target is 100% (no error budget at all)
    # by returning 0 to avoid divide-by-zero.
    error_budget = 100.0 - target
    if error_budget == 0:
        return 0.0

    actual_errors = 100.0 - actual
    return (actual_errors / error_budget) * 100


def burn_rate(
    events: Iterable[Event],
    target: float,
    window: timedelta,
) -> float:
    """Compute the burn rate over the given window.

    Burn rate of 1.0 means we are exactly on pace to exhaust the budget by
    the end of the window. Burn rate > 1 means we are burning faster than
    sustainable. Burn rate < 1 is healthy.
    """
    events_list = list(events)
    if not events_list:
        return 0.0

    actual = availability(events_list)
    consumed = error_budget_consumed(actual, target)

    # Fraction of the window that has elapsed, based on first/last events
    first = min(e.timestamp for e in events_list)
    last = max(e.timestamp for e in events_list)
    elapsed = last - first
    window_fraction = elapsed.total_seconds() / window.total_seconds()

    if window_fraction == 0:
        return 0.0

    return (consumed / 100.0) / window_fraction


# NEW: helper to project when the error budget will be exhausted at the
# current burn rate. Useful for paging on "budget exhausted in <2h".
def time_to_budget_exhaustion(
    events: list[Event],
    target: float,
    window: timedelta,
) -> timedelta:
    """Return how long until the error budget is fully consumed at the
    current burn rate. Returns ``timedelta.max`` if not burning."""
    br = burn_rate(events, target, window)
    if br <= 0:
        return timedelta.max

    actual = availability(events)
    consumed_pct = error_budget_consumed(actual, target)
    remaining_pct = 100 - consumed_pct
    if remaining_pct <= 0:
        return timedelta(0)

    # At burn rate `br`, we consume 1 window worth of budget every (1/br) windows.
    # So time remaining is (remaining_pct / 100) * window / br
    return timedelta(
        seconds=(remaining_pct / 100) * window.total_seconds() / br
    )


# NEW: convenience constructor for the "last N minutes" window
def events_in_last(
    events: list[Event],
    minutes: int,
) -> list[Event]:
    """Filter events to the last N minutes from now."""
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    return [e for e in events if e.timestamp > cutoff]


def report(
    events: list[Event],
    target: float,
    window: timedelta,
) -> SLOReport:
    """Build a full SLO report for the given events and window."""
    if not events:
        # Empty window — treat as fully healthy
        now = datetime.utcnow()
        return SLOReport(
            target=target,
            actual=100.0,
            events_total=0,
            events_good=0,
            events_bad=0,
            error_budget_consumed_pct=0.0,
            burn_rate=0.0,
            window_start=now - window,
            window_end=now,
        )

    actual = availability(events)
    good = sum(1 for e in events if e.good)
    bad = len(events) - good
    consumed = error_budget_consumed(actual, target)
    br = burn_rate(events, target, window)

    return SLOReport(
        target=target,
        actual=actual,
        events_total=len(events),
        events_good=good,
        events_bad=bad,
        error_budget_consumed_pct=consumed,
        burn_rate=br,
        window_start=min(e.timestamp for e in events),
        window_end=max(e.timestamp for e in events),
    )
