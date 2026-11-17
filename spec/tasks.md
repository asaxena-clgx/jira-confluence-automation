# Task Breakdown: DB Migration QA Automation Tool

**Based on**: [plan.md](/Users/akash_saxena1/Desktop/hello-genai/spec/plan.md)
**Specification**: [specification.md](/Users/akash_saxena1/Desktop/hello-genai/spec/specification.md)
**Status**: Draft. Tasks that depend on an unconfirmed assumption (A-1 to A-12 in plan.md) are marked **Blocked by**.

## Conventions

- **ID**: `T-<phase>.<n>`. Milestone gate tasks are the last task in each phase.
- **Depends on**: tasks that must be done first. Only real prerequisites are listed.
- **Refs**: requirement IDs from the specification, plus plan assumption IDs.
- Each task is done when every acceptance criterion is checked and the work is merged to the main branch.

## Summary

| Phase | Milestone | Week | Tasks |
|---|---|---|---|
| 0 Setup | M0 | 1 | 13 |
| 1 Core engine (CLI) | M1 | 2 to 3 | 16 |
| 2 Script validation and sandbox | M2 | 4 to 5 | 15 |
| 3 Business rules and performance | M3 | 6 | 5 |
| 4 Test suite runner | M4 | 7 | 4 |
| 5 API, UI, and approval gate | M5 | 8 to 9 | 16 |
| 6 Reporting and frozen sign-off | M6 | 10 | 10 |
| 7 Pilot and hardening | M7 | 11 to 12 | 6 |

---

## Phase 0: Setup (Week 1), Milestone M0

### T-0.1 Confirming blocking assumptions
- **Milestone**: M0 · **Depends on**: none · **Refs**: A-1, A-10, A-12
- Get owner confirmation or correction for the assumptions that gate Phase 0. Record the answers in plan.md Section 2.
- **Acceptance criteria**
  - [ ] A-1 (project scope), A-10 (read-only Oracle access), and A-12 (stack) each have a recorded answer and owner.
  - [ ] plan.md is updated for any assumption that changed.

### T-0.2 Rewriting the constitution for the migration tool
- **Milestone**: M0 · **Depends on**: T-0.1 · **Refs**: A-1, plan Section 9
- Replace the Jira/Confluence constitution with a migration-tool version. Keep the existing structure: stack, principles, quality gates.
- **Acceptance criteria**
  - [ ] No Atlassian rate-limit or Jira write rules remain in constitution.md.
  - [ ] Covers: no production write access from any environment (NFR-1), no committed secrets (NFR-2), and negative tests required for the guard, read-only connectors, and approval gate.
  - [ ] Constitution is approved by the project owner.

### T-0.3 ADR: backend framework
- **Milestone**: M0 · **Depends on**: T-0.1 · **Refs**: A-12
- Decide between Express and Fastify, with rationale.
- **Acceptance criteria**
  - [ ] ADR is in the repo with status Accepted.
  - [ ] ADR states the choice and at least one rejected option with reason.

### T-0.4 ADR: PDF library and background job approach
- **Milestone**: M0 · **Depends on**: T-0.1 · **Refs**: plan Phase 0 work list
- Choose the PDF library and the approach for background work (BullMQ or a simple worker).
- **Acceptance criteria**
  - [ ] ADR is Accepted and states the choice and rationale.
  - [ ] ADR confirms the choice supports the one-run-per-sandbox queue (T-2.14).

### T-0.5 ADR: secret store, metadata store version, and SSO protocol
- **Milestone**: M0 · **Depends on**: T-0.1 · **Refs**: U-1, FR-9.1, NFR-3
- Decide the secret store (U-1), the metadata store version (PostgreSQL 15 unless changed), and whether SSO uses SAML or OIDC.
- **Acceptance criteria**
  - [ ] ADR is Accepted and names the secret store, store version, and SSO protocol.
  - [ ] Secret store can supply database credentials without storing them in a file in the repo.

### T-0.6 Repository skeleton
- **Milestone**: M0 · **Depends on**: T-0.3 · **Refs**: plan Phase 0 work list
- Create `packages/core`, `packages/cli`, `packages/api`, `packages/web`, and `packages/connectors`, with lint and test configuration.
- **Acceptance criteria**
  - [ ] All five packages exist and install with one command.
  - [ ] Lint and an empty unit test run pass locally.

