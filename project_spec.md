# Project Specification: DB Migration QA Automation Tool

| Field | Value |
|---|---|
| Owner | AI Manager (manages a team of 10 DB migration engineers) |
| Migration | Oracle to PostgreSQL (database engine change) |
| Status | Draft v1, derived from stakeholder interview |
| Target | MVP in 8 to 12 weeks, pilot with 2 to 3 engineers first |

---

## 1. Purpose and Problem Statement

The team migrates an Oracle database to PostgreSQL. Migration scripts and their results are currently validated manually, which slows sign-off and lets defects reach later stages.

The QA Automation Tool must:

1. **Validate migration scripts before they run** against the target.
2. **Execute migration scripts in a non-production sandbox**, then validate the results.
3. **Verify data correctness** between Oracle source and PostgreSQL target.
4. **Produce a migration readiness sign-off report** that the manager can approve.
5. **Speed up sign-off** so the migration moves faster.

### Success Criteria
- Faster migration readiness sign-off (measured as elapsed time from "scripts ready" to "signed off").
- No migration run reaches production without a passed QA report and manager approval.
- Each engineer can see their own tasks and results. The manager can see team-wide status.

---

## 2. Scope

### 2.1 In Scope (MVP)
- Source (Oracle) and target (PostgreSQL) connection profiles, read-only.
- Migration script validation (static checks before execution).
- Execution of migration scripts in a **non-production sandbox** only.
- Post-execution validation checks:
  - **Row count comparison**, full comparison for all tables.
  - **Schema diff**: tables, columns, types, indexes, and constraints.
  - **Data type mapping validation** (Oracle to PostgreSQL).
  - **Null, PK, FK, and constraint validation.**
  - **Custom business-rule SQL assertions** (user-defined).
  - **Query performance and regression timing.**
  - **Running application/regression test suites** in the lower environment.
- Manual test-run triggers from **both the web UI and the CLI**.
- Manager approval gate before a migration run can proceed.
- Team dashboard and per-engineer task views.
- Exportable reports (CSV and PDF) for migration readiness sign-off.
- Login with corporate SSO.

### 2.2 Out of Scope (MVP)
- **Sampled row-level comparison.** Not selected for MVP. Revisit after the pilot.
- **Scheduled runs and CI/CD pipeline triggers.** Manual triggers only for MVP.
- **Writes to Jira.** The tool only exports reports. No issues are created or updated.
- Execution of migration scripts against **production**.
- Data masking or synthesis. Test data is already synthetic or masked.
- Migration of non-Oracle sources.

### 2.3 Future Considerations (post-MVP)
- Scheduled and CI/CD-triggered validation runs.
- Sampled row-level comparison for very large tables.
- Jira integration (auto-create issues for failed checks, or link to existing tickets).

---

## 3. Users and Roles

| Role | Needs |
|---|---|
| **Manager** (primary) | Team-wide dashboard, approval gate for migration runs, readiness sign-off reports, exports. |
| **Migration engineer** (about 10) | Trigger validation and test runs, view own tasks and results, see failed checks with details. |
| **QA engineer** (if separate from migration engineers) | Define business-rule assertions, review failed checks. |

Authorization is role-based, with manager and engineer roles at minimum. Engineers see their own runs by default. The manager sees all runs.

---

## 4. Functional Requirements

### FR-1 Connection Management
- FR-1.1 Store Oracle and PostgreSQL connection profiles (host, port, service/database, schema).
- FR-1.2 Connect with **read-only service accounts** for source and target validation.
- FR-1.3 The sandbox used for script execution has its own connection profile with write access. It is never production.
- FR-1.4 Credentials are stored in a secrets manager or environment-injected secret store, never in source code or plain-text config.
- FR-1.5 Test each connection and report its status.

### FR-2 Migration Script Validation (pre-execution)
- FR-2.1 Parse and lint migration scripts (SQL and PL/SQL to PostgreSQL dialect).
- FR-2.2 Flag Oracle-specific syntax that does not run on PostgreSQL.
- FR-2.3 Check that data type mappings match the approved mapping table.
- FR-2.4 Report all findings with script name, line number, rule ID, and severity.

