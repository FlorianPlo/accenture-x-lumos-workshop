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
