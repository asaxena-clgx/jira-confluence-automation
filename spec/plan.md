# Implementation Plan: DB Migration QA Automation Tool

**Based on**: [specification.md](/Users/akash_saxena1/Desktop/hello-genai/spec/specification.md)
**Review input**: [clarify.md](/Users/akash_saxena1/Desktop/hello-genai/spec/clarify.md)
**Constitution**: [constitution.md](/Users/akash_saxena1/Desktop/hello-genai/spec/constitution.md) (see Assumption A-1)
**Timeline**: 12 weeks (MVP complete at week 10, pilot weeks 11 to 12)
**Status**: Draft. Written on unresolved clarifications, which are listed as assumptions in Section 2.

---

## 1. Goals and Approach

Deliver the QA Automation Tool for the Oracle-to-PostgreSQL migration in phases. Each phase ends with a milestone that can be demonstrated and tested. The CLI comes first, then the UI and approval gate, then reporting.

Planning principles:

- **Safety first.** The sandbox guard (FR-3.1) and read-only connectors (FR-1.2) are built in the first phases that touch databases. They are not added later.
- **Audit from the start.** The audit log (FR-9.3, NFR-8) is built in Phase 1. Retrofitting it would miss events.
- **One engine, two interfaces.** The CLI and REST API call the same services (NFR-10 modular checks).
- **Pluggable checks.** Each check implements `run(context) -> CheckResult`, so new checks do not change the run engine.

---

## 2. Assumptions for Unresolved Clarifications

These assumptions cover the blocking items from [clarify.md](/Users/akash_saxena1/Desktop/hello-genai/spec/clarify.md). Each must be confirmed by the owner listed. If an assumption is wrong, the affected phase changes.

| ID | Question (clarify ref) | Assumed answer | Affected phases | Confirm by |
|---|---|---|---|---|
| A-1 | Project scope (C-1, C-2) | This plan is for the migration tool. The Jira/Confluence constitution is replaced by a migration-tool constitution in Phase 0. | 0 | End of week 1 |
| A-2 | Comparison target (C-4) | Post-execution checks compare Oracle source with the **sandbox after script execution**. The real PostgreSQL target stays read-only and is used only for pre-execution schema reads. | 1, 2, 3 | End of week 2 |
| A-3 | Check status semantics (G-2) | Fail and Error block approval. Warning does not block approval but is listed in the sign-off report. | 1, 5 | End of week 3 |
| A-4 | Mandatory checks (G-3) | All checks are mandatory unless the run definition marks them optional. Only mandatory checks gate approval. | 2, 5 | End of week 4 |
| A-5 | Sandbox sharing (G-4) | One active run per sandbox. Other runs queue. | 2, 5 | End of week 4 |
| A-6 | Approver (G-9) | Any user with the manager role can approve. Self-approval is not allowed. | 5 | End of week 8 |
| A-7 | Role source (G-10) | Roles come from SSO group claims, mapped to the `User.role` field on first login. | 5 | End of week 8 |
| A-8 | Run versioning (G-6) | Editing a run definition creates a new version. A re-run uses the same version and creates a new execution record. Sign-off freezes the version. | 2, 6 | End of week 6 |
| A-9 | Approval enforcement outside the tool (G-1) | The tool exposes approval status through its API and writes a signed sign-off artifact. Nothing else checks it in MVP. This is recorded as a known limitation. | 6, 7 | End of week 9 |
| A-10 | Oracle access (G-12) | A read-only Oracle account per schema is available. Oracle Instant Client or the thin driver is approved for the VM. | 0, 1 | End of week 1 |
| A-11 | Sandbox readiness (Open Q 4) | A PostgreSQL 15 sandbox mirroring the target schema is provisioned by week 3. Reset uses a snapshot of this sandbox. | 0, 2 | End of week 2 |
| A-12 | Stack (Spec Assumption 8) | TypeScript on Node.js LTS. Framework (Express or Fastify) is decided by ADR in Phase 0. | 0 | End of week 1 |

---

## 3. Phases and Milestones

