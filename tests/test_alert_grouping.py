"""Tests for alert_grouping."""
from datetime import datetime, timedelta

from src.alert_grouping import Alert, fingerprint, group_alerts


def _alert(service: str, name: str, msg: str, minutes_ago: int = 0) -> Alert:
    return Alert(
        timestamp=datetime(2026, 1, 1, 12, 0, 0) - timedelta(minutes=minutes_ago),
        service=service,
        name=name,
        message=msg,
    )


class TestFingerprint:
    def test_same_alerts_have_same_fingerprint(self):
        a1 = _alert("api", "5xx", "Internal error on /orders")
        a2 = _alert("api", "5xx", "Internal error on /orders", minutes_ago=5)
        assert fingerprint(a1) == fingerprint(a2)

    def test_different_services_have_different_fingerprints(self):
        a1 = _alert("api", "5xx", "Internal error")
        a2 = _alert("auth", "5xx", "Internal error")
        assert fingerprint(a1) != fingerprint(a2)

    def test_uuids_are_normalised(self):
        a1 = _alert("api", "5xx", "Failed for 7a3f1c2e-9d4b-4f8a-b6e1-2c5a8d7e3f0a")
        a2 = _alert("api", "5xx", "Failed for 8b4e2d3f-0c5a-5e9b-c7f2-3d6b9e8f4a1b")
        assert fingerprint(a1) == fingerprint(a2)


class TestGrouping:
    def test_groups_collapse_duplicates(self):
        alerts = [
            _alert("api", "5xx", "Internal error", minutes_ago=10),
            _alert("api", "5xx", "Internal error", minutes_ago=5),
            _alert("api", "5xx", "Internal error", minutes_ago=2),
        ]
        groups = group_alerts(alerts)
        assert len(groups) == 1
        assert groups[0].count == 3

    def test_sorted_by_last_seen_desc(self):
        alerts = [
            _alert("api", "5xx", "Error A", minutes_ago=20),
            _alert("auth", "timeout", "Error B", minutes_ago=2),
        ]
        groups = group_alerts(alerts)
        assert groups[0].service == "auth"
        assert groups[1].service == "api"
