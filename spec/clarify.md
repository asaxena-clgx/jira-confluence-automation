# Spec Review: DB Migration QA Automation Tool

**Reviewed files**:
- [specification.md](/Users/akash_saxena1/Desktop/hello-genai/spec/specification.md)
- [constitution.md](/Users/akash_saxena1/Desktop/hello-genai/spec/constitution.md)

**Reviewer role**: Senior developer, pre-plan review
**Purpose**: Identify what must be resolved before `/speckit.plan`. Each item is a candidate for `/speckit.clarify`.

## Summary

The spec is well structured and covers its requirements thoroughly. Five issues block planning:

1. The constitution governs a different project (Jira/Confluence automation). It cannot be checked against this spec.
2. The spec never says which database the post-execution checks run against: the sandbox, or the real target.
3. Nothing enforces the approval gate outside the tool, even though SC-002 says no run reaches production without approval.
4. "Mandatory" check status and the Warning result are undefined, so the approval rule cannot be implemented.
5. Concurrent runs (NFR-6) have no rule for sharing one sandbox.

Priority key: **P0** blocks planning. **P1** must be resolved before implementation of the affected story. **P2** can be resolved during planning or later.

---

## 1. Contradictions

| ID | Priority | Where | Issue | Suggested resolution |
|---|---|---|---|---|
| C-1 | P0 | [constitution.md](/Users/akash_saxena1/Desktop/hello-genai/spec/constitution.md) vs [specification.md](/Users/akash_saxena1/Desktop/hello-genai/spec/specification.md) | The constitution is titled and scoped to "Jira/Confluence Automation". The spec is an Oracle-to-PostgreSQL migration QA tool. Constitution Sections 2.3, 2.4, 2.5 and 5 are Atlassian-specific and do not apply. Section 6 requires a "Constitution Check" that cannot be done meaningfully. | Confirm which project this is. Then either rewrite the constitution for the migration tool, or write a separate constitution for the Jira/Confluence project. |
| C-2 | P0 | Constitution §1 vs spec Assumption 8 | Constitution: React 18 + Vite, Express, PostgreSQL 15 in Docker. Spec: React + TypeScript (no Vite), Express *or* Fastify (undecided), Node/TypeScript CLI. Constitution also allows JavaScript or TypeScript, while the spec requires TypeScript. | Once C-1 is settled, align the framework list. Make the frontend build tool and backend framework explicit. |
| C-3 | P0 | Constitution §2.6 and §4 vs spec NFR-9 | Constitution requires `docker compose up` to start the whole local environment with PostgreSQL 15. The spec puts the tool on an internal VM or server with no mention of Docker or PG version. The constitution's rule that tests run against Dockerized PG 15 would not cover Oracle, which the spec requires. | Decide whether the metadata store and local dev environment use Docker. Specify the PostgreSQL version of the metadata store and whether Oracle has a Docker-based test double. |
| C-4 | P0 | FR-1.2, FR-1.3, FR-3, FR-4 (esp. FR-4.4), Story 3 | FR-1.2 says the target is read-only. FR-3.1 runs scripts only in the sandbox. FR-4.4 says checks run "on the target". Story 3 says the tool compares Oracle source with "PostgreSQL target". It is unclear whether the target in comparisons is the sandbox (after scripts run) or the real target (which scripts never touch). | Define the comparison pair explicitly: Oracle source versus sandbox after execution. Show this in the run lifecycle. Restate FR-4 in those terms. |
| C-5 | P1 | User Story 3, scenario 3 vs NFR-4 | US3 attaches "returned rows" as evidence for failed business-rule assertions. NFR-4 says reports should avoid row-level values unless needed as evidence, and store counts, hashes, and identifiers. The exception is undefined. | Define a rule for when row values may be stored (for example, masked data only, capped row count, or hashes only), and add it to NFR-4. |
| C-6 | P1 | Run lifecycle vs User Story 1 | The lifecycle is `Draft -> Validated -> Sandbox Executed`, so validation is a prerequisite. FR-2 does not say validation blocks execution. The edge case about changed scripts assumes this, but the rule is not stated. | State in FR-3 that a run must be `Validated` before execution, and that failed validation blocks execution unless overridden. |
| C-7 | P1 | Lifecycle vs FR-4 | The lifecycle has `Sandbox Executed -> Checked`, but FR-4.7 (test suites) runs against the "lower environment", which is not the sandbox. The spec does not say whether `Checked` needs the lower environment and sandbox both. | Specify which environment each check uses, and whether a run can reach `Checked` if one is unavailable. |
| C-8 | P2 | FR-7.5 "immutable once signed off" vs US7 scenario 2 | The spec says reports are immutable and that changes are refused. It does not say how a real error found after sign-off is corrected. | Define a re-sign-off or amendment process, and who can trigger it. |