| Milestone | Week | Phase | Name | Exit criteria |
|---|---|---|---|---|
| **M0** | 1 | 0 | Setup complete | ADRs accepted, repo and CI running, read-only accounts working, data volume measured, constitution rewritten. |
| **M1** | 3 | 1 | Core engine (CLI) | Connections tested, row count, schema diff, data type mapping, null and constraint checks run from the CLI. Audit log records each action. |
| **M2** | 5 | 2 | Script validation and sandbox | Scripts linted with findings. Sandbox execution runs with the guard. Refused attempts are audited. Runs are created and triggered from the CLI. |
| **M3** | 6 | 3 | Business rules and performance | Versioned business-rule assertions and performance regression checks produce Pass, Fail, Warning, or Error. |
| **M4** | 7 | 4 | Test suite runner | Lower-environment suites run, results and logs are attached to the run. |
| **M5** | 9 | 5 | API, UI, and approval gate | SSO login, RBAC, dashboards, per-engineer views, approval gate blocks runs correctly in the UI and API. |
| **M6** | 10 | 6 | Reporting and frozen sign-off | CSV and PDF exports match stored results. Signed-off reports are frozen. Jira reference field and export are in place. MVP feature complete. |
| **M7** | 12 | 7 | Pilot signed off | 2 to 3 engineers complete one run end to end. Runbook written. Go or no-go decision for the other engineers. |

---

## 4. Phase Details

### Phase 0: Setup (Week 1)

**Goal**: Remove blockers before building.

**Work**
- Write the migration-tool constitution, replacing the Jira/Confluence version (A-1). Use the existing structure: stack, principles, quality gates.
- Write ADRs: backend framework (A-12), PDF library, background job approach, secret store choice (U-1), metadata store version.
- Create the repository structure: `packages/core` (engine and checks), `packages/cli`, `packages/api`, `packages/web`, `packages/connectors`.
- Set up CI: lint, unit tests, integration tests with PostgreSQL in Docker.
- Spike: Oracle test database in Docker (Oracle Free image) for integration tests. If unavailable, use recorded fixtures and a shared test database.
- Provision read-only Oracle and PostgreSQL accounts (FR-1.2).
- Measure data volumes for the largest tables (feeds NFR-5 and the sampling decision).
- Request SSO client registration from the identity team (needed for Phase 5).

**Exit criteria (M0)**: ADRs accepted, CI green on an empty skeleton, read-only connections verified, data volumes recorded, constitution approved.

**Spec coverage**: FR-1.4 (choice), NFR-2, NFR-9 (setup), NFR-5 (measurement).

---

### Phase 1: Core Engine, CLI Only (Weeks 2 to 3)

**Goal**: Read-only comparison of Oracle source and sandbox, driven from the CLI.

**Work**
- Connector module for Oracle (read-only) and PostgreSQL. Connection profiles stored with a `profile_type` and `read_only` flag.
- Connection test command (FR-1.5).
- Check interface `run(context) -> CheckResult` and result model with Pass, Fail, Warning, Error (FR-4.8).
- Checks: row count, full comparison by default (FR-4.1); schema diff for tables, columns, types, indexes, constraints, sequences (FR-4.2); data type mapping against the approved table (FR-4.3); null, PK, FK, and constraint checks (FR-4.4).
- Per-table and per-run configuration and thresholds (FR-4.9).
- Evidence policy: store counts, hashes, and identifiers. Row values are not stored by default (NFR-4, resolves C-5).
- Audit log foundation: append-only table with user, action, target, timestamp, and payload hash (FR-9.3, NFR-8). CLI user identity is taken from the local OS user until SSO is available in Phase 5.
- Read-only guard: connectors reject any statement that is not a `SELECT`, and the connection profile must be `read_only` for source and target (NFR-1).

**Exit criteria (M1)**: All Phase 1 checks produce correct results on seeded test pairs, including seeded differences. Read-only guard tested with write attempts that must be refused.

**Spec coverage**: FR-1.1, FR-1.2, FR-1.5, FR-4.1 to FR-4.4, FR-4.8, FR-4.9, FR-9.3 (foundation), NFR-1, NFR-4, NFR-8 (foundation), NFR-10.

