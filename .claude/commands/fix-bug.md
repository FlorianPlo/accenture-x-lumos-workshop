---
description: Resolve one bug report end-to-end (reproduce, root cause, fix, tests, draft PR)
argument-hint: <issues/BUG-xxx.md | GitHub issue number>
---

Resolve this bug report: $ARGUMENTS

Follow `CLAUDE.md` and the procedure in `.claude/agent/bugfix-workflow.md` exactly:
read the wiki, CONTRIBUTING.md and CHANGELOG.md first, run pytest before and after,
write the failing regression test first, fix the root cause minimally in the domain module,
update CHANGELOG.md, and open a **draft** PR from `fix/<ticket-id>` whose description
follows `.github/pull_request_template.md`. Never push to `main`.