---

## 2. Gaps (missing requirements)

| ID | Priority | Area | What is missing |
|---|---|---|---|
| G-1 | P0 | Approval enforcement | SC-002 says no run reaches production without QA report and approval. The tool never deploys to production, so nothing enforces this. Define what the tool outputs (for example, a signed artifact or status API), and whether anything downstream checks it. Otherwise SC-002 cannot be verified. |
| G-2 | P0 | Check status semantics | FR-4.8 defines Pass, Fail, Warning, and Error. None is defined in terms of whether it blocks approval. Define each status and its effect on FR-6.2. |
| G-3 | P0 | "Mandatory" checks | FR-6.2 depends on mandatory checks, but the spec does not say which checks are mandatory, whether this is per check or per run, or who sets it. |
| G-4 | P0 | Concurrency | NFR-6 allows "a small number of concurrent runs", but two runs cannot safely share one sandbox. No locking, queueing, or per-run sandbox rule exists. |
| G-5 | P1 | Sandbox data seeding and reset | FR-3.4 requires reset or re-seed. The seed source, how the sandbox is loaded with data that mirrors Oracle source, and how long a reset takes are all undefined. |
| G-6 | P1 | Run versioning | Story 4 and FR-5.2 say runs are "versioned", and the edge case refers to run definitions changing after sign-off. The spec does not say what increments a version, whether a re-run creates a new run or a new version of the same run, or how old versions are kept. |
| G-7 | P1 | Migration phases | Story 6 and FR-7.1 refer to "sign-off status per migration phase". No entity or requirement defines phases. (The Section 8 delivery phases of the tool are a different thing.) |
| G-8 | P1 | Roles and permissions | Section 3 of the source spec lists a QA engineer role (define business-rule assertions, review failed checks). FR-9.2 names only manager and engineer. Permissions for the QA role are missing. Who may create, edit, or approve business rules (Open Question 3) is also unassigned. |
| G-9 | P1 | Approver assignment | FR-6.1 says "the manager", but the spec does not say how the approver is determined for a run: a named person, a team, a delegate, or any user with the manager role. Self-approval is open (Open Question 9). |
| G-10 | P1 | Authorization source | FR-9.1 and FR-9.2 do not say where roles come from: SSO groups, claims, or a local table in the User entity. |
| G-11 | P1 | Access exceptions | FR-9.2 says engineers are scoped to their own runs "by default", implying an override exists. No override mechanism is defined. |
| G-12 | P1 | Oracle source access | The spec does not say how the source is read: Oracle client requirements, network path, which schemas are in scope, and whether a read-only account can run the row-count and checksum queries at scale. |
| G-13 | P1 | Script inventory and ordering | A run is a set of scripts (FR-5.2), but the spec does not define script ordering, dependencies between scripts, or how a script is linked to a version (only a hash is stored). |
| G-14 | P1 | Cancellation and progress | Long-running runs (NFR-5) have no requirement for cancellation, progress reporting, or partial results. |
| G-15 | P1 | Mapping table ownership | FR-2.3 and FR-4.3 depend on an "approved mapping table". No owner, approval process, or location is defined. |
| G-16 | P1 | Threshold definition | FR-4.6 and Story 3 scenario 4 use a "configurable threshold". The spec does not say whether it is absolute (ms) or relative (percent slower than source), or where it is configured. |
| G-17 | P2 | Retention | No retention rules for runs, evidence, reports, or audit logs. Relevant for compliance and storage. |
| G-18 | P2 | Backup and recovery | NFR-7 accepts business-hours availability but gives no backup, RPO, or RTO for the metadata store. |
| G-19 | P2 | Audit scope | FR-9.3 lists trigger, approve, and export actions. US2 scenario 1 also requires logging refused execution attempts, and NFR-8 requires logging "every run". The list is not consistent. Audit log immutability and retention are also undefined (the AuditLog entity has no field for them). |
| G-20 | P2 | Tasks entity | FR-7.2 shows "tasks" for each engineer, but "task" is not defined in the spec or the data model. |
| G-21 | P2 | CLI behavior | The CLI is a required interface (FR-5.1) but its output format, exit codes, and authentication (SSO for CLI users) are not specified. |
| G-22 | P2 | Report content | FR-7.3 lists sections of the sign-off report, but the spec does not define the layout, the PDF template, or the CSV schema. |
| G-23 | P2 | Encryption detail | NFR-3 requires data at rest encryption. Key management and ownership are undefined. |
| G-24 | P2 | Script changes after validation | The edge case says the run must detect changes via the script hash, but does not say whether a changed script invalidates only that script or the whole run. |
| G-25 | P2 | Observability | No requirements for application logs, metrics, health checks, or alerting. |
| G-26 | P2 | Time zones and timestamps | Timestamps are required throughout, but the time zone (UTC or local) is not stated. |
| G-27 | P2 | Data model gaps | The data model lacks Phase, Team/engineer assignment, Sandbox state, Threshold, Mapping table, and Report template entities that the requirements imply. |
| G-28 | P2 | Success measurement | SC-001 requires a baseline that has not been measured. SC-006 "without manual data correction" is not defined. |