---

### Phase 2: Script Validation and Sandbox (Weeks 4 to 5)

**Goal**: Lint scripts, run them safely in the sandbox, and manage runs from the CLI.

**Work**
- Script linter for Oracle-to-PostgreSQL issues (FR-2.1, FR-2.2). Start with a rule set of about 30 common Oracle-specific constructs. Rules are stored as data, so engineers can add rules (risk mitigation).
- Mapping validation against the approved mapping table (FR-2.3). Mapping table owner and location to be confirmed (G-15).
- Findings with script name, line number, rule ID, and severity (FR-2.4, SC-004).
- Sandbox executor with a guard: refuses any profile not flagged as `sandbox` (FR-3.1, SC-005). Refused attempts are audit logged (US2 scenario 1).
- Record start time, end time, status, and output for each script (FR-3.2).
- Stop on first error by default, with a continue option (FR-3.3).
- Reset and re-seed from a sandbox snapshot (FR-3.4, G-5).
- Run model: `MigrationRun` with script list, check list, environment, and version (FR-5.2, A-8). Run triggering and re-run from the CLI (FR-5.1 CLI part, FR-5.3).
- Sandbox lock: one active run per sandbox, queued runs wait (A-5, G-4).
- Script hash stored at validation. Execution is blocked if the hash differs (edge case, G-24).

**Exit criteria (M2)**: Linter findings match a labeled corpus. Sandbox guard refuses 100% of non-sandbox attempts in negative tests (SC-005). Reset restores the snapshot. A run executes end to end from the CLI.

**Spec coverage**: FR-1.3, FR-2.1 to FR-2.4, FR-3.1 to FR-3.4, FR-5.1 (CLI), FR-5.2, FR-5.3, NFR-1 (sandbox isolation).

---

### Phase 3: Business Rules and Performance (Week 6)

**Goal**: User-defined checks and performance regression.

**Work**
- Business-rule assertions in SQL: must return zero rows, or match an expected result (FR-4.5).
- Versioning: a rule change creates a new version. Past results keep the version they ran with (U-8).
- Performance regression: a configured query set is timed on source and target. Threshold is relative (percent slower than source) with an absolute floor to avoid noise (FR-4.6, G-16).
- Results from the check engine (Pass, Fail, Warning, Error). Invalid or timed-out SQL is recorded as Error with the database message (edge case).

**Exit criteria (M3)**: Versioned rules run and record the version used. Performance check flags a seeded slow query and passes an unchanged one.

**Spec coverage**: FR-4.5, FR-4.6.

---

### Phase 4: Test Suite Runner (Week 7)

**Goal**: Run lower-environment regression suites and attach results.

**Work**
- Suite runner that invokes a configured command and captures exit code, pass/fail counts, and logs (FR-4.7).
- Retry policy, with retries and flake markers recorded (flakiness risk).
- Result attached to the run and to a per-test history.
- The suite framework is not yet confirmed (U-9). The runner uses a command template, so it works with any framework that reports exit code and output.

**Exit criteria (M4)**: A sample suite runs, results and logs are attached, and a flaky test is marked on its second run.

**Spec coverage**: FR-4.7.

---

### Phase 5: API, UI, and Approval Gate (Weeks 8 to 9)

**Goal**: The manager and engineers use the tool through the web UI, with SSO and the approval gate.

**Work**
- REST API for runs, checks, approvals, and reports, calling the same services as the CLI.
- SSO login (SAML or OIDC, decided in Phase 0), with role mapping (A-7, FR-9.1, FR-9.2).
- RBAC: engineers see their own runs, managers see all, QA engineers can edit business rules (G-8, G-11).
- Web UI (React + TypeScript): run triggering (FR-5.1 UI part), team dashboard (FR-7.1), per-engineer view (FR-7.2).
- Approval gate: a run cannot advance past `Checked` until approved. Fail and Error block approval, Warning does not (A-3, A-4). Approval records approver, timestamp, comment, and accepted failures with reasons (FR-6.1 to FR-6.3). Self-approval is blocked (A-6).
- Run state machine enforced in code: `Draft -> Validated -> Sandbox Executed -> Checked -> Pending Approval -> Approved -> Signed Off`. No skipping.
- Audit log extended to all trigger, approve, and export actions (FR-9.3).
- Load test for 10 concurrent users (NFR-6).

