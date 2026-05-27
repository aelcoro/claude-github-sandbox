"""Alert grouping and deduplication helpers.

Tiny utilities to take a stream of raw alerts and collapse them into
unique incidents based on a fingerprint (service + alert name + a hash
of the normalised message).

This is intentionally small — the goal is to demonstrate the shape, not
to be a full alert manager.
"""
from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


_RE_UUID = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
_RE_NUMS = re.compile(r"\b\d+\b")


@dataclass
class Alert:
    timestamp: datetime
    service: str
    name: str
    message: str
    severity: str = "warning"


@dataclass
class AlertGroup:
    fingerprint: str
    service: str
    name: str
    severity: str
    first_seen: datetime
    last_seen: datetime
    count: int
    sample_messages: list[str] = field(default_factory=list)


def _normalise(message: str) -> str:
    """Strip volatile bits so alerts with different request IDs collapse."""
    s = _RE_UUID.sub("<uuid>", message)
    s = _RE_NUMS.sub("<n>", s)
    return s.strip().lower()


def fingerprint(alert: Alert) -> str:
    """Stable identifier for grouping. Two alerts with the same
    fingerprint should be treated as the same incident."""
    payload = f"{alert.service}|{alert.name}|{_normalise(alert.message)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def group_alerts(alerts: Iterable[Alert]) -> list[AlertGroup]:
    """Group a list of alerts by fingerprint.

    Returns groups sorted by ``last_seen`` descending so the most recent
    incidents float to the top.
    """
    buckets: dict[str, list[Alert]] = defaultdict(list)
    for alert in alerts:
        buckets[fingerprint(alert)].append(alert)

    groups: list[AlertGroup] = []
    for fp, items in buckets.items():
        items.sort(key=lambda a: a.timestamp)
        groups.append(
            AlertGroup(
                fingerprint=fp,
                service=items[0].service,
                name=items[0].name,
                severity=items[0].severity,
                first_seen=items[0].timestamp,
                last_seen=items[-1].timestamp,
                count=len(items),
                sample_messages=[a.message for a in items[:3]],
            )
        )

    groups.sort(key=lambda g: g.last_seen, reverse=True)
    return groups