---

## 3. Unclear requirements

| ID | Requirement | Problem | Clarifying question |
|---|---|---|---|
| U-1 | FR-1.4 | "a secrets manager or environment-injected secret store" leaves the choice open. | Which secret store is approved for the internal VM? |
| U-2 | FR-2.1 | "Parse and lint ... PL/SQL" covers a large grammar. The spec does not say which PL/SQL objects are in scope (packages, triggers, functions, procedures, types). | Which PL/SQL object types must be parsed for MVP? |
| U-3 | FR-2.2 | "Oracle-specific syntax that does not run on PostgreSQL" has no rule set defined. | Who owns the initial rule set, and where is it stored? |
| U-4 | FR-3.3 | "Stop execution on first error by default" does not say whether a failed script leaves the sandbox in a partial state, or whether a reset is automatic. | Should the sandbox auto-reset after a failed run? |
| U-5 | FR-4.1 | "Full comparison by default" does not say whether a comparison result of "match" is needed for each table, or whether a warning is raised for tables with zero rows. | What counts as a match for an empty table? |
| U-6 | FR-4.2 | "Schema diff" does not say whether differences are expected (for example, Oracle `NUMBER` mapping to PostgreSQL types) or are always failures. | Is a schema diff a Fail, or a Warning when the difference is an approved mapping? |
| U-7 | FR-4.4 | "Null, PK, FK, and constraint checks on the target" does not say whether checks compare against the source or only check the target against its own constraints. | Are these checks absolute (for example, no NULL in a NOT NULL column) or comparative with the source? |
| U-8 | FR-4.5 | "Stored and versioned" does not say who may change a rule, or whether a changed rule invalidates past results. | Do results from an older rule version remain valid? |
| U-9 | FR-4.7 | "Application and regression test suites" does not say which application, which framework, or how suites are invoked (Open Question 5). | Which test suites are in scope for the MVP pilot? |
| U-10 | FR-5.1 | "Trigger a test run manually" does not say whether a run may be triggered by any user or only by the owner, or whether an engineer may trigger a run owned by someone else. | Who may trigger runs owned by others? |
| U-11 | FR-6.2 | "Explicitly accepted known failures with a recorded reason" does not say whether acceptance is per check or per run, or whether acceptance expires. | Are accepted failures per check and permanent for that run? |
| U-12 | FR-7.1 | "Pass/fail rates" are undefined in time window and denominator. | What time window and scope do the rates cover? |
| U-13 | FR-7.4 | The export format for CSV and PDF is not specified beyond "export". | Does the CSV export contain the same fields as the PDF? |
| U-14 | FR-8.1 | "A form that can be attached to Jira tickets" does not define size limits or format (Open Question 8). | What is the maximum attachment size, and must PDF or CSV be used? |
| U-15 | FR-8.3 | "Jira ticket reference field ... entered manually" does not define format validation. | Should the reference be validated against a project key pattern? |
| U-16 | NFR-1 | "The sandbox is isolated from production by network and credentials" does not say how isolation is verified. | Is isolation verified by a test, an audit, or a checklist? |
| U-17 | NFR-5 | "Within an agreed window" has no value. This is marked NEEDS CLARIFICATION. | What is the window, and who agrees it? |
| U-18 | NFR-6 | "A small number of concurrent runs" is not quantified. | What number of concurrent runs is the maximum? |
| U-19 | Environment entity | `is_production` is "always false" but the sandbox, source, target, and lower environment all need explicit flags. The entity has four types, but FR-3.1 says "marked as sandbox" and does not say what marking is. | How is the sandbox flag set and protected from change? |
| U-20 | Key Entities: Approval | `decision` values are not listed. | What decision values are allowed (approve, reject, accept-with-failures)? |
| U-21 | Story 6 | "Pass/fail rates, open failures" depends on undefined "open failure" (G-7 and G-19 apply). | Define open failure: unresolved failure in an active run, or any failure not yet accepted? |
| U-22 | Story 8 scenario 1 | "Redirected to sign in" does not say what happens when the SSO session expires during a long run. | Does a running job continue when the user's session expires? |
| U-23 | SC-003 | "Verified by access tests for every role" depends on roles that are not fully defined (G-8). | Which roles are tested? |
| U-24 | SC-005 | "Refuses 100% of execution attempts" against non-sandbox profiles needs a list of attempt types to test. | Which negative test cases define 100% coverage? |