**Exit criteria (M5)**: Gate tests cover every transition, including blocked runs and self-approval. Engineer access tests confirm no cross-engineer access. Load test passes for 10 users.

**Spec coverage**: FR-5.1 (UI), FR-6.1 to FR-6.3, FR-7.1, FR-7.2, FR-9.1, FR-9.2, NFR-3 (TLS), NFR-6.

---

### Phase 6: Reporting and Frozen Sign-Off (Week 10)

**Goal**: Produce the sign-off report and freeze it.

**Work**
- Sign-off report generator from stored results only (FR-7.3). Sections: scope, checks, results, accepted risks, approval record.
- CSV export and PDF export from the same data model. CSV and PDF are tested for matching content (SC-007, U-13).
- Freeze on sign-off: stored results are immutable. Amendments create a new signed version, with approver and reason (C-8, FR-7.5).
- Checksum on the file, stored in `SignOffReport` (NFR-3).
- Jira reference field entered manually on each run (FR-8.3). Export is attachable to Jira manually (FR-8.1). No Jira writes (FR-8.2).
- Encryption at rest for the metadata store (NFR-3, G-23).
- Audit log for every export (NFR-8).

**Exit criteria (M6)**: CSV and PDF match on a test run. Frozen reports cannot be edited. Amendment path works. MVP feature complete.

**Spec coverage**: FR-7.3, FR-7.4, FR-7.5, FR-8.1 to FR-8.3, NFR-3 (at rest), NFR-8.

---

### Phase 7: Pilot and Hardening (Weeks 11 to 12)

**Goal**: Run the tool with real engineers and close the findings.

**Work**
- Pilot with 2 to 3 engineers (pilot selection, Open Q 7).
- Collect feedback and defects. Fix defects that block the pilot.
- Runbook: installation on the VM, backup and restore procedure (G-18), secret rotation, Oracle and PostgreSQL account setup, and how to add a lint rule.
- Measure SC-001 and SC-006 against the baseline measured in the pilot (G-28).
- Go or no-go decision for the other engineers.

**Exit criteria (M7)**: Pilot run signed off end to end. Runbook reviewed. No open Sev-1 defects.

**Spec coverage**: NFR-7, NFR-9, SC-001, SC-006.

---

## 5. Requirement Coverage

Every functional requirement is assigned to a phase. Requirements that span phases are listed in their completion phase.

| Requirement | Phase | Requirement | Phase |
|---|---|---|---|
| FR-1.1 | 1 | FR-4.9 | 1 |
| FR-1.2 | 1 | FR-5.1 | 2 (CLI), 5 (UI) |
| FR-1.3 | 2 | FR-5.2 | 2 |
| FR-1.4 | 0 (decision), 1 (implementation) | FR-5.3 | 2 |
| FR-1.5 | 1 | FR-6.1 to FR-6.3 | 5 |
| FR-2.1 to FR-2.4 | 2 | FR-7.1, FR-7.2 | 5 |
| FR-3.1 to FR-3.4 | 2 | FR-7.3 to FR-7.5 | 6 |
| FR-4.1 to FR-4.4 | 1 | FR-8.1 to FR-8.3 | 6 |
| FR-4.5, FR-4.6 | 3 | FR-9.1, FR-9.2 | 5 |
| FR-4.7 | 4 | FR-9.3 | 1 (foundation), 6 (complete) |
| FR-4.8 | 1 | | |

