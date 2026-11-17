# Feature Specification: DB Migration QA Automation Tool

**Feature Branch**: `main` (no feature branch yet)
**Created**: 2026-11-18
**Status**: Draft v1, derived from stakeholder interview
**Input**: [project_spec.md](/Users/akash_saxena1/Desktop/hello-genai/project_spec.md) (Module 08 specification)
**Constitution**: [constitution.md](/Users/akash_saxena1/Desktop/hello-genai/spec/constitution.md)

| Field | Value |
|---|---|
| Owner | AI Manager (manages a team of 10 DB migration engineers) |
| Migration | Oracle to PostgreSQL (database engine change) |
| Target | MVP in 8 to 12 weeks, pilot with 2 to 3 engineers first |

## Overview

The team migrates an Oracle database to PostgreSQL. Migration scripts and their results are validated manually today. This slows sign-off and lets defects reach later stages.

The QA Automation Tool:

1. Validates migration scripts before they run against the target.
2. Executes migration scripts in a non-production sandbox, then validates the results.
3. Verifies data correctness between the Oracle source and the PostgreSQL target.
4. Produces a migration readiness sign-off report that the manager can approve.
5. Speeds up sign-off so the migration moves faster.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Migration Scripts Before Execution (Priority: P1)

A migration engineer submits a set of Oracle-to-PostgreSQL migration scripts. The tool lints them and reports Oracle-specific syntax, data type mapping issues, and rule violations before anything runs.

**Why this priority**: Catching defects before execution is the core value and works without a sandbox. It is the first slice to deliver.

**Independent Test**: Submit a script containing known Oracle-only constructs and approved/unapproved type mappings. Verify each finding is reported with script name, line number, rule ID, and severity.

**Acceptance Scenarios**:

1. **Given** a script that uses an Oracle-only function, **When** the engineer runs validation, **Then** the tool flags the line with a rule ID and severity.
2. **Given** a script that maps a column type not in the approved mapping table, **When** validation runs, **Then** the finding identifies the column and the mismatch.
3. **Given** a clean script, **When** validation runs, **Then** no findings are reported and the script is marked validated.

---

### User Story 2 - Execute Scripts in a Sandbox Safely (Priority: P1)

A migration engineer executes validated scripts in the non-production sandbox. The tool records each execution and refuses to run against any environment not flagged as sandbox.

**Why this priority**: Execution is required to test scripts for real. The safety guard protects production and is a hard requirement.

**Independent Test**: Attempt execution against a non-sandbox profile and confirm refusal. Execute against the sandbox and confirm timing, status, and output are recorded.

**Acceptance Scenarios**:

1. **Given** a profile not marked as sandbox, **When** an engineer attempts to execute a script, **Then** the tool refuses and records the refused attempt in the audit log.
2. **Given** a script that fails midway, **When** the run uses default settings, **Then** execution stops at the first error.
3. **Given** a run with the continue-on-error option, **When** a script fails, **Then** execution continues and the failure is recorded.
4. **Given** a completed run, **When** the engineer requests a reset and re-seed, **Then** the sandbox returns to its seeded state so the run can be repeated.

---

### User Story 3 - Verify Data Correctness Between Source and Target (Priority: P1)

After execution, the tool compares Oracle source and PostgreSQL target: row counts, schema, data types, keys, constraints, business rules, and performance. Each check returns a clear result with evidence.

**Why this priority**: This is the main correctness guarantee for the migration and the basis for sign-off.

**Independent Test**: Run the check suite on a known source/target pair with seeded differences. Verify each seeded difference produces the expected status.

**Acceptance Scenarios**:

1. **Given** a source table and a target table with different row counts, **When** the row count check runs, **Then** the result is Fail with both counts as evidence.
2. **Given** a target missing a column present in the source, **When** the schema diff runs, **Then** the missing column is reported.
3. **Given** a business-rule assertion that returns rows, **When** it runs, **Then** the check is Fail and the returned rows are attached as evidence (see NFR-4 for row-value handling).
4. **Given** a query that runs longer than its configured threshold on the target than on the source, **When** the performance check runs, **Then** it is flagged.
5. **Given** a check that cannot execute because a connection fails, **When** the run completes, **Then** the check result is Error with the connection failure details.