### FR-3 Sandbox Execution
- FR-3.1 Execute migration scripts in the **non-production sandbox** only. The tool refuses to run against any profile not marked as sandbox.
- FR-3.2 Record start time, end time, status, and output for each script run.
- FR-3.3 Stop execution on first error by default, with an option to continue.
- FR-3.4 Provide a reset or re-seed option so runs are repeatable.

### FR-4 Post-Execution Validation Checks
- FR-4.1 **Row count comparison** for every table in scope. Full comparison by default.
- FR-4.2 **Schema diff** covering tables, columns, data types, indexes, constraints, and sequences.
- FR-4.3 **Data type mapping validation** against the approved mapping table.
- FR-4.4 **Null, PK, FK, and constraint checks** on the target.
- FR-4.5 **Business-rule assertions**: users write SQL that must return zero rows (or a defined expected result). Stored and versioned.
- FR-4.6 **Performance regression checks**: time a defined set of queries on source and target and flag results that exceed a configurable threshold.
- FR-4.7 **Application/regression test suites** run against the lower environment. The tool invokes the suite, captures pass/fail and logs, and attaches them to the run.
- FR-4.8 Each check returns: Pass, Fail, Warning, or Error, with details and evidence.
- FR-4.9 Thresholds and check configuration are set per table or per run.

### FR-5 Test Run Triggering
- FR-5.1 Trigger a test run manually from the **web UI** or the **CLI**.
- FR-5.2 A run is a named, versioned set of: scripts, checks, and target environment.
- FR-5.3 Runs can be re-run with the same configuration.

### FR-6 Approval Gate
- FR-6.1 A migration run is **blocked from proceeding** until the manager approves it.
- FR-6.2 Approval requires that all mandatory checks have passed, or that the manager has explicitly accepted known failures with a recorded reason.
- FR-6.3 Approvals are logged with approver identity, timestamp, and comment.

### FR-7 Reporting and Dashboards
- FR-7.1 **Team dashboard** showing: active runs, pass/fail rates, open failures, and sign-off status per migration phase.
- FR-7.2 **Per-engineer view** showing that engineer's runs, tasks, and failures.
- FR-7.3 **Migration readiness sign-off report** summarizing scope, checks run, results, accepted risks, and approval record.
- FR-7.4 Export reports as **CSV and PDF**.
- FR-7.5 Reports are timestamped and immutable once signed off.

### FR-8 Jira Interaction (export only)
- FR-8.1 Reports can be exported in a form that can be attached to Jira tickets manually.
- FR-8.2 The tool does **not** write to Jira in the MVP.
- FR-8.3 Include a Jira ticket reference field on each run, entered manually.

### FR-9 Authentication and Authorization
- FR-9.1 Users log in through **corporate SSO** (SAML or OIDC).
- FR-9.2 Role-based access: manager and engineer, with engineers scoped to their own runs by default.
- FR-9.3 All actions that trigger runs, approve runs, or export reports are audit-logged.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-1 | Security | No production write access. Source and target validation uses read-only accounts. Sandbox is isolated from production by network and credentials. |
| NFR-2 | Security | Secrets are never committed to source control. `.env` files are gitignored (already configured in this repo). |
| NFR-3 | Security | All traffic is encrypted in transit (TLS). Data at rest in the tool's own metadata store is encrypted. |
| NFR-4 | Data handling | Data is synthetic or masked. The tool should still avoid storing row-level values in reports unless needed for evidence. Store counts, hashes, and sampled identifiers where possible. |
| NFR-5 | Performance | Full row-count comparison on the largest table should finish within an agreed window (to be defined with the team after measuring data volumes). |
| NFR-6 | Scalability | Supports 10 concurrent users and a small number of concurrent runs. |
| NFR-7 | Availability | Internal tool. Business hours availability is acceptable for MVP. |
| NFR-8 | Auditability | Every run, approval, and export is logged with user, timestamp, and inputs. |
| NFR-9 | Deployability | Runs on an internal server or VM with no public internet exposure. |
| NFR-10 | Maintainability | Checks are modular. Adding a new check does not require changes to the run engine. |

---

## 6. Recommended Technical Architecture

The stakeholder had no stack preference, so this is a recommendation.