### T-0.7 CI pipeline
- **Milestone**: M0 · **Depends on**: T-0.6 · **Refs**: NFR-2, plan Phase 0
- Run lint, unit tests, and integration tests with PostgreSQL 15 in Docker. Scan for committed secrets.
- **Acceptance criteria**
  - [ ] CI is green on the empty skeleton.
  - [ ] A deliberate lint error fails the build (verified once, then reverted).
  - [ ] A test secret committed in a branch fails the secret scan.

### T-0.8 Spike: Oracle test database
- **Milestone**: M0 · **Depends on**: T-0.6 · **Refs**: plan Phase 0, plan Section 8 risk
- Start an Oracle Free container for integration tests. If it cannot run, choose the fallback (recorded fixtures plus a shared test database).
- **Acceptance criteria**
  - [ ] Either the container starts and a test query returns rows, or the fallback is chosen and recorded in an ADR by end of week 1.

### T-0.9 Read-only database accounts
- **Milestone**: M0 · **Depends on**: T-0.1 · **Blocked by**: A-10 · **Refs**: FR-1.2, NFR-1
- Get read-only accounts for Oracle and PostgreSQL. Each Oracle schema gets its own account.
- **Acceptance criteria**
  - [ ] Connections succeed with each account.
  - [ ] A write statement (INSERT into a scratch table) is refused by the database with the account in use.

### T-0.10 Data volume measurement
- **Milestone**: M0 · **Depends on**: T-0.9 · **Refs**: NFR-5, plan Risk "Full row-count comparison too slow"
- Measure row counts and sizes for the largest tables on the Oracle source.
- **Acceptance criteria**
  - [ ] A table of the largest tables (row count, size) is recorded in a note under spec/.
  - [ ] The measured volume is used to decide whether full comparison is feasible within the NFR-5 window, or whether sampling is needed.

### T-0.11 SSO client registration request
- **Milestone**: M0 · **Depends on**: none · **Refs**: plan Section 7, FR-9.1
- Request SSO client registration from the identity team.
- **Acceptance criteria**
  - [ ] Request is filed and the ticket ID is recorded in plan.md Section 7.

### T-0.12 VM or server provisioning
- **Milestone**: M0 · **Depends on**: T-0.1 · **Refs**: Open Q 6, NFR-9
- Get the VM or server for the tool, with the network path to the sandbox.
- **Acceptance criteria**
  - [ ] Host is reachable from the CI runner and the engineers' network segment.
  - [ ] Owner and access list are recorded in plan.md Section 7.

### T-0.13 Milestone gate M0
- **Milestone**: M0 · **Depends on**: T-0.2 to T-0.12 · **Refs**: plan Section 3
- Check the M0 exit criteria.
- **Acceptance criteria**
  - [ ] ADRs are accepted, CI is green on the skeleton, read-only connections are verified, volumes are recorded, and the constitution is approved.

---

## Phase 1: Core Engine, CLI Only (Weeks 2 to 3), Milestone M1

### T-1.1 Oracle read-only connector
- **Milestone**: M1 · **Depends on**: T-0.6, T-0.9 · **Refs**: FR-1.1, FR-1.2, NFR-1
- Connector that opens a read-only session, reads table metadata, and runs queries.
- **Acceptance criteria**
  - [ ] Connects with the read-only account from T-0.9.
  - [ ] Returns table, column, index, constraint, and sequence metadata for a seeded schema.

### T-1.2 PostgreSQL connector
- **Milestone**: M1 · **Depends on**: T-0.6, T-0.9 · **Refs**: FR-1.1, FR-1.2
- Connector for PostgreSQL with the same interface as T-1.1.
- **Acceptance criteria**
  - [ ] Connects with the read-only account and returns the same metadata shape as T-1.1.

### T-1.3 Connection profiles
- **Milestone**: M1 · **Depends on**: T-1.1, T-1.2, T-0.5 · **Refs**: FR-1.1, FR-1.2, FR-1.4
- Profiles store `profile_type` (source, target, sandbox) and a `read_only` flag. Credentials come from the secret store.
- **Acceptance criteria**
  - [ ] A profile with a credential value in the file is rejected.
  - [ ] A source profile without `read_only` is rejected.
  - [ ] Each profile type can be read back with its flag.

### T-1.4 Read-only statement guard
- **Milestone**: M1 · **Depends on**: T-1.1, T-1.2 · **Refs**: NFR-1, constitution
- Connectors reject any statement that is not a `SELECT` before it reaches the database.
- **Acceptance criteria**
  - [ ] Negative tests refuse INSERT, UPDATE, DELETE, MERGE, DDL, and multi-statement input (for example `SELECT 1; DROP TABLE x`).
  - [ ] Each refused statement is raised as an error and never sent to the database (checked with a mock connection).