---

### User Story 4 - Trigger and Re-run Test Runs (Priority: P2)

An engineer triggers a named, versioned test run from either the web UI or the CLI, and can re-run it later with the same configuration.

**Why this priority**: Both interfaces share the same behavior. The CLI can be delivered before the UI.

**Independent Test**: Trigger a run from the CLI, then trigger the same run from the UI. Confirm both produce identical configuration and results.

**Acceptance Scenarios**:

1. **Given** a saved run definition, **When** an engineer triggers it from the web UI or the CLI, **Then** the run starts with the same scripts, checks, and target environment.
2. **Given** a completed run, **When** an engineer re-runs it, **Then** the new run uses the same configuration and is recorded as a separate execution.

---

### User Story 5 - Approve Migration Runs Through a Gate (Priority: P2)

A manager reviews a run's results and either approves it or accepts known failures with a recorded reason. A run cannot proceed until this approval is recorded.

**Why this priority**: The approval gate prevents unverified migrations from reaching production and is a stated success criterion.

**Independent Test**: Attempt to advance a run with a failed mandatory check and no acceptance. Verify it is blocked. Accept the failure with a reason and verify the run advances and the approval is logged.

**Acceptance Scenarios**:

1. **Given** a run with a failed mandatory check, **When** the manager has not accepted the failure, **Then** the run stays blocked.
2. **Given** a run where all mandatory checks passed, **When** the manager approves it, **Then** the run advances and the approval is logged with approver, timestamp, and comment.
3. **Given** a run with a failed check, **When** the manager accepts the failure with a reason, **Then** the run advances and the accepted failure is recorded in the sign-off report.

---

### User Story 6 - Monitor Team Status and Per-Engineer Work (Priority: P2)

The manager sees a team-wide dashboard of runs, pass/fail rates, open failures, and sign-off status per migration phase. Each engineer sees their own runs, tasks, and failures.

**Why this priority**: Visibility speeds up decisions. It depends on the core engine and the run lifecycle.

**Independent Test**: Log in as the manager and as an engineer. Confirm the manager sees all runs and the engineer sees only their own.

**Acceptance Scenarios**:

1. **Given** runs owned by several engineers, **When** the manager opens the dashboard, **Then** all runs and their statuses are visible.
2. **Given** runs owned by several engineers, **When** an engineer opens their view, **Then** only their own runs and failures are visible.

---

### User Story 7 - Produce and Export Sign-Off Reports (Priority: P2)

The tool generates a migration readiness sign-off report summarizing scope, checks run, results, accepted risks, and the approval record. Reports are exported as CSV and PDF. Once signed off, a report is frozen.

**Why this priority**: The report is the deliverable for sign-off and for attaching to Jira manually.

**Independent Test**: Sign off a run, export both formats, and verify the contents match the stored results. Attempt to change the signed-off record and confirm it is refused.

**Acceptance Scenarios**:

1. **Given** an approved run, **When** the engineer exports the report, **Then** CSV and PDF files are produced with the same results and approval record.
2. **Given** a signed-off report, **When** anyone attempts to modify its stored results, **Then** the change is refused.

---

### User Story 8 - Sign In With Corporate SSO and Role-Based Access (Priority: P2)

Users log in through corporate SSO. Managers see all runs. Engineers see their own runs by default.

**Why this priority**: Access control is required before the tool is used beyond the pilot.

**Independent Test**: Log in with a manager account and an engineer account. Confirm the access rules hold.

**Acceptance Scenarios**:

1. **Given** a user without a valid SSO session, **When** they access the tool, **Then** they are redirected to sign in.
2. **Given** an engineer account, **When** they request another engineer's run, **Then** access is denied.
3. **Given** any action that triggers, approves, or exports, **When** it completes, **Then** an audit log entry is written with user, timestamp, and inputs.

