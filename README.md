# claude-github-sandbox

A small Python playground used to exercise Claude + GitHub Actions integrations
end-to-end. Contains a tiny SRE-flavoured toolkit (SLO calculation, alert
grouping) with a pytest suite, so there's enough surface area to test review,
refactor, bug-finding, and test-generation flows.

## Project layout

```
claude-github-sandbox/
├── .github/workflows/
│   └── claude-code-review.yml    # triggers Claude on every PR
├── src/
│   ├── __init__.py
│   ├── slo_calculator.py         # availability, error budget, burn rate
│   └── alert_grouping.py         # fingerprinting + deduplication
├── tests/
│   ├── test_slo_calculator.py
│   └── test_alert_grouping.py
├── LICENSE                       # MIT
├── README.md
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

All tests should pass out of the box.

## What the modules do

### `slo_calculator`
Tiny helpers for the standard SRE SLO math: availability from a list of good/bad
events, error-budget consumption, burn rate over a time window, and a combined
`report()` that puts it all together.

### `alert_grouping`
Takes a noisy stream of alerts and collapses duplicates by fingerprinting on
`service + name + normalised message` (UUIDs and numbers stripped). Useful when
many alerts of the same underlying incident arrive within a short window.

## Why this exists

This repo is the test bed for a Claude-powered GitHub Actions workflow that
reviews every PR. The code is small enough that reviews are fast to read, but
real enough that the reviewer has something substantive to say — SLO maths and
fingerprinting have plenty of edge cases.

## Things to try asking Claude in a PR

- "Review this PR for correctness and edge cases."
- "Suggest additional test cases."
- "Refactor `slo_calculator.report()` to avoid duplicating work between
  `availability` and `burn_rate`."
- "Look for off-by-one errors in the burn-rate calculation."
