---
name: add-lint-rule
description: Adds a pluggable Oracle-to-PostgreSQL lint rule that flags Oracle-only syntax in migration scripts, with ID, severity, and pass/fail tests.
---

# Add Lint Rule

Add a rule to the script linter from backlog task 2.8 (FR-2.1, FR-2.2, FR-2.4).

- **Input format**
  + Oracle construct to flag (for example `NVL`, `ROWNUM`, `CONNECT BY`, `DUAL`, `VARCHAR2`, `NUMBER`).
  + Rule purpose and the PostgreSQL replacement, if one exists.
  + Severity: `error`, `warning`, or `info`.
  + One failing script sample and one passing script sample for tests.
- **Processing steps**
  + Assign a unique rule ID using the project's ID scheme. Check existing rule IDs before choosing a new one.
  + Put the rule in the rules folder chosen for the linter. Do not edit the linter core.
  + Implement the rule against the parsed tree from the chosen parser (backlog task 2.8). Do not match raw text with regular expressions unless the parser cannot represent the construct; record that exception in the rule description.
  + Set rule ID, severity, and description as metadata on the rule.
  + Add two tests: the failing sample must produce exactly one finding for this rule ID with the correct line number; the passing sample must produce none.
  + Run the rule's tests, then the linter test suite.
  + Add the rule to the user documentation for lint rules (backlog task 5.1).
- **Output format**
  + Each finding reports: script name, line number, rule ID, severity, and a short message (FR-2.4).
  + Rule metadata: `id`, `severity`, `description`.
- **Constraints**
  + Rule IDs are unique and never reused after a rule is removed.
  + Each rule has exactly one severity.
  + The linter only reads scripts. It never executes them (FR-3.1).
  + Do not put database credentials or connection strings in rule files or samples.
  + Keep samples minimal: only the construct under test, no real migration data.
  + Do not add a rule that duplicates an existing rule's construct; update the existing rule instead.