---

### Edge Cases

- A script file is changed after validation but before execution. The run must detect the change through the stored script hash and require re-validation.
- A source or target connection drops mid-check. The affected check is recorded as Error, and the run is marked incomplete rather than passed.
- A business-rule SQL statement is invalid or times out. It is recorded as Error with the database message, not as Pass.
- A table exists in the source but not the target (or the reverse). The schema diff and row count check both report it, without stopping other checks.
- A regression test suite produces flaky results. Retries and flake markers are captured, and the history of that test is shown.
- An approval is attempted by the same user who triggered the run. The behavior must be defined before implementation (see Open Questions).
- A signed-off report is requested after the underlying run definition changed. The report reflects the stored results at sign-off time.
- Row-level values appear in evidence. Evidence must follow NFR-4 (counts, hashes, and identifiers rather than raw values where possible).

---

## Requirements *(mandatory)*

### Functional Requirements

**FR-1 Connection Management**
- **FR-1.1** Store Oracle and PostgreSQL connection profiles (host, port, service/database, schema).
- **FR-1.2** Connect with read-only service accounts for source and target validation.
- **FR-1.3** The sandbox used for script execution has its own connection profile with write access. It is never production.
- **FR-1.4** Credentials are stored in a secrets manager or environment-injected secret store, never in source code or plain-text config.
- **FR-1.5** Test each connection and report its status.

**FR-2 Migration Script Validation (pre-execution)**
- **FR-2.1** Parse and lint migration scripts (SQL and PL/SQL to PostgreSQL dialect).
- **FR-2.2** Flag Oracle-specific syntax that does not run on PostgreSQL.
- **FR-2.3** Check that data type mappings match the approved mapping table.
- **FR-2.4** Report all findings with script name, line number, rule ID, and severity.

**FR-3 Sandbox Execution**
- **FR-3.1** Execute migration scripts in the non-production sandbox only. The tool refuses to run against any profile not marked as sandbox.
- **FR-3.2** Record start time, end time, status, and output for each script run.
- **FR-3.3** Stop execution on first error by default, with an option to continue.
- **FR-3.4** Provide a reset or re-seed option so runs are repeatable.

**FR-4 Post-Execution Validation Checks**
- **FR-4.1** Row count comparison for every table in scope. Full comparison by default.
- **FR-4.2** Schema diff covering tables, columns, data types, indexes, constraints, and sequences.
- **FR-4.3** Data type mapping validation against the approved mapping table.
- **FR-4.4** Null, PK, FK, and constraint checks on the target.
- **FR-4.5** Business-rule assertions: users write SQL that must return zero rows (or a defined expected result). Stored and versioned.
- **FR-4.6** Performance regression checks: time a defined set of queries on source and target and flag results that exceed a configurable threshold.
- **FR-4.7** Application and regression test suites run against the lower environment. The tool invokes the suite, captures pass/fail and logs, and attaches them to the run.
- **FR-4.8** Each check returns one of: Pass, Fail, Warning, or Error, with details and evidence.
- **FR-4.9** Thresholds and check configuration are set per table or per run.

**FR-5 Test Run Triggering**
- **FR-5.1** Trigger a test run manually from the web UI or the CLI.
- **FR-5.2** A run is a named, versioned set of scripts, checks, and target environment.
- **FR-5.3** Runs can be re-run with the same configuration.

**FR-6 Approval Gate**
- **FR-6.1** A migration run is blocked from proceeding until the manager approves it.
- **FR-6.2** Approval requires that all mandatory checks have passed, or that the manager has explicitly accepted known failures with a recorded reason.
- **FR-6.3** Approvals are logged with approver identity, timestamp, and comment.

**FR-7 Reporting and Dashboards**
- **FR-7.1** Team dashboard showing active runs, pass/fail rates, open failures, and sign-off status per migration phase.
- **FR-7.2** Per-engineer view showing that engineer's runs, tasks, and failures.
- **FR-7.3** Migration readiness sign-off report summarizing scope, checks run, results, accepted risks, and approval record.
- **FR-7.4** Export reports as CSV and PDF.
- **FR-7.5** Reports are timestamped and immutable once signed off.