### T-1.5 Connection test command
- **Milestone**: M1 · **Depends on**: T-1.3 · **Refs**: FR-1.5
- CLI command that tests each profile and reports success or the failure reason.
- **Acceptance criteria**
  - [ ] Successful profile reports OK. A bad host or password reports the failure reason.
  - [ ] Output never shows the credential value.

### T-1.6 Check interface and result model
- **Milestone**: M1 · **Depends on**: T-0.6 · **Refs**: FR-4.8, NFR-10
- Checks implement `run(context) -> CheckResult`. Statuses are Pass, Fail, Warning, and Error.
- **Acceptance criteria**
  - [ ] A stub check is registered and runs without changes to the engine.
  - [ ] The result model has exactly the four statuses listed.

### T-1.7 Thresholds and per-run configuration
- **Milestone**: M1 · **Depends on**: T-1.6 · **Refs**: FR-4.9
- Load per-table and per-run thresholds from configuration, with defaults.
- **Acceptance criteria**
  - [ ] A table with no override uses the default threshold.
  - [ ] A table override is used in place of the default.
  - [ ] An invalid threshold value is rejected with a clear message.

### T-1.8 Row count check
- **Milestone**: M1 · **Depends on**: T-1.1, T-1.2, T-1.6 · **Refs**: FR-4.1
- Compare row counts for each table between source and sandbox (per A-2).
- **Acceptance criteria**
  - [ ] Equal counts produce Pass. A seeded difference produces Fail with both counts stored.
  - [ ] An unreachable database produces Error with the reason.

### T-1.9 Full comparison check (hash-based)
- **Milestone**: M1 · **Depends on**: T-1.8 · **Refs**: FR-4.1, NFR-4, C-5
- Compare rows by hash. Store counts, hashes, and identifiers only, never row values.
- **Acceptance criteria**
  - [ ] A seeded differing row produces Fail, with the row's identifier and hash stored.
  - [ ] A test asserts that the stored result contains no row values.

### T-1.10 Schema diff check
- **Milestone**: M1 · **Depends on**: T-1.1, T-1.2, T-1.6 · **Refs**: FR-4.2
- Compare tables, columns, types, indexes, constraints, and sequences.
- **Acceptance criteria**
  - [ ] Each seeded difference type (missing table, extra column, type change, missing index, missing constraint, sequence difference) produces a Fail that names the object.
  - [ ] Identical schemas produce Pass.

### T-1.11 Data type mapping check
- **Milestone**: M1 · **Depends on**: T-1.10 · **Blocked by**: G-15 (mapping table) · **Refs**: FR-4.3
- Compare each column's type against the mapping table. Until the approved table exists, use a provisional mapping file.
- **Acceptance criteria**
  - [ ] A column mapped correctly produces Pass. An unmapped type produces Fail.
  - [ ] The mapping table is read from configuration, not hard-coded.

### T-1.12 Null, PK, FK, and constraint checks
- **Milestone**: M1 · **Depends on**: T-1.10 · **Refs**: FR-4.4
- Check nulls in NOT NULL columns, primary keys, foreign keys, and constraints.
- **Acceptance criteria**
  - [ ] A seeded null in a NOT NULL column, a missing PK, and a missing FK each produce Fail.
  - [ ] A clean seeded schema produces Pass for all four.

### T-1.13 Audit log foundation
- **Milestone**: M1 · **Depends on**: T-0.5 · **Refs**: FR-9.3, NFR-8
- Append-only audit table with user, action, target, timestamp, and payload hash.
- **Acceptance criteria**
  - [ ] The data access layer has no update or delete path for audit rows.
  - [ ] A connection test and a check run each write one entry with all five fields.

### T-1.14 CLI identity from OS user
- **Milestone**: M1 · **Depends on**: T-1.13 · **Refs**: FR-9.3 (until Phase 5)
- Until SSO is available, record the local OS username as the actor.
- **Acceptance criteria**
  - [ ] Audit entries from the CLI show the OS username.

### T-1.15 CLI run of read-only checks with stored results
- **Milestone**: M1 · **Depends on**: T-1.5, T-1.8 to T-1.12, T-1.13 · **Refs**: NFR-10, FR-4.8
- CLI command that runs the checks against a profile pair and stores results.
- **Acceptance criteria**
  - [ ] One command runs all Phase 1 checks and stores each result.
  - [ ] A second run keeps the first run's results (history is kept).

