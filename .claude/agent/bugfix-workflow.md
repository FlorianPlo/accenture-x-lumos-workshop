# Bug fixing workflow (agent procedure)

Follow these steps in order. `CLAUDE.md` has the rules that apply to every step.
Post short progress notes as comments on the GitHub issue (if there is one) at the
milestones marked 💬, so that humans can follow your reasoning while you work.

## Step 0: Understand the ticket

- Read the bug report completely: the GitHub issue (`gh issue view <n> --comments`) or the
  file under `issues/`.
- Work out the **ticket id**:
  - a `BUG-<n>` id in the title or body → use it (e.g. `BUG-142`);
  - otherwise use `GH-<issue number>` (e.g. `GH-7`).
- Write down in your own words: affected customer(s), month, actual result, expected result.
- If the issue is not a bug report, is missing the information you need to reproduce it, or
  asks for a business rule change: 💬 comment what is missing, then stop. Do not open a PR.

## Step 1: Read the repository context

- `wiki/Home.md` → the wiki pages that relate to the ticket → `CONTRIBUTING.md` →
  `CHANGELOG.md` → the related source files and tests.
- Write down the **exact wiki rule(s)** that define the correct behaviour (quote them).

## Step 2: Baseline and reproduction

```bash
git switch -c fix/<ticket-id>
python -m pytest -q                       # baseline
python -m wattwise invoice <C-id> <YYYY-MM>   # or: python -m wattwise run <YYYY-MM>
```

- Reproduce the reported symptom on the CLI and keep the output.
- Write a **failing regression test** in the matching `tests/test_<module>.py`, with the
  ticket id comment and the hand calculation from the wiki.
- Run it and confirm it fails **for the reason in the ticket**.
- 💬 "Reproduced: <symptom>. Failing test: `<test name>`."

## Step 3: Root cause

- Trace the symptom through the data flow in `wiki/Architecture.md`
  (`service` → `billing.create_invoice` → `meter` / `tariff` / `models` / `money`).
- Find the line(s) where the code breaks the wiki rule. Record `file:line`, what the code does,
  and what the wiki says it must do.
- Check `CHANGELOG.md`: which release or ticket introduced or touched this code?
- Check why the existing tests did not catch it.
- Check the blast radius: run `python -m wattwise run` for the sample months
  (2026-10, 2026-11, 2026-12) and note which customers and amounts change.
- 💬 "Root cause: `<file:line>` does X; `wiki/<page>` requires Y."

## Step 4: Minimal fix

- Change only the domain module(s) that contain the root cause.
- Follow `CONTRIBUTING.md`: Decimal only, `round_eur` once per line, type hints,
  Google docstrings, domain exceptions.
- Keep the change minimal. No refactoring and no formatting churn.

## Step 5: Validate

```bash
python -m pytest -q                        # full suite green
python -m wattwise invoice <C-id> <YYYY-MM>   # symptom gone, numbers match the wiki
python -m wattwise run <YYYY-MM>           # no other customer broken
```

- Prove that the regression test fails without the fix and passes with it
  (`git stash` the source change, run the test, `git stash pop`).
- Add edge-case tests where the wiki defines them (e.g. tier boundaries, 6-digit meters,
  plausibility after rollover, February, leap years).

## Step 6: Changelog, ticket, commit

- `CHANGELOG.md`: one line under `## Unreleased` with the ticket id.
- If the ticket is a file in `issues/`: set the status to `Fixed (pending review)`.
- Commit with Conventional Commits, ending with the ticket id. Separate `test(...)` and
  `fix(...)` commits are welcome, because they show the test-first order.

## Step 7: Pull request (human review)

```bash
git push -u origin fix/<ticket-id>
gh pr create --draft --base main --head fix/<ticket-id> \
  --title "fix(<module>): <summary> (<ticket-id>)" --body-file <file>
```

- The body follows `.github/pull_request_template.md`. Fill every section with evidence.
  Write "None" rather than leaving a section out.
- Link the issue with `Fixes #<n>` when there is one. GitHub closes it only after a human merges.
- 💬 Comment the PR link on the issue.
- Never push to `main`. Never merge.
