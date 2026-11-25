# WattWise Billing

WattWise Billing creates the monthly electricity invoices for the household customers of
**WattWise Energy** (a fictional energy supplier). It reads meter readings, works out
consumption, applies the customer's tariff and prints the invoice.

## Quick start

```bash
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# macOS/Linux:          source .venv/bin/activate
python -m pip install -e ".[dev]"

python -m wattwise serve                    # web UI on http://localhost:8000
python -m pytest                            # run the test suite
```

The web UI shows the monthly billing run for all customers and an invoice page per
customer and month. Stop it with `Ctrl+C`.

Command line alternatives (same logic, no UI):

```bash
python -m wattwise invoice C-1001 2026-11   # print the invoice for one customer
python -m wattwise run 2026-11              # nightly batch job for all customers
```

Requires Python 3.10+. There are no runtime dependencies.

**Windows troubleshooting**
- `pytest` / `wattwise` "not recognized": the install step was skipped or the virtual
  environment is not active. Activate it and use `python -m pytest`.
- `Activate.ps1 cannot be loaded because running scripts is disabled`: run
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in the same terminal, then activate again.
- `python` opens the Microsoft Store: use `py` instead of `python`.

## Repository layout

| Path | Contents |
| --- | --- |
| `src/wattwise/` | Application code (see [wiki/Architecture.md](wiki/Architecture.md)) |
| `tests/` | pytest test suite |
| `data/` | Sample customers, meters and meter readings (Oct–Dec 2026) |
| `wiki/` | Team wiki: business rules, tariffs, architecture, workflow |
| `issues/` | Open bug reports |
| `CONTRIBUTING.md` | Coding conventions and definition of done |
| `CHANGELOG.md` | Release notes |

## Where to start

1. Read [wiki/Home.md](wiki/Home.md) for the domain.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing code.
3. Open bug reports are in [issues/](issues/).

## Bug Fixing Agent

Bugs are resolved by a Claude Code agent running in GitHub Actions
([`.github/workflows/claude-bugfix.yml`](.github/workflows/claude-bugfix.yml)).

| How to start it | What happens |
| --- | --- |
| Open a GitHub issue (template **Bug report**) | The agent reads the issue, works through the repo context and opens a **draft PR** from `fix/<ticket-id>` |
| Add the label `agent-fix` to an issue | Re-runs the agent on that issue |
| Actions → *Bug Fixing Agent* → *Run workflow* with `issues/BUG-….md` | Same, for a bug report file in `issues/` |
| Comment `@claude …` on an issue or PR | Claude follows up, e.g. on review feedback ([`claude.yml`](.github/workflows/claude.yml)) |

The agent's rules are in [`CLAUDE.md`](CLAUDE.md) and its step-by-step procedure in
[`.claude/agent/bugfix-workflow.md`](.claude/agent/bugfix-workflow.md). Every PR description
follows [`.github/pull_request_template.md`](.github/pull_request_template.md) and is the
agent's reasoning log. A human reviews and merges. CI ([`ci.yml`](.github/workflows/ci.yml))
runs pytest on every PR. Locally, run the same procedure with `/fix-bug issues/BUG-….md` in Claude Code.

Setup: install the Claude GitHub App on the repo and add the secret `CLAUDE_CODE_OAUTH_TOKEN`
(created with `claude setup-token`).