| Non-functional requirement | Phase |
|---|---|
| NFR-1 | 1 (read-only guard), 2 (sandbox isolation) |
| NFR-2 | 0 (repository and CI checks) |
| NFR-3 | 5 (TLS), 6 (encryption at rest) |
| NFR-4 | 1 |
| NFR-5 | 0 (measurement), 1 (window verified) |
| NFR-6 | 5 (load test) |
| NFR-7 | 7 |
| NFR-8 | 1 (foundation), 5 and 6 (complete) |
| NFR-9 | 0 (setup), 7 (runbook) |
| NFR-10 | 1 (interface), 3 (first new check added without engine changes) |

---

## 6. Test Strategy

| Level | Scope | Tooling | Example |
|---|---|---|---|
| Unit | Check logic, linter rules, state machine, guards | Vitest | Guard refuses a non-sandbox profile. |
| Integration | Connectors against real databases | Vitest with Docker PostgreSQL 15 and Oracle test container | Seeded row-count mismatch returns Fail. |
| Contract | CLI and API parity | Shared fixtures | Same run produces identical results from CLI and API. |
| End to end | Full run, approval, export | Playwright for UI | Engineer triggers, manager approves, PDF exported. |
| Security | Guard, RBAC, read-only, secrets | Targeted negative tests, code review of the guard | Engineer requests another engineer's run and is denied. |
| Load | 10 concurrent users | k6 or equivalent | Dashboard and run list under load (NFR-6). |

Negative tests for safety-critical behavior (sandbox guard, read-only connectors, approval gate) must exist before the feature is marked complete. These are listed in each phase exit criteria.

---

## 7. Dependencies

| Dependency | Needed by | Owner | Status |
|---|---|---|---|
| Read-only Oracle and PostgreSQL accounts | Phase 0 | DBA team | Open (A-10) |
| PostgreSQL sandbox mirroring target | Phase 2 | DBA team | Open (A-11) |
| SSO client registration | Phase 5 | Identity team | Request in Phase 0 |
| VM or server provisioning | Phase 0 | Infrastructure | Open (Open Q 6) |
| Approved mapping table | Phase 2 | Migration lead | Open (G-15) |
| Lower-environment test suites | Phase 4 | QA lead | Open (U-9) |
| Pilot engineers | Phase 7 | Manager | Open (Open Q 7) |

---

## 8. Risks

| Risk | Impact | Mitigation | Phase |
|---|---|---|---|
| SSO integration takes longer than the 2-week window. | Phase 5 slips. | Register the client in Phase 0. Build RBAC against stub claims so the UI can proceed. | 0, 5 |
| Oracle test container unavailable. | Integration tests cannot run locally. | Fallback to recorded fixtures and a shared test database. Decision by week 1. | 0 |
| Linter rules incomplete. | False negatives. | Sandbox execution is the final check (spec risk). Rule set grows with the pilot. | 2, 7 |
| Full row-count comparison too slow. | Missed NFR-5 window. | Volumes measured in Phase 0. Per-table thresholds. Sampling considered after pilot. | 0, 1 |
| Guard bypass. | Production write. | Guard tested with negative tests. Separate credentials and network path. Code review. | 1, 2 |
| Scope creep (scheduling, Jira writes). | MVP delay. | Post-MVP list. Change request required. | All |
| Approval becomes a bottleneck. | Engineer delays. | Dashboard shows pending approvals. Approval SLA is post-MVP. | 5, 7 |

---

## 9. Constitution Check

The migration-tool constitution (to be written in Phase 0) must cover these points. Each phase plan includes a check against them.

- Sections 1 to 4 apply to the migration tool, with Oracle and Atlassian rules replaced by the matching database rules.
- Safety-critical features (guard, read-only connectors, approval gate) require negative tests before completion.
- No production write access from any environment (NFR-1).
- Secrets are never committed (NFR-2, FR-1.4).

---

## 10. Next Steps

1. Confirm or correct assumptions A-1 to A-12 with their owners. Phase 0 cannot close without A-1, A-10, and A-12.
2. Start Phase 0 tasks: constitution rewrite, ADRs, repository skeleton, access requests.
3. Re-run [clarify.md](/Users/akash_saxena1/Desktop/hello-genai/spec/clarify.md) against the updated spec after the answers are recorded. Update this plan where an assumption changed.
