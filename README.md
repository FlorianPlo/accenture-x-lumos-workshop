# Accenture × Lumos Workshop: Bug Fixing Agent

A case study from a workshop held by **Accenture** with the **Lumos** student organization
in November 2026. We took on **Case 1, "Bug Fixing Agent"**, and built an AI agent that
resolves reported bugs in a codebase on its own and hands every fix to a human for review.

## The problem

The client's development team loses valuable time on recurring bugs. The challenge was to
build an AI agent that resolves a reported bug in a given codebase **autonomously**. The agent should:

- analyze the bug report and locate the root cause,
- use the repository's own context: wiki, code, conventions and tests,
- implement a fix that follows the team's coding standards,
- validate the fix with existing or new tests.

The judging criteria were a **correct, working fix**, **smart use of the repository context**
and **transparent agent reasoning with human review**.

The codebase is **WattWise Billing**, a small Python app that creates monthly electricity
invoices for a fictional energy supplier (meter readings → consumption → tariff → invoice).
It came with three open bug reports.

## Our solution

We built the agent with **Claude Code running in GitHub Actions**. It lives entirely in this
repository and needs no external server.

```
GitHub issue opened ──▶ Bug Fixing Agent (GitHub Actions + Claude Code)
                          │  reads CLAUDE.md → wiki → CONTRIBUTING → CHANGELOG → code & tests
                          │  reproduces the bug → failing test → root cause → minimal fix
                          ▼
                        Draft PR on fix/<ticket-id>, with the full reasoning log
                          ▼
                        CI (pytest) ──▶ human review (@claude for changes) ──▶ merge
```

- **Trigger:** someone opens a GitHub issue using the bug report template.
- **Repository context:** [`CLAUDE.md`](CLAUDE.md) tells the agent what to read and in which order.
  The wiki is the source of truth for business rules, and `CONTRIBUTING.md` sets the coding
  standards and the Definition of Done.
- **Procedure:** [`.claude/agent/bugfix-workflow.md`](.claude/agent/bugfix-workflow.md) is the
  team's own bug workflow turned into steps the agent follows. It writes a failing regression
  test first, then fixes the root cause in the domain module, then runs the full suite and
  updates the changelog.
- **Transparency:** every pull request follows
  [`.github/pull_request_template.md`](.github/pull_request_template.md). Each claim cites a
  file and line, a quoted wiki rule, a test, or command output. Risks and open business
  questions are flagged for the reviewer.
- **Guardrails:** the agent may only push to `fix/*` branches. Pushing to `main`,
  force-pushing and merging are blocked, and so are edits to the wiki, the data files and the
  workflows. Only repo members can trigger it, and a human always reviews and merges.

## Results

The agent resolved all three bug reports. Each one went from issue to draft PR in about
1.5 minutes, and each PR was reviewed and merged by a human.

| Ticket | Bug | Root cause the agent found | PR |
| --- | --- | --- | --- |
| BUG-142 | Billing run aborts for one customer | Meter counter rollover was rejected instead of handled as the wiki defines | [#2](../../pull/2) |
| BUG-158 | Base fee about 3% too low | Billing period counted 29 instead of 30 days (the last day was not counted) | [#4](../../pull/4) |
| BUG-151 | Bill jumps far more than consumption | Tiered tariff charged all kWh at the highest tier price, instead of each tier's price | [#6](../../pull/6) |

The test suite grew from 39 to 48 tests, and every fix passed CI.

## How to use it

| Action | What happens |
| --- | --- |
| Open an issue (template **Bug report**) | The agent fixes the bug and opens a draft PR |
| Add the label `agent-fix` to an issue | Re-runs the agent on that issue |
| Actions → *Bug Fixing Agent* → *Run workflow* | Runs the agent on a bug report file in `issues/` |
| Comment `@claude …` on an issue or PR | Claude follows up, e.g. on review feedback |

Setup: install the [Claude GitHub App](https://github.com/apps/claude) and add the secret
`CLAUDE_CODE_OAUTH_TOKEN` (created with `claude setup-token`).

## Running the app locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest                            # test suite
python -m wattwise serve                    # web UI on http://localhost:8000
python -m wattwise invoice C-1001 2026-11   # one invoice
python -m wattwise run 2026-11              # billing run for all customers
```

Requires Python 3.10+ and has no runtime dependencies.

| Path | Contents |
| --- | --- |
| `src/wattwise/` | Application code |
| `tests/` | pytest test suite |
| `data/` | Sample customers, meters and readings (Oct–Dec 2026) |
| `wiki/` | Business rules, tariffs, architecture, workflow |
| `issues/` | The original bug reports |
| `.github/`, `.claude/`, `CLAUDE.md` | The Bug Fixing Agent |

---

*The case and the WattWise Billing codebase were provided by Accenture for the workshop.
The agent setup was built by the Lumos team.*