### T-1.16 Milestone gate M1
- **Milestone**: M1 · **Depends on**: T-1.1 to T-1.15 · **Refs**: plan Section 3
- Run the seeded test pairs and the read-only negative tests.
- **Acceptance criteria**
  - [ ] Every Phase 1 check gives the expected result on the seeded pairs, including the seeded differences.
  - [ ] All read-only guard negative tests pass.
  - [ ] Audit log has one entry per action in the run.

---

## Phase 2: Script Validation and Sandbox (Weeks 4 to 5), Milestone M2

### T-2.1 Data-driven lint rule engine
- **Milestone**: M2 · **Depends on**: T-1.6 · **Refs**: FR-2.1, FR-2.2, plan risk "Linter rules incomplete"
- Rules are loaded from a data file, so engineers can add rules without code changes.
- **Acceptance criteria**
  - [ ] A rule added to the data file runs with no code change (tested with a dummy rule).

### T-2.2 Oracle-to-PostgreSQL rule set
- **Milestone**: M2 · **Depends on**: T-2.1 · **Refs**: FR-2.1, FR-2.2
- About 30 rules covering common Oracle-specific constructs.
- **Acceptance criteria**
  - [ ] Each rule has an ID, a description, one positive sample, and one negative sample.
  - [ ] Each rule's positive sample produces its finding, and its negative sample does not.

### T-2.3 Labeled linter corpus
- **Milestone**: M2 · **Depends on**: T-2.2 · **Refs**: plan M2 exit criteria
- Scripts with expected findings labeled by hand.
- **Acceptance criteria**
  - [ ] Linter findings match the labels on the whole corpus.

### T-2.4 Findings output
- **Milestone**: M2 · **Depends on**: T-2.1 · **Refs**: FR-2.4, SC-004
- Each finding includes script name, line number, rule ID, and severity.
- **Acceptance criteria**
  - [ ] Every finding in the CLI output has all four fields.
  - [ ] A finding's line number points to the construct in the script.

### T-2.5 Mapping validation against the approved table
- **Milestone**: M2 · **Depends on**: T-1.11 · **Blocked by**: G-15 · **Refs**: FR-2.3
- Flag script references to types or objects not covered by the approved mapping table.
- **Acceptance criteria**
  - [ ] An unmapped object in a script is flagged with its line number.
  - [ ] A mapped object is not flagged.

### T-2.6 Script hash capture and enforcement
- **Milestone**: M2 · **Depends on**: T-2.1 · **Refs**: G-24 (edge case)
- Store a hash of each script at validation. Block execution if the hash has changed.
- **Acceptance criteria**
  - [ ] A script edited after validation is refused with a message saying it must be re-validated.
  - [ ] An unchanged script runs.

### T-2.7 Sandbox profile guard
- **Milestone**: M2 · **Depends on**: T-1.3 · **Refs**: FR-3.1, NFR-1, SC-005
- The executor runs only against profiles flagged `sandbox`.
- **Acceptance criteria**
  - [ ] Negative tests cover a source profile, a target profile, a profile with no flag, and a read-only profile. All are refused.
  - [ ] The guard refuses 100% of non-sandbox attempts in the test suite (SC-005).

### T-2.8 Sandbox executor with per-script records
- **Milestone**: M2 · **Depends on**: T-2.6, T-2.7 · **Refs**: FR-3.2
- Run each script in the sandbox and record start time, end time, status, and output.
- **Acceptance criteria**
  - [ ] Each executed script has all four recorded fields.
  - [ ] A script that errors records status Error with its database message.

### T-2.9 Stop on first error, with continue option
- **Milestone**: M2 · **Depends on**: T-2.8 · **Refs**: FR-3.3
- Stop at the first error by default. A continue flag runs the remaining scripts.
- **Acceptance criteria**
  - [ ] Default run stops after the first error and marks later scripts as not run.
  - [ ] With the continue flag, all scripts run and each error is recorded.

### T-2.10 Sandbox reset from snapshot
- **Milestone**: M2 · **Depends on**: T-2.8 · **Blocked by**: A-11 · **Refs**: FR-3.4, G-5
- Reset the sandbox to a snapshot, then re-seed.
- **Acceptance criteria**
  - [ ] After reset, row counts for each table match the snapshot.
  - [ ] The reset is logged to the audit log.