---

## 4. Constitution-specific gaps

These apply once C-1 is resolved.

| ID | Constitution section | Gap |
|---|---|---|
| K-1 | §1 | No database for Oracle, no Oracle driver, and no PDF or report library are listed. The spec needs all three. |
| K-2 | §2.3 | Tests must run against the Dockerized PG 15 instance. The spec has no equivalent for Oracle test data. |
| K-3 | §2.4 | Secrets rules cover Atlassian credentials only. Oracle and PostgreSQL profile credentials (FR-1.4) are not covered. |
| K-4 | §2.5 | Idempotency and rate-limit rules are written for Jira/Confluence. Equivalent rules for sandbox execution (for example, re-running a script) are needed. |
| K-5 | §5 | Out-of-scope rules forbid Atlassian production writes. They do not cover production Oracle or PostgreSQL writes, which the spec forbids via NFR-1. |
| K-6 | §6 | The Constitution Check requires compliance with §§1 to 4. For the migration tool, there is no test that verifies the approval gate or the sandbox guard. Add one. |

---

## 5. Recommended clarification questions (in priority order)

1. **Project scope (C-1, C-2):** Is the constitution meant for the Jira/Confluence project or the migration tool? If the migration tool, should the stack stay as in the spec?
2. **Comparison target (C-4):** Are post-execution checks run against the sandbox after scripts run, or against the real PostgreSQL target?
3. **Approval enforcement (G-1):** What, if anything, outside the tool must check that approval exists before a migration proceeds?
4. **Check statuses (G-2, G-3):** Which checks are mandatory, and does Warning block approval?
5. **Sandbox sharing (G-4):** Can two runs share a sandbox, or must each run get its own?
6. **Approver and roles (G-8, G-9, G-10):** Who can approve, who can define rules, and where do roles come from?
7. **Run versioning and sign-off amendments (G-6, C-8):** What does a version mean, and how is a signed-off error corrected?
8. **Oracle access (G-12):** Which schemas are in scope, and is there a read-only account with the needed privileges?
9. **Evidence policy (C-5):** Which row-level values, if any, may be stored in evidence?
10. **Lower environment and test suites (C-7, U-9):** Which application and test framework are used, and in which environment?

---

## 6. Next steps

- Resolve C-1 and C-2 before any further planning. Everything in the constitution depends on them.
- Answer questions 2 to 5 above, then update [specification.md](/Users/akash_saxena1/Desktop/hello-genai/spec/specification.md) and mark each resolved `[NEEDS CLARIFICATION]` item as answered.
- Re-run this review after the spec is updated.
