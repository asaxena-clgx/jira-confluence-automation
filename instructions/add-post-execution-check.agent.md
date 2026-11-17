---
name: add-post-execution-check
description: Adds a post-execution check (row count, schema diff, constraints, performance, and similar) that implements the Check interface and registers without engine changes.
---

# Add Post-Execution Check

Add a check to the DB migration QA tool using the `Check` interface from backlog task 2.3.

- **Input format**
  + Check name and purpose (one sentence).
  + Source and target objects in scope: tables, columns, constraints, or queries.
  + Thresholds per table or per run, if any (FR-4.9). Default: exact match.
  + Mandatory or optional flag.
  + Fixture schema or data for tests (small, synthetic).
- **Processing steps**
  + Create one module per check in the checks package chosen in backlog task 1.1.
  + Implement `run(context) -> CheckResult`. Read connections, thresholds, and config only from `context`.
  + Use read-only connectors only. Do not open write sessions.
  + Compare source and target. Compute per-object differences, not row values.
  + Map the outcome to one status: `Pass`, `Fail`, `Warning`, or `Error`.
    + `Pass`: no difference, or difference within threshold.
    + `Warning`: difference beyond warning threshold but within fail threshold.
    + `Fail`: difference beyond fail threshold, or an expected constraint or object is missing.
    + `Error`: check could not run (connection failure, missing table in catalog query, timeout).
  + Register the check in the check registry. Do not edit the run engine.
  + Add tests: matching input (Pass), mismatch (Fail), missing object (Error), and threshold edge (Warning) when applicable.
  + Run the test subset for the new check only, then the full unit suite.
- **Output format**
  + `CheckResult` fields: `status`, `details` (JSON with counts and object names), `evidence_ref` (reference, not values), `check_id`, `created_at`.
  + Details contain counts, hashes, object names, and differences by category only.
- **Constraints**
  + Apply the shared guardrails in `./instructions/enforce-qa-guardrails.agent.md`.
  + Do not hard-code thresholds; read them from configuration (FR-4.9).
  + Do not modify the run engine or other checks when adding this check (NFR-10).
  + Use the same `CheckResult` model as existing checks; do not add fields for one check only.