### T-2.11 Audit of refused sandbox attempts
- **Milestone**: M2 · **Depends on**: T-2.7, T-1.13 · **Refs**: US2 scenario 1
- Every refused execution attempt writes an audit entry.
- **Acceptance criteria**
  - [ ] A refused attempt creates an audit entry with the reason for refusal.

### T-2.12 Run model with versioning
- **Milestone**: M2 · **Depends on**: T-1.15 · **Refs**: FR-5.2, A-8
- `MigrationRun` stores script list, check list, environment, and version. Editing a run definition creates a new version.
- **Acceptance criteria**
  - [ ] A run records its script list, check list, environment, and version.
  - [ ] Editing a saved run definition creates version N+1 and leaves version N unchanged.

### T-2.13 CLI run trigger and re-run
- **Milestone**: M2 · **Depends on**: T-2.12, T-2.8 · **Refs**: FR-5.1 (CLI), FR-5.3, A-8
- Trigger a run from the CLI and re-run it.
- **Acceptance criteria**
  - [ ] One CLI command runs validation, sandbox execution, and checks end to end.
  - [ ] A re-run uses the same version and creates a new execution record.

### T-2.14 Sandbox lock and queue
- **Milestone**: M2 · **Depends on**: T-2.13 · **Refs**: A-5, G-4
- One active run per sandbox. Other runs wait in a queue.
- **Acceptance criteria**
  - [ ] A second run started while one is active is queued, not run.
  - [ ] The queued run starts when the first finishes or fails.
  - [ ] A lock held by a crashed process is released after a timeout (tested with a simulated crash).

### T-2.15 Milestone gate M2
- **Milestone**: M2 · **Depends on**: T-2.1 to T-2.14 · **Refs**: plan Section 3
- **Acceptance criteria**
  - [ ] Linter output matches the labeled corpus.
  - [ ] The guard refuses 100% of negative cases.
  - [ ] Reset restores the snapshot.
  - [ ] A run executes end to end from the CLI.

---

## Phase 3: Business Rules and Performance (Week 6), Milestone M3

### T-3.1 SQL business-rule check
- **Milestone**: M3 · **Depends on**: T-1.6, T-1.3 · **Refs**: FR-4.5, A-2
- A rule either returns zero rows, or matches an expected result. Rules run against the sandbox.
- **Acceptance criteria**
  - [ ] A zero-row rule with no rows returns Pass. The same rule with rows returns Fail with the row count.
  - [ ] An expected-result rule matches or fails correctly.

### T-3.2 Business-rule versioning
- **Milestone**: M3 · **Depends on**: T-3.1 · **Refs**: U-8, A-8
- A changed rule creates a new version. Past results keep the version they ran with.
- **Acceptance criteria**
  - [ ] Changing a rule creates a new version, and the old version's results still show the old version number.

### T-3.3 Invalid and timed-out SQL recorded as Error
- **Milestone**: M3 · **Depends on**: T-3.1 · **Refs**: plan Phase 3 edge case
- A syntax error or timeout is recorded as Error. Other checks keep running.
- **Acceptance criteria**
  - [ ] Syntax error and timeout each produce Error with the database message.
  - [ ] Remaining checks in the run still execute.

### T-3.4 Performance regression check
- **Milestone**: M3 · **Depends on**: T-1.1, T-1.2, T-1.6 · **Refs**: FR-4.6, G-16
- Time a configured query set on source and sandbox. Use a relative threshold with an absolute floor.
- **Acceptance criteria**
  - [ ] A seeded slow query (sandbox slower than source beyond the threshold) produces Fail.
  - [ ] An unchanged query produces Pass.
  - [ ] A query under the absolute floor cannot produce Fail, whatever its ratio.

### T-3.5 Milestone gate M3
- **Milestone**: M3 · **Depends on**: T-3.1 to T-3.4 · **Refs**: plan Section 3
- **Acceptance criteria**
  - [ ] Versioned rules run and record the version used.
  - [ ] Performance check flags the seeded slow query and passes the unchanged one.

---

## Phase 4: Test Suite Runner (Week 7), Milestone M4

### T-4.1 Suite runner with command template
- **Milestone**: M4 · **Depends on**: T-1.6 · **Blocked by**: U-9 · **Refs**: FR-4.7
- Run a configured command and capture exit code, pass and fail counts, and logs. Works with any framework that reports an exit code and output.
- **Acceptance criteria**
  - [ ] A sample suite run records the exit code and full log.
  - [ ] Pass and fail counts are recorded when the output is parseable, and the run is marked as exit-code-only otherwise.