### 6.1 Technology Stack
| Layer | Recommendation | Rationale |
|---|---|---|
| Language | **Python 3.12+** | Mature Oracle and PostgreSQL drivers (`python-oracledb`, `psycopg`). Strong data and reporting libraries. |
| Backend API | **FastAPI** | Typed, async-ready, and easy to expose to both the web UI and the CLI. |
| CLI | **Typer** | Thin layer over the same service functions used by the API. |
| Web UI | **React + TypeScript** (or server-rendered templates for MVP) | Dashboard and per-engineer views. Keep the MVP UI small. |
| Metadata store | **PostgreSQL** | Stores runs, checks, results, approvals, and audit logs. Reuses the team's existing PostgreSQL skills. |
| Job execution | **Background worker** (for example, a task queue such as Celery or RQ, or a simple worker process for MVP) | Long-running comparisons and test suites should not block the API. |
| Reporting | **Jinja2 + WeasyPrint** for PDF, standard CSV writer | Generates sign-off reports. |
| Auth | **OIDC/SAML** via the corporate identity provider | Required by the stakeholder. |
| Testing | **pytest** for the tool, plus **the tool's own checks** as the QA product | Keeps the test approach consistent with the Python stack. |

### 6.2 Components
```
+------------------+      +------------------+
|   Web UI         |      |   CLI            |
+--------+---------+      +--------+---------+
         |                         |
         +------------+------------+
                      |
              +-------v--------+
              |  REST API      |  (FastAPI, SSO auth, RBAC)
              +-------+--------+
                      |
        +-------------+--------------+
        |                            |
+-------v--------+          +--------v---------+
| Run Orchestrator|--------->| Background Workers|
+-------+--------+          +--------+---------+
        |                            |
        |          +-----------------+-------------------+
        |          |                 |                   |
        |   +------v-----+   +-------v------+   +--------v-------+
        |   | Script      |   | Check Engine |   | Test Suite     |
        |   | Validator & |   | (modular     |   | Runner (lower  |
        |   | Sandbox Exec|   |  checks)     |   |  env)          |
        |   +------+------+   +------+-------+   +--------+-------+
        |          |                 |                    |
        |   +------v-----------------v--------------------v------+
        |   |  Connectors: Oracle (read-only), PostgreSQL          |
        |   |  (read-only target, sandbox write-enabled)           |
        |   +------------------------------------------------------+
        |
+-------v--------+      +-----------------+
| Metadata Store  |      | Report Generator|  (CSV, PDF)
| (PostgreSQL)    |      +-----------------+
+-----------------+
```

### 6.3 Key Design Points
- **Connector isolation:** Oracle and PostgreSQL connectors are read-only except the sandbox connector. A guard refuses writes on any non-sandbox profile.
- **Plugin-style checks:** Each check implements a common interface (`run(context) -> CheckResult`). New checks register without changing the run engine.
- **Run lifecycle:** `Draft -> Validated -> Sandbox Executed -> Checked -> Pending Approval -> Approved -> Signed Off`. A run cannot skip a state.
- **Idempotent reports:** Reports are generated from stored results. Sign-off freezes the record.

---

## 7. Data Model (initial)

| Entity | Key fields |
|---|---|
| `Environment` | id, name, type (`source`, `target`, `sandbox`, `lower_env`), connection_ref, is_production (always false) |
| `MigrationRun` | id, name, version, owner_id, environment_id, status, created_at, jira_ref (manual) |
| `ScriptExecution` | id, run_id, script_name, script_hash, started_at, ended_at, status, output_ref |
| `CheckDefinition` | id, check_type, scope (table or run), config (JSON), threshold |
| `CheckResult` | id, run_id, check_id, status (Pass, Fail, Warning, Error), details (JSON), evidence_ref, created_at |
| `BusinessRule` | id, name, sql, expected_result, owner_id, version |
| `Approval` | id, run_id, approver_id, decision, comment, accepted_failures (JSON), decided_at |
| `SignOffReport` | id, run_id, generated_at, file_ref, checksum, frozen |
| `User` | id, sso_subject, name, email, role |
| `AuditLog` | id, user_id, action, target_type, target_id, timestamp, payload_hash |

---

