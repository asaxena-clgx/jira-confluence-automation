# Implementation Backlog: DB Migration QA Automation Tool

Source: [project_spec.md](/Users/akash_saxena1/Desktop/hello-genai/project_spec.md)

## How to Read This Backlog

- Phases map to the spec's delivery phases (Section 8). Spec phases 1-4 are in **Core Features**. Spec phase 5 is in **Integration**. Spec phase 6 (reporting) is in **Core Features** because the report generator depends only on stored results. Spec phase 7 (pilot) is in **Testing**.
- Priority: connections and the sandbox safety guard (FR-1, FR-3) come first, because the production guard is the top risk (spec Section 10).
- Each task names its requirement ID (FR-x, NFR-x) so it can be traced back to the spec.
- Tasks are sized to roughly 0.5 to 2 days. Dependencies are listed as `after:` references.

---

## Phase 1: Setup (Spec Phase 0, Week 1)

### 1.1 Stack and Environment
- [x] Confirm Python 3.12+ stack with FastAPI, Typer, and PostgreSQL metadata store (owner confirmed; spec Section 9, assumption 1)
- [x] Create the project repository (already done in this repo)
- [x] Set up the development environment (`.venv`, pinned `requirements-dev.txt`) (already done)
- [ ] Add runtime dependencies to a pinned manifest: `python-oracledb`, `psycopg`, `fastapi`, `typer`, `jinja2`, `weasyprint`, `pytest`
- [ ] Choose and document the package layout for the tool (for example, `qa_tool/` package) alongside the existing `status_report.py`