### T-4.2 Retry policy and flake marking
- **Milestone**: M4 · **Depends on**: T-4.1 · **Refs**: plan Phase 4 flakiness risk
- Retry failed tests up to a configured limit. A test that fails then passes is marked flaky.
- **Acceptance criteria**
  - [ ] A test that fails once and passes on retry is marked flaky, and each attempt is recorded.
  - [ ] Retry count comes from configuration.

### T-4.3 Attach suite results to runs
- **Milestone**: M4 · **Depends on**: T-4.1, T-2.12 · **Refs**: FR-4.7
- Store the suite result and logs on the run and in a per-test history.
- **Acceptance criteria**
  - [ ] The run record shows the suite result and a link to the log.
  - [ ] A test's history across runs can be queried.

### T-4.4 Milestone gate M4
- **Milestone**: M4 · **Depends on**: T-4.1 to T-4.3 · **Refs**: plan Section 3
- **Acceptance criteria**
  - [ ] A sample suite runs and its results and logs are attached.
  - [ ] A flaky test is marked on its second run.

---

## Phase 5: API, UI, and Approval Gate (Weeks 8 to 9), Milestone M5

### T-5.1 REST API for runs, checks, approvals, and reports
- **Milestone**: M5 · **Depends on**: T-2.13, T-1.15 · **Refs**: NFR-10, FR-5.1 (UI part)
- Endpoints call the same services as the CLI.
- **Acceptance criteria**
  - [ ] Endpoints exist for runs, checks, approvals, and reports, with a documented schema.
  - [ ] Endpoints call the same service functions as the CLI (no duplicate logic).

### T-5.2 CLI and API parity contract tests
- **Milestone**: M5 · **Depends on**: T-5.1 · **Refs**: plan Section 6 (contract tests)
- **Acceptance criteria**
  - [ ] The same run gives identical results from the CLI and the API.

### T-5.3 SSO login and role mapping
- **Milestone**: M5 · **Depends on**: T-0.5, T-0.11, T-5.1 · **Blocked by**: SSO registration · **Refs**: FR-9.1, FR-9.2, A-7
- Log in through SSO. Map group claims to `User.role` on first login.
- **Acceptance criteria**
  - [ ] A user with an approved group claim logs in and receives the mapped role.
  - [ ] A user with no approved group is denied access.

### T-5.4 RBAC tests on stub claims
- **Milestone**: M5 · **Depends on**: T-0.11 · **Refs**: plan Section 8 (SSO risk)
- Build RBAC against stub claims so the UI can proceed while SSO is pending.
- **Acceptance criteria**
  - [ ] The RBAC test suite runs against stub claims and passes.
  - [ ] Stub claims are not used in any non-test configuration.

### T-5.5 RBAC rules
- **Milestone**: M5 · **Depends on**: T-5.3 or T-5.4 · **Refs**: FR-9.2, G-8, G-11
- Engineers see their own runs. Managers see all runs. QA engineers can edit business rules.
- **Acceptance criteria**
  - [ ] An engineer requesting another engineer's run is denied.
  - [ ] A manager sees all runs. A QA engineer can edit a business rule but cannot approve a run.

### T-5.6 Run state machine
- **Milestone**: M5 · **Depends on**: T-2.12 · **Refs**: FR-6.1
- Enforce `Draft -> Validated -> Sandbox Executed -> Checked -> Pending Approval -> Approved -> Signed Off` in code.
- **Acceptance criteria**
  - [ ] Each allowed transition succeeds.
  - [ ] Skipping a state (for example Draft to Approved) is rejected.
  - [ ] Each rejected transition is audit logged.

### T-5.7 Approval gate
- **Milestone**: M5 · **Depends on**: T-5.6 · **Refs**: FR-6.1, FR-6.2, A-3, A-4
- A run cannot move past Checked until approved. Fail and Error block approval. Warning does not. Only mandatory checks gate approval.
- **Acceptance criteria**
  - [ ] A run with a Fail or Error check cannot be approved.
  - [ ] A run with only Warning results can be approved.
  - [ ] A failing optional check does not block approval.

