"""Tests for slo_calculator."""
from datetime import datetime, timedelta, timezone

import pytest

from src.slo_calculator import (
    Event,
    availability,
    burn_rate,
    error_budget_consumed,
    events_in_last,
    report,
    time_to_budget_exhaustion,
)


def _events(good: int, bad: int) -> list[Event]:
    """Build a small mixed list of events."""
    now = datetime(2026, 1, 1, 12, 0, 0)
    out = []
    for i in range(good):
        out.append(Event(timestamp=now + timedelta(minutes=i), good=True))
    for i in range(bad):
        out.append(Event(timestamp=now + timedelta(minutes=good + i), good=False))
    return out


class TestAvailability:
    def test_all_good_returns_100(self):
        assert availability(_events(10, 0)) == 100.0

    def test_all_bad_returns_0(self):
        assert availability(_events(0, 10)) == 0.0

    def test_mixed(self):
        assert availability(_events(9, 1)) == 90.0

    def test_empty_returns_100(self):
        """Empty event stream is treated as healthy."""
        assert availability([]) == 100.0


class TestErrorBudgetConsumed:
    def test_meeting_target_exactly_consumes_100pct(self):
        # 99.9% actual against 99.9% target → all budget spent
        assert error_budget_consumed(99.9, 99.9) == pytest.approx(100.0)

    def test_perfect_actual_consumes_0pct(self):
        assert error_budget_consumed(100.0, 99.9) == pytest.approx(0.0)

    def test_below_target_over_consumes(self):
        # 99.8% actual against 99.9% target → 200% consumed
        assert error_budget_consumed(99.8, 99.9) == pytest.approx(200.0)

    def test_target_100pct_does_not_divide_by_zero(self):
        # New guard: target=100% means no error budget at all
        assert error_budget_consumed(99.9, 100.0) == 0.0


class TestReport:
    def test_meeting_slo_flag(self):
        r = report(_events(99, 1), target=99.0, window=timedelta(hours=1))
        assert r.is_meeting_slo is True

    def test_budget_exhausted_flag(self):
        r = report(_events(50, 50), target=99.0, window=timedelta(hours=1))
        assert r.budget_exhausted is True

    def test_empty_events_returns_default(self):
        r = report([], target=99.0, window=timedelta(hours=1))
        assert r.events_total == 0
        assert r.actual == 100.0
        assert r.burn_rate == 0.0


class TestTimeToBudgetExhaustion:
    def test_no_burn_returns_max(self):
        events = _events(100, 0)
        result = time_to_budget_exhaustion(events, target=99.0, window=timedelta(hours=1))
        assert result == timedelta.max

    def test_active_burn_returns_positive(self):
        # 990 good, 5 bad on a 99% target — ~50% of budget consumed,
        # burning but not yet exhausted
        events = _events(990, 5)
        result = time_to_budget_exhaustion(events, target=99.0, window=timedelta(hours=1))
        # Result should be positive, finite, and not max (active burn)
        assert result > timedelta(0)
        assert result != timedelta.max

    def test_already_exhausted_returns_zero(self):
        # 50/50 split on a 99% target — budget already gone
        events = _events(50, 50)
        result = time_to_budget_exhaustion(events, target=99.0, window=timedelta(hours=1))
        assert result == timedelta(0)


class TestEventsInLast:
    def test_returns_recent_events_only(self):
        # Build events spanning the last 2 hours, anchored to "now"
        now = datetime.now(timezone.utc)
        events = [
            Event(timestamp=now - timedelta(minutes=10), good=True),
            Event(timestamp=now - timedelta(minutes=30), good=True),
            Event(timestamp=now - timedelta(minutes=90), good=False),  # outside window
            Event(timestamp=now - timedelta(minutes=120), good=False),  # outside window
        ]
        result = events_in_last(events, minutes=60)
        assert len(result) == 2
        # Both should be the recent ones
        assert all(e.timestamp > now - timedelta(minutes=60) for e in result)

    def test_empty_list_returns_empty(self):
        assert events_in_last([], minutes=60) == []

    def test_all_old_returns_empty(self):
        now = datetime.now(timezone.utc)
        events = [
            Event(timestamp=now - timedelta(hours=2), good=True),
            Event(timestamp=now - timedelta(hours=3), good=False),
        ]
        result = events_in_last(events, minutes=60)
        assert result == []