**FR-8 Jira Interaction (export only)**
- **FR-8.1** Reports can be exported in a form that can be attached to Jira tickets manually.
- **FR-8.2** The tool does not write to Jira in the MVP.
- **FR-8.3** Include a Jira ticket reference field on each run, entered manually.

**FR-9 Authentication and Authorization**
- **FR-9.1** Users log in through corporate SSO (SAML or OIDC).
- **FR-9.2** Role-based access with manager and engineer roles at minimum. Engineers are scoped to their own runs by default.
- **FR-9.3** All actions that trigger runs, approve runs, or export reports are audit-logged.

### Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Security | No production write access. Source and target validation uses read-only accounts. The sandbox is isolated from production by network and credentials. |
| NFR-2 | Security | Secrets are never committed to source control. `.env` files are gitignored. |
| NFR-3 | Security | All traffic is encrypted in transit (TLS). Data at rest in the tool's metadata store is encrypted. |
| NFR-4 | Data handling | Data is synthetic or masked. Reports avoid row-level values unless needed as evidence. Store counts, hashes, and sampled identifiers where possible. |
| NFR-5 | Performance | Full row-count comparison on the largest table finishes within an agreed window. The window is defined after measuring data volumes. [NEEDS CLARIFICATION: target duration] |
| NFR-6 | Scalability | Supports 10 concurrent users and a small number of concurrent runs. |
| NFR-7 | Availability | Internal tool. Business-hours availability is acceptable for MVP. |
| NFR-8 | Auditability | Every run, approval, and export is logged with user, timestamp, and inputs. |
| NFR-9 | Deployability | Runs on an internal server or VM with no public internet exposure. |
| NFR-10 | Maintainability | Checks are modular. Adding a new check does not require changes to the run engine. |

### Key Entities

- **Environment**: id, name, type (`source`, `target`, `sandbox`, `lower_env`), connection reference, is_production (always false).
- **MigrationRun**: id, name, version, owner, environment, status, created_at, jira_ref (manual).
- **ScriptExecution**: id, run, script name, script hash, started_at, ended_at, status, output reference.
- **CheckDefinition**: id, check type, scope (table or run), configuration, threshold.
- **CheckResult**: id, run, check, status (Pass, Fail, Warning, Error), details, evidence reference, created_at.
- **BusinessRule**: id, name, SQL, expected result, owner, version.
- **Approval**: id, run, approver, decision, comment, accepted failures, decided_at.
- **SignOffReport**: id, run, generated_at, file reference, checksum, frozen.
- **User**: id, SSO subject, name, email, role.
- **AuditLog**: id, user, action, target type, target id, timestamp, payload hash.

### Run Lifecycle

`Draft -> Validated -> Sandbox Executed -> Checked -> Pending Approval -> Approved -> Signed Off`

A run cannot skip a state. Reports are generated from stored results, and sign-off freezes the record.

---

## Success Criteria *(mandatory)*

- **SC-001**: Elapsed time from "scripts ready" to "signed off" is measurably lower than the current manual baseline. The baseline is measured during the pilot. [NEEDS CLARIFICATION: baseline measurement method]
- **SC-002**: Zero migration runs reach production without a passed QA report and recorded manager approval.
- **SC-003**: Each engineer sees only their own runs and results. The manager sees team-wide status. This is verified by access tests for every role.
- **SC-004**: Every script in a pilot run receives findings with script name, line number, rule ID, and severity.
- **SC-005**: The tool refuses 100% of execution attempts against profiles not marked as sandbox during acceptance testing.
- **SC-006**: Pilot group of 2 to 3 engineers completes at least one full run from validation to signed-off report without manual data correction.
- **SC-007**: CSV and PDF exports of a signed-off report contain the same results and approval record.

---

## Assumptions

