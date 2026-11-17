# Instructions Catalog

Each entry below is an instruction file with a one-line description. Optional sub-fields after `+`:
- **Keywords** — trigger words/phrases: if user's request matches, load this instruction.
- **Target** — file glob pattern: if current file or context matches, consider this instruction relevant.
- **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

---

- [`./create-status-report.agent.md`](./create-status-report.agent.md) — Generates a weekly status report in Markdown with accomplishments, blockers, and next-week plans.
  + Keywords: status report, weekly report, weekly status, accomplishments, blockers
- [`./creating-instructions.agent.md`](./creating-instructions.agent.md) — Creates or updates instruction files, skills, and IDE prompt/rule wrappers; bootstraps the instruction setup in a new project.
  + Keywords: create instruction, new instruction, update instruction, create skill, create prompt, bootstrap instructions, creating instructions
- [`./add-post-execution-check.agent.md`](./add-post-execution-check.agent.md) — Adds a post-execution check (row count, schema diff, constraints, performance) that implements the Check interface.
  + Keywords: add check, new check, post-execution check, row count check, schema diff check, performance check
  + Target: checks package
- [`./add-lint-rule.agent.md`](./add-lint-rule.agent.md) — Adds a pluggable Oracle-to-PostgreSQL lint rule with ID, severity, and pass/fail tests.
  + Keywords: add lint rule, new lint rule, Oracle syntax rule, linter rule
  + Target: linter rules folder
- [`./create-business-rule.agent.md`](./create-business-rule.agent.md) — Creates a versioned business-rule assertion (SQL that must return zero rows or a defined result).
  + Keywords: business rule, create rule, assertion, SQL rule, data rule
