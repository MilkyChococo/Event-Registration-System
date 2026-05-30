# Test Plan

## Objective

Verify that the event registration system satisfies its functional requirements and provides enough evidence for coursework submission.

## Test levels

### Unit tests

Purpose:

- validate pure business rules
- validate security helpers
- validate service responses for edge cases

Examples:

- password hashing and verification
- duplicate registration prevention
- capacity enforcement

### Integration and API tests

Purpose:

- verify routes, cookies, database changes, and role checks

Examples:

- register then login
- register for event then cancel
- admin can create event
- normal user cannot access admin routes

### End-to-end tests with Playwright

Purpose:

- verify critical user flows through the browser UI

Smoke set:

- login as seeded student and redirect to dashboard
- open a dedicated event detail page
- register and cancel a registration from the detail page

Critical regression set:

- admin creates event
- forgot password updates credentials
- attendee visibility restricted to admins

## Entry criteria

- app starts successfully
- seeded data available
- no unresolved blocker on current sprint stories

## Exit criteria

- all unit and integration tests pass
- all smoke tests pass
- no blocker or critical defects open for demo scope

## Environment

- local development on Python 3.13
- SQLite for lightweight reproducible testing
- GitHub Actions for CI
- Chromium via Playwright for E2E

## Test schedule

The testing work is planned from 26/01 to 02/05. Each week includes one or two working sessions depending on the scope and current project progress.

| Week | Date range | Sessions | Main work |
| --- | --- | --- | --- |
| 1 | 26/01 - 01/02 | 1 session | Review requirements, define test scope, identify critical user flows |
| 2 | 02/02 - 08/02 | 1 session | Prepare test environment, seeded data, and basic test checklist |
| 3 | 09/02 - 15/02 | 2 sessions | Design unit test cases for authentication, validation, and core business rules |
| 4 | 16/02 - 22/02 | 1 session | Implement and run initial unit tests, record early defects |
| 5 | 23/02 - 01/03 | 2 sessions | Design API and integration test cases for login, event, registration, and admin routes |
| 6 | 02/03 - 08/03 | 1 session | Execute integration tests and verify database changes, cookies, and permissions |
| 7 | 09/03 - 15/03 | 2 sessions | Create Playwright smoke tests for login, dashboard, event detail, register, and cancel flows |
| 8 | 16/03 - 22/03 | 1 session | Run E2E smoke tests, collect screenshots or traces for failed scenarios |
| 9 | 23/03 - 29/03 | 2 sessions | Expand regression tests for admin event creation, forgot password, and attendee visibility |
| 10 | 30/03 - 05/04 | 1 session | Review failed cases, update defect log, and retest fixed items |
| 11 | 06/04 - 12/04 | 2 sessions | Complete system test cases and validate major workflows from the user perspective |
| 12 | 13/04 - 19/04 | 1 session | Update traceability matrix and confirm coverage against requirements |
| 13 | 20/04 - 26/04 | 2 sessions | Final regression run, verify no blocker or critical defects remain for demo scope |
| 14 | 27/04 - 02/05 | 1 session | Archive test evidence, finalize lab report files, and prepare submission summary |

## Evidence to archive

- unittest output
- Playwright HTML report
- screenshots for failed tests if any
- traceability matrix
- defect log
