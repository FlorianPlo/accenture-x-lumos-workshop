# Contributing to WattWise Billing

These conventions apply to every change, including bug fixes. Reviewers will reject
pull requests that do not follow them.

## Business rules

- The **wiki is the source of truth** for business rules (`wiki/Billing-Rules.md`,
  `wiki/Tariffs.md`, `wiki/Meter-Readings.md`). If code and wiki disagree, the code is wrong.
- Do not change a business rule in the wiki without sign-off from the product owner.
  If you think a rule is wrong, raise it in the pull request; do not change it yourself.

## Code style

- Python 3.10+, full type hints on all public functions.
- Google-style docstrings on all public functions and classes (`Args:`, `Returns:`, `Raises:`).
- Keep functions small and side-effect free; I/O only in `repository.py`, `web.py` and `cli.py`.
- No business logic in the UI (`web.py`, `views.py`) or the CLI. Fix bugs in the domain modules.
- No new third-party dependencies without team approval.

## Money

- All monetary values are `decimal.Decimal`. **Never use `float` for money**, not even
  in intermediate steps.
- Build Decimals from strings or ints (`Decimal("0.19")`), never from floats.
- Round with `wattwise.money.round_eur` only. Do not call `round()` or `quantize()`
  in business code.
- Round **each invoice line once**, at the end of its calculation. Do not round intermediate
  results (e.g. a daily rate or a single tier).

## Errors

- Raise the domain exceptions from `wattwise/errors.py`, never bare `Exception`.
- Error messages name the affected entity (meter id, customer id) and the offending values.

## Tests

- Every change comes with tests. Every **bug fix** comes with at least one regression test
  that fails without the fix. Put the ticket id in a comment above the test:

  ```python
  # Regression test for BUG-123
  def test_energy_charge_handles_something() -> None:
      ...
  ```

- Test names: `test_<function>_<expected behaviour>`.
- Put the hand calculation for expected amounts in a comment (see `tests/test_tariff.py`).
- The full suite must pass: `pytest`.

## Changelog and commits

- Add a line to `CHANGELOG.md` under **Unreleased** for every user-visible change,
  with the ticket id.
- Commit messages follow Conventional Commits and end with the ticket id:
  `fix(meter): handle register rollover (BUG-123)`.
  Allowed types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.
- One ticket per pull request.

## Definition of done

- [ ] Root cause understood and described in the PR
- [ ] Fix follows the wiki rules and the conventions above
- [ ] Regression test added, full suite green
- [ ] CHANGELOG updated
- [ ] Reviewed by a second person
