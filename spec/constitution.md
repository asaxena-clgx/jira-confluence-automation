# Project Constitution: Jira/Confluence Automation

This constitution defines the principles and non-negotiable constraints that every specification, plan, task, and implementation in this project must follow. Later SpecKit phases (`/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) must comply with it. If a requirement conflicts with this document, amend the constitution first.

## 1. Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Frontend | React 18 + Vite | Single-page app. Built and served with Vite. |
| Backend | Node.js (LTS) + Express | REST API for the frontend and for automation jobs. |
| Database | PostgreSQL 15 | Runs in Docker. Schema changes go through versioned migrations. |
| Containers | Docker + Docker Compose | Local development database and service orchestration. |
| Language | JavaScript or TypeScript (chosen in Phase 0, applied consistently) | Use one language choice across frontend and backend unless the plan justifies otherwise. |

Do not add a technology outside this table without an amendment to this constitution.

## 2. Core Principles

### 2.1 Specification First
- No feature is implemented without an approved `spec.md`.
- Plans and tasks must trace back to numbered requirements in the spec.
- Ambiguities are resolved through `/speckit.clarify` and written back into the spec, not assumed in code.

### 2.2 Simplicity
- Prefer the smallest design that satisfies the current spec.
- Do not build for speculative future needs (YAGNI).
- Avoid new abstractions, layers, or dependencies unless a requirement needs them.

### 2.3 Test-Driven Quality
- Every backend endpoint and every automation workflow has automated tests.
- Integration tests for PostgreSQL run against the Dockerized PostgreSQL 15 instance, not mocks.
- Jira and Confluence calls are tested with recorded fixtures or a dedicated test site. Tests never call production Atlassian instances.
- A task is not complete until its tests pass.

### 2.4 Security by Default
- Jira and Confluence credentials (API tokens, emails, site URLs) are read from environment variables or a secrets manager. They are never committed to source control.
- Commit `.env.example` with placeholder values only. `.env` is listed in `.gitignore`.
- Apply least privilege to Atlassian API tokens. Request only the scopes the feature needs.
- Validate and sanitize all input at the API boundary. Use parameterized queries for all PostgreSQL access.
- Log errors without logging secrets, tokens, or personal data.

### 2.5 Reliable Integrations
- All calls to Jira and Confluence handle rate limits (HTTP 429) with backoff and retry.
- External calls have timeouts.
- Automation jobs are idempotent. Re-running a job must not create duplicate issues or pages.
- Partial failures are reported with enough detail to resume or retry.

### 2.6 Reproducible Environments
- The local environment starts with `docker compose up`. No manual database setup is required.
- Pin the Node.js version (for example, through `.nvmrc` or `engines`) and the PostgreSQL image tag (`postgres:15`).
- Lockfiles (`package-lock.json` or equivalent) are committed.

### 2.7 Clear Code
- Use consistent formatting and linting across frontend and backend.
- Keep modules small and single-purpose.
- Comment only code that needs clarification. Do not comment obvious code.

## 3. Architecture Constraints

- **Separation of layers:** React components call the Express API only. They never access PostgreSQL or Atlassian APIs directly.
- **Backend structure:** routes handle HTTP only. Services contain business logic. Repositories or data-access modules handle PostgreSQL. Atlassian clients are isolated in their own module.
- **Database access:** schema changes are versioned migrations. Manual schema edits are not allowed.
- **Configuration:** all environment-specific settings come from environment variables.

## 4. Quality Gates

Before a task or feature is marked done:

1. Linting and formatting pass for the changed code.
2. Unit and integration tests pass.
3. The app starts locally with `docker compose up` and the frontend builds with `vite build`.
4. No secrets are present in the diff.
5. Relevant documentation (README, API notes, or spec sections) is updated.

## 5. Out of Scope Without Amendment

- Storing Jira or Confluence content in PostgreSQL beyond what a spec explicitly requires.
- Writing to production Atlassian instances from development or test environments.
- Replacing the stack listed in Section 1.
- Adding authentication providers or user-management systems not named in a spec.

## 6. Governance

- This constitution takes precedence over other project documents when they conflict.
- Changes require a written rationale and must be recorded in the Amendment Log below.
- Each feature plan includes a "Constitution Check" section confirming compliance with Sections 1 to 4.

## Amendment Log

| Version | Date | Change | Rationale |
|---|---|---|---|
| 1.0.0 | 2026-11-18 | Initial constitution | Project kickoff |