### T-5.8 Approval record and accepted failures
- **Milestone**: M5 · **Depends on**: T-5.7 · **Refs**: FR-6.2, FR-6.3
- Approval stores approver, timestamp, comment, and any accepted failures with reasons.
- **Acceptance criteria**
  - [ ] An approval record has all four fields.
  - [ ] An accepted failure with no reason is rejected.

### T-5.9 Self-approval blocked
- **Milestone**: M5 · **Depends on**: T-5.7, T-5.3 or T-5.4 · **Blocked by**: A-6 · **Refs**: A-6
- The run owner cannot approve their own run.
- **Acceptance criteria**
  - [ ] A test where the approver is the run owner is refused.

### T-5.10 Web UI: run triggering
- **Milestone**: M5 · **Depends on**: T-5.1, T-5.5 · **Refs**: FR-5.1 (UI part)
- Engineers trigger a run from the web UI (React + TypeScript).
- **Acceptance criteria**
  - [ ] A run triggered in the UI produces the same result as the CLI with the same definition.

### T-5.11 Team dashboard
- **Milestone**: M5 · **Depends on**: T-5.5 · **Refs**: FR-7.1, plan Section 8 (approval bottleneck)
- Show runs and their status. Show pending approvals to managers.
- **Acceptance criteria**
  - [ ] The dashboard lists runs with their current state.
  - [ ] A manager sees pending approvals at the top.

### T-5.12 Per-engineer view
- **Milestone**: M5 · **Depends on**: T-5.5 · **Refs**: FR-7.2
- Each engineer sees only their own runs.
- **Acceptance criteria**
  - [ ] An engineer's view lists only their runs.

### T-5.13 Audit log for trigger and approve actions with SSO identity
- **Milestone**: M5 · **Depends on**: T-1.13, T-5.3 · **Refs**: FR-9.3, NFR-8
- Trigger and approve actions record the SSO identity. CLI entries keep the OS username.
- **Acceptance criteria**
  - [ ] A trigger or approve action in the UI records the SSO user.
  - [ ] A CLI action still records the OS user.

### T-5.14 TLS for web and API
- **Milestone**: M5 · **Depends on**: T-5.1 · **Refs**: NFR-3
- **Acceptance criteria**
  - [ ] Plain HTTP is refused or redirected to HTTPS.
  - [ ] The certificate is valid for the tool's host name.

### T-5.15 Load test for 10 concurrent users
- **Milestone**: M5 · **Depends on**: T-5.10, T-5.11, T-5.12 · **Refs**: NFR-6
- **Acceptance criteria**
  - [ ] 10 concurrent users run the dashboard and run list scenario, and the results meet the latency target in NFR-6.

### T-5.16 Milestone gate M5
- **Milestone**: M5 · **Depends on**: T-5.1 to T-5.15 · **Refs**: plan Section 3
- **Acceptance criteria**
  - [ ] Gate tests cover every state transition, including blocked runs and self-approval.
  - [ ] Engineer access tests confirm no cross-engineer access.
  - [ ] An engineer triggers a run and a manager approves it in the UI.

---

## Phase 6: Reporting and Frozen Sign-Off (Week 10), Milestone M6

### T-6.1 Sign-off report generator
- **Milestone**: M6 · **Depends on**: T-5.8, T-4.3 · **Refs**: FR-7.3
- Build the report from stored results only. Sections: scope, checks, results, accepted risks, approval record.
- **Acceptance criteria**
  - [ ] The report contains all five sections.
  - [ ] Generating the report makes no connection to the source or sandbox (checked by a test with connections blocked).

### T-6.2 CSV export
- **Milestone**: M6 · **Depends on**: T-6.1 · **Refs**: FR-7.4, SC-007
- **Acceptance criteria**
  - [ ] CSV rows match the stored results for the test run.

### T-6.3 PDF export
- **Milestone**: M6 · **Depends on**: T-6.1 · **Refs**: FR-7.4, SC-007, U-13
- **Acceptance criteria**
  - [ ] The PDF text matches the CSV content for the test run (checked by an automated comparison).

### T-6.4 Freeze on sign-off
- **Milestone**: M6 · **Depends on**: T-5.6 · **Refs**: FR-7.5, C-8
- Stored results become immutable after sign-off.
- **Acceptance criteria**
  - [ ] An update to a signed-off run's results is refused by the service and the database.

### T-6.5 Amendment path
- **Milestone**: M6 · **Depends on**: T-6.4 · **Refs**: C-8, FR-7.5
- An amendment creates a new signed version with the approver and reason. The original is kept.
- **Acceptance criteria**
  - [ ] An amendment without a reason is refused.
  - [ ] After an amendment, both the original and the new version are retrievable.