1. Hosting is an internal server or VM with no public internet access.
2. Application and regression test suites live in the lower environment and can be invoked from the tool's host.
3. Migration scripts are written in SQL or PL/SQL and can be executed in a non-production sandbox that mirrors the target schema.
4. Data in all environments is synthetic or masked, so PII handling is light. This must be re-checked if the assumption changes.
5. Oracle and PostgreSQL service accounts can be provisioned as read-only for source and target.
6. Corporate SSO (SAML or OIDC) is available and can be integrated.
7. Jira access is limited to manual report attachment during MVP.
8. The stack is Node.js with TypeScript for the backend and CLI, and React with TypeScript for the web UI. Framework and PDF library choices are made during planning (Phase 0).

---

## Out of Scope (MVP)

- Sampled row-level comparison. Revisit after the pilot.
- Scheduled runs and CI/CD pipeline triggers. Manual triggers only.
- Writes to Jira. The tool only exports reports.
- Execution of migration scripts against production.
- Data masking or synthesis.
- Migration of non-Oracle sources.

## Future Considerations (post-MVP)

- Scheduled and CI/CD-triggered validation runs.
- Sampled row-level comparison for very large tables.
- Jira integration (auto-create issues for failed checks, or link to existing tickets).
- Delegated approval or approval SLAs.

---

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Full row-count and checksum comparisons on very large tables take too long. | Slow feedback, missed deadlines. | Measure data volumes in Phase 0. Add per-table thresholds. Revisit sampling after the pilot. |
| Accidental execution against production. | Severe data loss or outage. | Hard guard: only sandbox-flagged profiles can execute writes. Separate credentials and network paths. Code review on the guard. |
| Oracle-to-PostgreSQL dialect differences are hard to lint fully. | False negatives in script validation. | Start with a known rule set. Let engineers add rules. Rely on sandbox execution as the final check. |
| Manager approval becomes a bottleneck. | Delays for engineers. | Show clear status on the dashboard. Consider delegation or approval SLAs post-MVP. |
| Business-rule SQL is written inconsistently across engineers. | Unreliable results. | Provide templates, QA review, and versioning for every rule. |
| Test suite results are unstable or flaky. | False failures. | Capture retries and flake markers. Show per-test history. |
| Scope creep to scheduled runs, CI/CD, and Jira writes. | Delayed MVP. | Keep these in the post-MVP list. Require a change request for any addition. |

---

## Open Questions

1. **Data volumes**: How many rows and tables are in the largest schemas? [NEEDS CLARIFICATION: needed for NFR-5 and the sampling decision]
2. **Approval policy**: Can the manager accept known failures on the sign-off report, or must every check pass? [NEEDS CLARIFICATION: affects FR-6.2]
3. **Business-rule owner**: Who writes and approves business-rule assertions? [NEEDS CLARIFICATION]
4. **Sandbox readiness**: Does a PostgreSQL sandbox that mirrors the target schema already exist? [NEEDS CLARIFICATION]
5. **Test suite details**: What framework do the lower-environment test suites use, and how are they invoked today? [NEEDS CLARIFICATION: affects FR-4.7]
6. **Hosting**: Who owns provisioning of the VM or server for the tool? [NEEDS CLARIFICATION]
7. **Pilot selection**: Which 2 to 3 engineers form the pilot group? [NEEDS CLARIFICATION]
8. **Jira export format**: Is a PDF or CSV attachment enough, or must a specific template be matched? [NEEDS CLARIFICATION: affects FR-8.1]
9. **Self-approval**: Can an engineer approve a run they triggered? [NEEDS CLARIFICATION: affects FR-6 and the edge case above]

---

## Glossary

- **Sandbox**: A non-production PostgreSQL environment where migration scripts are executed safely.
- **Lower environment**: A non-production environment (dev, QA, or staging) used for application testing.
- **Readiness sign-off**: A manager-approved report confirming that a migration run passed QA.
- **Business-rule assertion**: A SQL query that must return zero rows (or an expected result) to pass.
