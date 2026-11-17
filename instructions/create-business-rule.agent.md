---
name: create-business-rule
description: Creates a versioned business-rule assertion (SQL that must return zero rows, or a defined expected result) from a template for the QA run.
---

# Create Business Rule

Create a business-rule assertion for the DB migration QA tool (FR-4.5, backlog tasks 2.10 and 5.1).

- **Input format**
  + Rule name and one-sentence business meaning (for example, "every active account has an owner").
  + Rule owner (user ID or team).
  + SQL query text, written against the target PostgreSQL schema.
  + Expected result: zero rows (default), or a defined result such as a single row with a specific count.
  + Version number, starting at `1` for a new rule.
- **Processing steps**
  + Copy the rule template file from backlog task 2.10 and fill in the fields.
  + Assign a unique rule ID. Check existing IDs first.
  + Verify the SQL is a single read-only `SELECT` statement (or `WITH ... SELECT`). Reject any other statement.
  + Run the SQL against a disposable test database with a passing fixture (expects zero rows) and a failing fixture (returns rows). Confirm both outcomes match the expected result.
  + Store the rule with `id`, `name`, `sql`, `expected_result`, `owner_id`, and `version`.
  + If a rule with the same ID already exists and the SQL or expected result changes, increment `version`. Do not overwrite the old version.
  + Add a test that a rule returning rows fails and a rule returning none passes (backlog task 2.10).
- **Output format**
  + Stored rule record: `id`, `name`, `sql`, `expected_result`, `owner_id`, `version`.
  + Run result per rule: pass or fail, the rule ID and version used, and the row count returned (count only, never row values).
- **Constraints**
  + Apply the shared guardrails in `./instructions/enforce-qa-guardrails.agent.md`.
  + The SQL must be a single `SELECT` or `WITH ... SELECT` statement; reject all others.
  + Every run records the rule version it used.
  + Do not change the rule's owner without approval from the existing owner.
