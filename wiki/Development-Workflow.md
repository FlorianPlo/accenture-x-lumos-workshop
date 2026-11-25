# Development Workflow

## Handling a bug ticket

1. **Reproduce** the bug in the web UI (`python -m wattwise serve`) or the CLI with the sample data, then with a failing test.
2. **Find the root cause.** Compare the code to the business rules in the wiki. Fix the
   cause, not the symptom (no special cases for single customers or meters).
3. **Write a regression test** that fails before the fix (see [CONTRIBUTING](../CONTRIBUTING.md)).
4. **Fix** the code following the conventions.
5. **Run the full suite** (`python -m pytest`) and check the affected customer in the web UI.
6. **Update `CHANGELOG.md`** under *Unreleased*.
7. **Open a pull request** with: ticket id, root cause, fix, how it was tested.
   A second person reviews and approves before merge.

## Ticket format

Bug tickets live in `issues/` as Markdown files named `BUG-<id>-<slug>.md`.
When a ticket is fixed, set its status to `Fixed (pending review)` and add the PR link.
