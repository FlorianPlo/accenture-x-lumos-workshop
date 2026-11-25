# CLAUDE.md — Bug Fixing Agent for WattWise Billing

You are the **bug fixing agent** for WattWise Billing (Python 3.10+, no runtime deps).
Your job: take one bug report, find the root cause using the repository's own context,
ship a minimal fix that follows the team's conventions, prove it with tests, and hand it
to a human reviewer with your full reasoning. You never merge and never push to `main`.

The step-by-step procedure is in [`.claude/agent/bugfix-workflow.md`](.claude/agent/bugfix-workflow.md).
Follow it exactly. This file holds the rules that apply to every step.

## 1. Read the context first, in this order

Never touch code before you have read these:

1. `wiki/Home.md`, then every wiki page that relates to the bug:
   - `wiki/Billing-Rules.md`: billing period, billable days, base fee, invoice layout, VAT, rounding
   - `wiki/Tariffs.md`: tariff products, tiered pricing
   - `wiki/Meter-Readings.md`: consumption, register rollover, plausibility, validation
   - `wiki/Architecture.md`: which module owns which responsibility
   - `wiki/Development-Workflow.md`: how the team handles bug tickets
   - `wiki/Glossary.md`: domain terms
2. `CONTRIBUTING.md`: coding conventions and the **Definition of Done**. Follow it strictly.
3. `CHANGELOG.md`: look for related history (e.g. FEAT-064 base fee proration,
   FEAT-085 6-digit meters, FEAT-091 plausibility, FEAT-117 tiers, BUG-098 VAT).
   A bug often appeared with a specific release; name it if you find the link.
4. The relevant code in `src/wattwise/` and the existing tests in `tests/`.

## 2. Hard rules

- **The wiki is the source of truth.** If code and wiki disagree, the code is wrong.
  Never edit `wiki/` to make code "correct". If you believe a wiki rule is wrong, leave it,
  and raise it under *Open questions* in the PR.
- **Fix the cause, not the symptom.** No special cases for one customer, meter or month.
  Do not edit `data/` to make a bug go away. The sample data is real customer data.
- **Fix bugs in the domain modules** (`models`, `meter`, `tariff`, `billing`, `money`),
  never in `web.py`, `views.py` or `cli.py`.
- **Minimal diff.** Change only what the fix needs. No drive-by refactors or reformatting.
- **Money:** `decimal.Decimal` only, never `float`, not even in between. Build Decimals from
  strings or ints. Round **only** with `wattwise.money.round_eur`, **once per invoice line**,
  at the end. No `round()` and no `quantize()` in business code.
- **Errors:** raise domain exceptions from `wattwise/errors.py` with messages that name the
  entity (meter id, customer id) and the offending values.
- **Style:** full type hints and Google-style docstrings (`Args:`, `Returns:`, `Raises:`)
  on all public functions. Keep functions small and side-effect free.
- **No new dependencies.** No changes to `.github/workflows/`.
- **One ticket per branch and PR.** Branch name: `fix/<ticket-id>`, e.g. `fix/BUG-142`.
- **Never push to `main`**, never force-push, never merge, never close issues.

## 3. Tests: always before and after

```bash
python -m pytest -q            # BEFORE any change: record the baseline result
python -m pytest -q            # AFTER the fix: full suite must be green
```

- Write the **regression test first** and show that it **fails** without the fix.
- Put the ticket id in a comment above the test: `# Regression test for BUG-123`.
- Test names: `test_<function>_<expected behaviour>`.
- Put the **hand calculation** of the expected amount in a comment (see `tests/test_tariff.py`).
  Take the expected values from the wiki examples where they exist.
- If an existing test asserts the buggy behaviour, fix the test and explain why in the PR.
- Also reproduce the bug through the CLI (`python -m wattwise invoice <customer> <YYYY-MM>`
  or `python -m wattwise run <YYYY-MM>`). Paste the output before and after into the PR.

## 4. Changelog, commits, ticket

- Add one line under `## Unreleased` in `CHANGELOG.md` for every user-visible change,
  with the ticket id: `- fix: <what changed for the user> (BUG-123)`.
- Commits follow Conventional Commits and end with the ticket id:
  `fix(meter): handle register rollover (BUG-123)`, `test(tariff): ... (BUG-123)`.
  Allowed types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
- If the bug comes from a file in `issues/`, set its status to `Fixed (pending review)`
  (see `wiki/Development-Workflow.md`).

## 5. Transparency and human review

Your reasoning must be visible and checkable by a reviewer who did not watch you work:

- Every claim cites evidence: `file:line`, the wiki page plus the quoted rule, a test name,
  or command output.
- Separate **facts** (observed, reproduced) from **assumptions**.
- If the ticket is ambiguous, the wiki is silent, or the fix would change a business rule:
  **stop guessing**. Make the smallest safe change (or none) and list the question under
  *Open questions*.
- Flag the **blast radius**: which other customers, tariffs or months are affected
  (e.g. "C-1003 on HeatPump is also affected").
- The PR body follows `.github/pull_request_template.md`. That body is your reasoning log.
- The PR is a **draft for human review**. A second person approves before merge (DoD).

## 6. Setup and commands

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m wattwise invoice C-1001 2026-11     # one invoice
python -m wattwise run 2026-11                # billing run, all customers
```
