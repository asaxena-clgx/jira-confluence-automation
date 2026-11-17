---
name: enforce-qa-guardrails
description: Shared safety and data-handling rules for every DB migration QA check, lint rule, and business rule. Referenced by those instructions.
---

# Enforce QA Guardrails

Apply these rules to every check, lint rule, business rule, fixture, and sample.

- Read only: use read-only connectors for source and target (FR-3.1, NFR-1).
- Never run DDL, DML, or session-changing SQL against any database from these workflows.
- Never execute migration scripts from these workflows. Script execution goes only through the sandbox guard (FR-3.1).
- Never store or print row-level values in details, reports, or results. Use counts, hashes, object names, and differences only (NFR-4).
- Never put credentials, tokens, or connection strings in rule, check, sample, or fixture files (FR-1.4, NFR-2).
- Use minimal synthetic fixtures and samples. Never use real migration data.
- Do not duplicate an existing check, rule, rule ID, or construct. Extend the existing one instead.
- Document every new check, lint rule, and business rule in the user documentation (backlog task 5.1).