## 8. Phased Delivery Plan (8 to 12 weeks)

| Phase | Weeks | Deliverables |
|---|---|---|
| 0. Setup | 1 | Repo structure, CI basics, environment profiles, read-only account setup, data volume measurement. |
| 1. Core engine | 2 to 3 | Connectors, check interface, row count, schema diff, data type mapping, null/constraint checks. CLI only. |
| 2. Script validation and sandbox | 4 to 5 | Script linter for Oracle-to-PostgreSQL issues, sandbox execution with safety guard. |
| 3. Business rules and performance | 6 | Business-rule SQL assertions with versioning, performance regression checks. |
| 4. Test suite runner | 7 | Invoke lower-env regression suites and capture results. |
| 5. API, UI, and approval gate | 8 to 9 | REST API, SSO, RBAC, dashboards, per-engineer views, approval workflow. |
| 6. Reporting | 10 | CSV and PDF sign-off reports, frozen records, audit log. |
| 7. Pilot and hardening | 11 to 12 | Pilot with 2 to 3 engineers, fix issues, document runbook. |

The MVP is complete after Phase 6. Phase 7 is the pilot. Rollout to all 10 engineers follows pilot sign-off.

---

## 9. Assumptions

1. The tech stack was not specified, so Python is recommended (Section 6.1). Confirm before Phase 0.
2. Hosting is an **internal server or VM** with no public internet access.
3. Application/regression test suites live in the **lower environment** and can be invoked from the tool's host.
4. Migration scripts are written in SQL or PL/SQL and can be executed in a **non-production sandbox** that mirrors the target schema.
5. Data in all environments is **synthetic or masked**, so PII handling is light. This must be re-checked if the assumption changes.
6. Oracle and PostgreSQL service accounts can be provisioned as read-only for source and target.
7. Corporate SSO (SAML or OIDC) is available and can be integrated.
8. Jira access is limited to manual report attachment during MVP.

---

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Full row-count and checksum comparisons on very large tables take too long. | Slow feedback, missed deadlines. | Measure data volumes in Phase 0. Add per-table thresholds. Revisit sampling after the pilot. |
| Accidental execution against production. | Severe data loss or outage. | Hard guard: only profiles flagged as sandbox can execute writes. Separate credentials and network paths. Code review on the guard. |
| Oracle-to-PostgreSQL dialect differences are hard to lint fully. | False negatives in script validation. | Start with a known rule set. Let engineers add rules. Rely on sandbox execution as the final check. |
| Manager approval becomes a bottleneck. | Delays for engineers. | Show clear status on the dashboard. Allow the manager to delegate or set approval SLAs (post-MVP). |
| Business-rule SQL is written inconsistently across engineers. | Unreliable results. | Provide templates and review by a QA engineer. Version every rule. |
| Test suite results are unstable or flaky. | False failures. | Capture retries and flake markers. Show the history of each test. |
| Scope creep to scheduled runs, CI/CD, and Jira writes. | Delayed MVP. | Keep these in the post-MVP list. Require a change request for any addition. |

---

## 11. Open Questions

1. **Data volumes:** How many rows and tables are in the largest schemas? (Needed for NFR-5 and the sampling decision.)
2. **Approval policy:** Can the manager accept known failures on the sign-off report, or must every check pass?
3. **Business rules owner:** Who writes and approves business-rule assertions?
4. **Sandbox readiness:** Does a PostgreSQL sandbox that mirrors the target schema already exist?
5. **Test suite details:** What framework do the lower-env test suites use, and how are they invoked today?
6. **Hosting confirmation:** The VM or server for the tool must be provisioned. Who owns that?
7. **Pilot selection:** Which 2 to 3 engineers form the pilot group?
8. **Jira export format:** Is a PDF or CSV attachment enough for Jira, or does a specific template need to be matched?

---

## 12. Glossary

- **Sandbox:** A non-production PostgreSQL environment where migration scripts are executed safely.
- **Lower environment:** A non-production environment (dev, QA, or staging) used for application testing.
- **Readiness sign-off:** A manager-approved report confirming that a migration run passed QA.
- **Business-rule assertion:** A SQL query that must return zero rows (or an expected result) to pass.