### T-6.6 Checksum on exported files
- **Milestone**: M6 · **Depends on**: T-6.2, T-6.3 · **Refs**: NFR-3
- Store a checksum for each signed-off export in `SignOffReport`.
- **Acceptance criteria**
  - [ ] A verify command passes on an untouched file and fails on an edited copy.

### T-6.7 Jira reference field and export
- **Milestone**: M6 · **Depends on**: T-2.12 · **Refs**: FR-8.1, FR-8.2, FR-8.3
- Engineers enter a Jira reference on each run. The export can be attached to Jira manually.
- **Acceptance criteria**
  - [ ] The reference is saved on the run and shown in the export.
  - [ ] A test confirms the tool makes no requests to Jira or Confluence.

### T-6.8 Encryption at rest for the metadata store
- **Milestone**: M6 · **Depends on**: T-0.5 · **Refs**: NFR-3, G-23
- **Acceptance criteria**
  - [ ] Config or infrastructure check confirms the metadata store volume is encrypted.

### T-6.9 Audit log for exports
- **Milestone**: M6 · **Depends on**: T-6.2, T-6.3, T-1.13 · **Refs**: NFR-8
- **Acceptance criteria**
  - [ ] Each CSV and PDF export writes one audit entry with the user, file type, and checksum.

### T-6.10 Milestone gate M6
- **Milestone**: M6 · **Depends on**: T-6.1 to T-6.9 · **Refs**: plan Section 3
- **Acceptance criteria**
  - [ ] CSV and PDF match on a test run.
  - [ ] Frozen reports cannot be edited.
  - [ ] The amendment path works.
  - [ ] MVP feature list is complete.

---

## Phase 7: Pilot and Hardening (Weeks 11 to 12), Milestone M7

### T-7.1 Confirm pilot engineers
- **Milestone**: M7 · **Depends on**: none · **Blocked by**: Open Q 7 · **Refs**: plan Section 7
- **Acceptance criteria**
  - [ ] 2 to 3 engineers are named and their access is granted.

### T-7.2 Pilot run end to end
- **Milestone**: M7 · **Depends on**: T-6.10, T-7.1 · **Refs**: SC-001, SC-006
- Each pilot engineer completes one run from validation to signed-off report.
- **Acceptance criteria**
  - [ ] Each engineer completes one run and gets a signed-off report.
  - [ ] Time for each run is recorded for the SC-001 and SC-006 comparison.

### T-7.3 Defect triage and fixes
- **Milestone**: M7 · **Depends on**: T-7.2 · **Refs**: plan Phase 7
- **Acceptance criteria**
  - [ ] No open Sev-1 defects. Open Sev-2 defects are listed with owners.

### T-7.4 Runbook
- **Milestone**: M7 · **Depends on**: T-6.8, T-0.9 · **Refs**: NFR-9, G-18
- Covers installation on the VM, backup and restore, secret rotation, Oracle and PostgreSQL account setup, and how to add a lint rule.
- **Acceptance criteria**
  - [ ] Each section is written. A reviewer who did not write it can follow the install steps on a clean VM.

### T-7.5 Backup and restore drill
- **Milestone**: M7 · **Depends on**: T-6.8 · **Refs**: G-18, NFR-9
- **Acceptance criteria**
  - [ ] A restore from backup into a clean environment reproduces a signed-off run and its report.

### T-7.6 Measurement and go or no-go decision
- **Milestone**: M7 · **Depends on**: T-7.2, T-7.3 · **Refs**: SC-001, SC-006, NFR-7, G-28
- **Acceptance criteria**
  - [ ] SC-001 and SC-006 are measured against the baseline from the pilot.
  - [ ] A go or no-go decision for the other engineers is recorded with its reasons.
  - [ ] M7 exit criteria are met: a pilot run is signed off end to end, the runbook is reviewed, and no Sev-1 defects are open.

---

## Dependency Notes

- Phase 0 gates everything. T-0.1 must be answered before any other Phase 0 task that is marked **Blocked by**.
- The first database-touching work (T-1.1, T-1.2) starts only after T-0.9 is complete. Otherwise the guard cannot be tested against real accounts.
- Tasks marked **Blocked by** an open item (A-6, A-10, A-11, A-12, G-15, U-9, Open Q 7, SSO registration) can start their code, but cannot be marked done until the item is closed.