### 1.2 Repository and CI Basics
- [ ] Confirm `.gitignore` covers `.env`, secrets files, `reports/*.pdf`, and any local evidence output (NFR-2)
- [ ] Add a pytest configuration (`pytest.ini` or `pyproject.toml`) with separate markers for unit, integration, and sandbox tests
- [ ] Add a lint and type-check configuration (ruff and mypy or pyright)
- [ ] Add a CI workflow that runs lint, type check, and unit tests on every push (manual triggers only for runs; CI here is for the tool's own code, not for migration runs)

### 1.3 Environment Profiles and Accounts
- [ ] Define the `Environment` profile schema: id, name, type (`source`, `target`, `sandbox`, `lower_env`), connection_ref, `is_production` (FR-1.1)
- [ ] Create a profile template file that holds no secrets (for example, `profiles.example.toml`) (FR-1.4)
- [ ] Request read-only Oracle service account for source (FR-1.2, spec Assumption 6)
- [ ] Request read-only PostgreSQL service account for target (FR-1.2, spec Assumption 6)
- [ ] Request PostgreSQL sandbox account with write access, on a separate network path from production (FR-1.3, NFR-1)
- [ ] Confirm whether a sandbox that mirrors the target schema already exists (spec Open Question 4)

### 1.4 Data Volume Measurement
- [ ] Query source Oracle for row counts and sizes of every table in scope (spec Open Question 1)
- [ ] Record results in a table with table name, row count, size, and largest-table flag
- [ ] Agree on the NFR-5 full row-count window with the team using these measurements
- [ ] Decide whether the sampling question (spec Section 2.2) needs a re-check before the pilot

---

## Phase 2: Core Features (Spec Phases 1-4 and 6)

Work in the order below. Connections and the sandbox guard come first.

### 2.1 Connections and Connection Testing (FR-1, NFR-2)
- [ ] Implement a secrets loader that reads credentials from environment variables or a secrets manager; fail if a credential is found in a config file (FR-1.4)
- [ ] Implement an Oracle connector using `python-oracledb` with read-only session enforcement (FR-1.2)
- [ ] Implement a PostgreSQL connector using `psycopg` with read-only session enforcement for source and target (FR-1.2)
- [ ] Implement a connection test that returns status and latency for each profile (FR-1.5) — after: 2.1 connectors
- [ ] Add unit tests for the secrets loader, using a fake secret store

### 2.2 Production Guard and Connector Isolation (FR-3.1, NFR-1, Section 6.3)
- [ ] Implement a guard that rejects any write statement on a profile whose type is not `sandbox` (FR-3.1)
- [ ] Implement a guard that refuses to run scripts on any profile where `is_production` is true or unknown; default to refusing
- [ ] Make the guard a single module with no alternate code paths for execution (code review required per spec Section 10)
- [ ] Add tests that attempt writes against source, target, lower_env, and a profile marked production; each must be refused
- [ ] Add tests that confirm writes succeed only against a profile marked sandbox
- [ ] Add a read-only session check on source and target connectors that fails the connection if write privilege is detected (NFR-1) — after: 2.1 connectors

### 2.3 Check Engine Interface (NFR-10, Section 6.3)
- [ ] Define the `Check` interface: `run(context) -> CheckResult`
- [ ] Define the `CheckResult` model with status (Pass, Fail, Warning, Error), details (JSON), and evidence reference (FR-4.8)
- [ ] Implement a check registry so new checks register without changes to the run engine (NFR-10) — after: 2.3 interface
- [ ] Implement a run context object carrying connections, thresholds, and configuration (FR-4.9)
- [ ] Add a unit test that registers a dummy check and confirms the engine runs it without engine changes

### 2.4 Post-Execution Checks: Row Count (FR-4.1)
- [ ] Implement a full row-count comparison check for every table in scope (default is full comparison)
- [ ] Store counts and per-table differences, not row values (NFR-4)
- [ ] Return Warning or Fail based on configurable threshold per table (FR-4.9) — after: 2.4 row count
- [ ] Add a test with matching counts (Pass), a mismatch (Fail), and a missing table (Error)

### 2.5 Post-Execution Checks: Schema Diff (FR-4.2)
- [ ] Read tables, columns, data types, indexes, constraints, and sequences from Oracle and PostgreSQL catalogs
- [ ] Compute the diff and report differences by object and category
- [ ] Add a test that covers a missing index, a renamed column, and a missing sequence

### 2.6 Data Type Mapping Validation (FR-2.3, FR-4.3)
- [ ] Create the approved Oracle-to-PostgreSQL type mapping table as a versioned config file (spec Section 4, FR-2.3)
- [ ] Get the mapping table approved by the team (blocks this task)
- [ ] Implement a check that compares actual target column types with the approved mapping
- [ ] Add a test that flags an unapproved mapping and passes an approved one

### 2.7 Null, PK, FK, and Constraint Checks (FR-4.4)
- [ ] Implement a check that verifies PK and FK constraints exist on the target and match the source
- [ ] Implement a check that counts NULL violations on columns declared NOT NULL in source
- [ ] Implement a check that verifies CHECK and UNIQUE constraints exist on the target
- [ ] Add tests for each check using a small fixture schema

### 2.8 Script Validation: Linter (FR-2.1, FR-2.2, FR-2.4)
- [ ] Choose the parser approach for Oracle SQL and PL/SQL (for example, `sqlglot` with Oracle dialect) and record the decision
- [ ] Create a starter rule set for Oracle-specific syntax that does not run on PostgreSQL (for example, `NVL`, `ROWNUM`, `CONNECT BY`, `DUAL`, `VARCHAR2`, `NUMBER`)
- [ ] Give each rule an ID, a severity, and a description
- [ ] Report each finding with script name, line number, rule ID, and severity (FR-2.4)
- [ ] Make rules pluggable so engineers can add rules without editing the linter core (spec Section 10)
- [ ] Add tests with one passing and one failing script per rule

### 2.9 Sandbox Execution (FR-3)
- [ ] Implement script execution against the sandbox profile only, using the guard from 2.2 — after: 2.2 guard
- [ ] Record `ScriptExecution` fields: script name, script hash, started_at, ended_at, status, output reference (FR-3.2)
- [ ] Stop on first error by default; add a `--continue-on-error` option (FR-3.3)
- [ ] Implement a reset or re-seed step that restores the sandbox to a known state (FR-3.4)
- [ ] Add a test that confirms a reset makes two consecutive runs produce the same result
- [ ] Add an integration test that runs a script against a disposable local PostgreSQL sandbox

### 2.10 Business-Rule Assertions (FR-4.5)
- [ ] Define the `BusinessRule` model: id, name, SQL, expected result, owner, version
- [ ] Implement execution of a rule expecting zero rows (default) or a defined expected result
- [ ] Store each rule version so a run records which version it used
- [ ] Create a rule template file for engineers to start from (spec Section 10, rule inconsistency risk)
- [ ] Add a test that a rule returning rows fails and a rule returning none passes

### 2.11 Performance Regression Checks (FR-4.6)
- [ ] Define a query set config: query text, source timing, target timing, threshold (FR-4.9)
- [ ] Time each query on source and target with a fixed number of repetitions
- [ ] Flag results that exceed the configured threshold as Warning or Fail
- [ ] Add a test that a slow target query is flagged and a fast one passes

### 2.12 Test Suite Runner (FR-4.7, Spec Phase 4)
- [ ] Define how a lower-environment suite is invoked (command, working directory, environment) — blocked until spec Open Question 5 is answered
- [ ] Implement the runner that invokes the suite and captures exit code, pass/fail counts, and logs
- [ ] Attach logs to the run as evidence
- [ ] Capture retries and flake markers, and store history per test (spec Section 10, flaky tests risk)
- [ ] Add a test using a small dummy suite that passes, fails, and times out

### 2.13 Run Model and Lifecycle (FR-5.2, FR-5.3, Section 6.3)
- [ ] Implement the `MigrationRun` model with name, version, owner, environment, status, created_at, and jira_ref (FR-8.3)
- [ ] Implement the run lifecycle: `Draft -> Validated -> Sandbox Executed -> Checked -> Pending Approval -> Approved -> Signed Off`
- [ ] Reject any transition that skips a state; add tests for each invalid transition
- [ ] Implement re-run with the same configuration as a new version of the run (FR-5.3)

### 2.14 Run Orchestrator and Background Worker (Section 6.2, NFR-6)
- [ ] Choose the worker approach (RQ, Celery, or a simple worker process) and record the decision
- [ ] Implement the orchestrator that runs validation, sandbox execution, and checks in order for one run
- [ ] Support a small number of concurrent runs (NFR-6)
- [ ] Add a test that a long-running check does not block other tasks

### 2.15 Metadata Store (Section 7, NFR-3)
- [ ] Create the PostgreSQL metadata schema for: `Environment`, `MigrationRun`, `ScriptExecution`, `CheckDefinition`, `CheckResult`, `BusinessRule`, `Approval`, `SignOffReport`, `User`, `AuditLog`
- [ ] Add migration scripts for the metadata schema, versioned in the repo
- [ ] Confirm at-rest encryption for the metadata store with the platform team (NFR-3)

### 2.16 Reporting: CSV and PDF Sign-Off (FR-7.3, FR-7.4, FR-7.5, FR-8.1, Spec Phase 6)
- [ ] Implement a report builder that reads only stored results (idempotent report generation, Section 6.3)
- [ ] Implement the sign-off report template in Jinja2 covering scope, checks run, results, accepted risks, and approval record (FR-7.3)
- [ ] Implement CSV export of the same report data (FR-7.4)
- [ ] Implement PDF export using WeasyPrint (FR-7.4)
- [ ] Stamp every report with a timestamp and SHA-256 checksum (FR-7.5)
- [ ] Freeze the `SignOffReport` record on sign-off so later changes are rejected (FR-7.5)
- [ ] Check that reports contain no row-level values unless evidence requires them (NFR-4)
- [ ] Add tests: checksum matches file content; frozen record rejects edits; CSV columns match the template

### 2.17 Audit Log (FR-9.3, NFR-8)
- [ ] Implement an audit writer that records user, action, target, timestamp, and payload hash
- [ ] Log every run trigger, approval, and export through the audit writer
- [ ] Add a test that each of these actions writes exactly one audit entry

---

## Phase 3: Integration (Spec Phase 5)

### 3.1 CLI (FR-5.1, Typer)
- [ ] Build the Typer CLI as a thin layer over the same service functions used by the API (Section 6.1)
- [ ] Add commands: test connection, lint scripts, run validation, execute sandbox, run checks, show run status, export report
- [ ] Add a CLI test for each command using Typer's test runner

### 3.2 REST API (FastAPI, Section 6.1)
- [ ] Set up the FastAPI application with versioned routes
- [ ] Add endpoints for connections, runs, checks, business rules, approvals, and reports
- [ ] Run long operations through the worker and return a job ID (NFR-6)
- [ ] Add API tests for each endpoint, including a rejected request for a non-sandbox write

### 3.3 Corporate SSO (FR-9.1, Assumption 7)
- [ ] Get the identity provider details (SAML or OIDC) from the platform team (Assumption 7)
- [ ] Implement the OIDC or SAML login flow
- [ ] Map SSO subject to the `User` record on first login
- [ ] Test login with the identity provider's test tenant

### 3.4 Role-Based Access Control (FR-9.2, Section 3)
- [ ] Define the manager and engineer roles, plus an optional QA engineer role (Section 3)
- [ ] Enforce engineers seeing only their own runs by default
- [ ] Enforce manager-only access to approval actions
- [ ] Add tests for each role on each protected endpoint

### 3.5 Approval Gate (FR-6)
- [ ] Block runs from proceeding until the manager approves them (FR-6.1)
- [ ] Require all mandatory checks to pass, or an explicit accepted-failure list with a recorded reason (FR-6.2)
- [ ] Record each approval with approver identity, timestamp, and comment (FR-6.3)
- [ ] Add tests: blocked without approval; approved with all checks passing; approved with accepted failures; rejected when a failure is not accepted

### 3.6 Web UI (FR-7.1, FR-7.2, Section 6.1)
- [ ] Decide server-rendered templates or React + TypeScript (Section 6.1)
- [ ] Build the team dashboard: active runs, pass/fail rates, open failures, sign-off status per phase (FR-7.1)
- [ ] Build the per-engineer view: runs, tasks, and failures (FR-7.2)
- [ ] Build the run detail page showing each check result with details and evidence
- [ ] Build the trigger-run form (FR-5.1)
- [ ] Build the approval screen for the manager
- [ ] Check the UI against the two personas in a browser (manager and engineer)

### 3.7 Jira Reference Field (FR-8.3)
- [ ] Add a manual Jira ticket reference field on the run form and in the CLI
- [ ] Confirm the tool does not call any Jira API (FR-8.2)

---

## Phase 4: Testing (Spec Phase 7 and Cross-Cutting)

### 4.1 Security Testing
- [ ] Run a test that tries to execute against a production-flagged profile through every entry point: CLI, API, and UI (FR-3.1, NFR-1)
- [ ] Confirm secrets are absent from the repo, logs, and reports (NFR-2, FR-1.4)
- [ ] Confirm TLS is enforced for API and database traffic (NFR-3)
- [ ] Confirm the SSO login flow rejects expired or tampered tokens
- [ ] Get a security review of the production guard (Section 10)

### 4.2 Performance Testing
- [ ] Time a full row-count comparison on the largest table from Phase 0 measurements (NFR-5)
- [ ] Confirm the tool supports 10 concurrent users and a small number of concurrent runs (NFR-6)

### 4.3 Pilot (Spec Phase 7)
- [ ] Confirm the pilot group of 2 to 3 engineers (spec Open Question 7)
- [ ] Run the pilot on one real migration phase against the sandbox
- [ ] Collect feedback and log defects
- [ ] Fix pilot issues and rerun the affected checks
- [ ] Measure the success metric: elapsed time from "scripts ready" to "signed off" (Section 1)
- [ ] Get pilot sign-off before rollout to all 10 engineers

### 4.4 Test Coverage of the Tool
- [ ] Confirm unit tests cover the guard, check engine, run lifecycle, approval gate, and report checksums
- [ ] Confirm integration tests run against a disposable PostgreSQL instance in CI
- [ ] Confirm every FR has at least one test referenced in its task

---

## Phase 5: Documentation

### 5.1 User Documentation
- [ ] Write a README covering install, configuration, and the first run
- [ ] Document the CLI commands with examples
- [ ] Document how to write a business-rule assertion, with the template from 2.10
- [ ] Document how to add a new check (the interface from 2.3)
- [ ] Document how to add a new lint rule (from 2.8)

### 5.2 Operations Documentation
- [ ] Write the runbook: deployment, configuration, secrets setup, and upgrades (Phase 7, NFR-9)
- [ ] Document the sandbox reset procedure (FR-3.4)
- [ ] Document the approval workflow for managers
- [ ] Document the audit log and how to query it (NFR-8)
- [ ] Document how to add an identity provider profile for SSO

### 5.3 Security and Compliance Documentation
- [ ] Document the production guard and its tests (NFR-1)
- [ ] Document the data-handling rule: counts, hashes, and identifiers only in reports (NFR-4)
- [ ] Document the assumption that data is synthetic or masked, and the trigger for re-checking it (Assumption 5)

### 5.4 Project Records
- [ ] Update [project_spec.md](/Users/akash_saxena1/Desktop/hello-genai/project_spec.md) Section 11 as each open question is answered
- [ ] Record architectural decisions (parser choice, worker choice, UI approach) in a decision log
- [ ] Update the existing [TODO.md](/Users/akash_saxena1/Desktop/hello-genai/TODO.md) progress notes as phases complete

---

## Open Questions Blocking Tasks

| Spec Q | Blocks | Task |
|---|---|---|
| Q1 Data volumes | NFR-5, sampling decision | 1.4 |
| Q2 Approval policy | Approval gate | 3.5 |
| Q3 Business-rule owner | Business-rule workflow | 2.10 |
| Q4 Sandbox readiness | Sandbox execution | 1.3, 2.9 |
| Q5 Test suite framework | Test suite runner | 2.12 |
| Q6 Hosting owner | Deployment | 5.2 |
| Q7 Pilot group | Pilot | 4.3 |
| Q8 Jira format | Export format | 2.16 |

## Out of Scope (Not in This Backlog)

Per spec Section 2.2 and 2.3: sampled row-level comparison, scheduled or CI/CD-triggered runs, Jira writes, production execution, data masking or synthesis, and non-Oracle sources.
