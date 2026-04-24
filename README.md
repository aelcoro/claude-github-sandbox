# claude-github-sandbox

A tiny Python playground to experiment with Claude + GitHub integrations. It contains a small calculator module, some string helpers, and a pytest suite so there's enough surface area to test features like code review, refactors, bug-fixing, and test generation.

## Project layout

```
claude-github-sandbox/
├── src/
│   ├── __init__.py
│   ├── calculator.py       # add, subtract, multiply, divide, average
│   └── string_utils.py     # reverse, is_palindrome, word_count
├── tests/
│   ├── test_calculator.py
│   └── test_string_utils.py
├── .gitignore
├── LICENSE                 # MIT
├── README.md
├── SETUP.md                # step-by-step push-to-GitHub + integration guide
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

All tests should pass out of the box.

## Things to try asking Claude

Once the repo is pushed to GitHub, these are fun starting prompts to exercise different capabilities:

- "Add a `power(a, b)` function to calculator.py with unit tests."
- "There's an intentional edge-case bug in `average()` — find and fix it."
- "Refactor `string_utils.py` to use better type hints and docstrings."
- "Open an issue describing a new feature: a command-line interface for the calculator."
- "Review this PR and suggest improvements." (after opening a PR)
- "Generate additional edge-case tests for `is_palindrome`."

## Next steps

See `SETUP.md` for instructions on creating the GitHub repository and connecting Claude.
