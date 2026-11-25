## <ticket-id>: <one-line summary>

Fixes #<issue number> <!-- or: Bug report: issues/BUG-xxx-....md -->

> 🤖 Opened by the Bug Fixing Agent as a **draft for human review**. Every claim below
> cites a file:line, a wiki rule, a test or command output. Please verify before approving.

### 1. Bug summary
<!-- Affected customer(s) / month, actual vs. expected result, in 2–4 sentences. -->

### 2. Context used
<!-- Wiki pages, CONTRIBUTING sections, CHANGELOG entries and code/tests read, and what each contributed. -->
| Source | What it told me |
| --- | --- |
| `wiki/...` | |
| `CONTRIBUTING.md` | |
| `CHANGELOG.md` | |

### 3. Reproduction
<!-- CLI command + output BEFORE the fix; failing regression test name + failure message. -->

### 4. Root cause
- **Where:** `src/wattwise/<file>.py:<line>`
- **What the code does:**
- **What the wiki requires:** > quote from `wiki/<page>.md`
- **Since when / why tests missed it:** <!-- CHANGELOG release, gap in existing tests -->

### 5. Fix
<!-- What changed and why this is the minimal fix in the right module. -->

### 6. Tests
- [ ] Regression test `<test name>` (`# Regression test for <ticket-id>`) **fails without the fix**, passes with it
- [ ] Additional edge-case tests:
- [ ] Full suite before: `<n passed>`, after: `<n passed>`
- [ ] CLI output AFTER the fix (matches the wiki numbers):

### 7. Blast radius and risks
<!-- Other customers/tariffs/months affected, changed amounts, possible corrected invoices. -->

### 8. Open questions for the reviewer
<!-- Ambiguities, assumptions, suspected wiki issues. Write "None" if there are none. -->

### Definition of Done (CONTRIBUTING.md)
- [ ] Root cause understood and described in the PR
- [ ] Fix follows the wiki rules and the conventions
- [ ] Regression test added, full suite green
- [ ] CHANGELOG updated
- [ ] Reviewed by a second person ← **human reviewer**
