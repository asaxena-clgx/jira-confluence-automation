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
- [`./calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — Uses tools/compound_interest.py to calculate the final amount and interest earned on a compound-interest investment, and presents the results.
  + Keywords: compound interest, compounding, future value, interest earned, savings growth, compound_interest.py
  + Target: tools folder
- [`./use-row-count-diff.agent.md`](./use-row-count-diff.agent.md) — Uses tools/row_count_diff.py to compare source and target row counts for a table and report Pass, Warning, or Fail.
  + Keywords: row count, row counts, count mismatch, reconcile counts, table count comparison, row_count_diff.py
  + Target: tools folder
- [`./use-query-timing-regression.agent.md`](./use-query-timing-regression.agent.md) — Uses tools/query_timing_regression.py to compare source and target query timings by median and flag slowdowns as Warning or Fail.
  + Keywords: query regression, slower query, performance regression, timing comparison, query timing, query_timing_regression.py
  + Target: tools folder
- [`./enforce-qa-guardrails.agent.md`](./enforce-qa-guardrails.agent.md) — Shared read-only, data-handling, and documentation rules referenced by the check, lint rule, and business rule instructions.
  + Keywords: guardrails, read-only, data safety, shared rules, QA safety
