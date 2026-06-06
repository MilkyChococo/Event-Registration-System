# Event Registration System

EMS is a Software Verification coursework project for an Event Registration System. The project includes a working web application, SRS and test documentation, lab reports, backend verification, and Playwright end-to-end automation evidence.

## Project Overview

The system supports students and administrators in managing event participation from discovery to registration, payment, approval, and notification.

Main goals:

- provide a complete event browsing and ticket reservation flow
- support wallet balance, QR top-up, and transaction history
- allow students to submit event requests for admin review
- provide admin tools for event management and request moderation
- maintain notifications for registration, approval, rejection, and reminders
- produce verification artifacts for Software Verification coursework

## SRS Revision History

| Name | Date | Reason For Changes | Version |
| --- | --- | --- | --- |
| Truong Thien Phu | 26-Jan-2026 | Initialized the SRS document, selected the Event Registration System topic, and drafted the purpose, project scope, and initial product overview. | 0.1 |
| Truong Thien Phu; Mai Xuan Tuan | 15-Feb-2026 | Added the overall system description, user classes, operating environment, assumptions, constraints, and initial functional requirement groups. | 0.2 |
| Group 11 | 10-Mar-2026 | Completed the main system features, including authentication, event browsing, ticket reservation, wallet payment, QR top-up, event request, admin approval, notifications, and reporting requirements. | 0.3 |
| Group 11 | 31-Mar-2026 | Updated data requirements, logical data model, data dictionary, business rules, external interface requirements, and nonfunctional requirements. | 0.4 |
| Mai Xuan Tuan | 20-Apr-2026 | Added and refined analysis diagrams, requirement traceability mapping, acceptance criteria, and alignment with the planned verification artifacts. | 0.5 |
| Truong Thien Phu | 02-May-2026 | Baselined the final SRS for course submission according to the COS SRS template, with finalized Release 1.0 scope and approved requirements. | 1.0 |

## System Features

### Student Features

- sign up, sign in, sign out, and forgot password
- manage profile information, avatar, phone, address, and date of birth
- browse event dashboard and view event details
- reserve tickets with quantity validation and account-level limits
- cancel reservations and review registration history
- top up wallet balance through QR payment flow
- view billing history and payment transactions
- submit, update, resubmit, and withdraw event requests
- choose event location with a map-based location picker
- receive notification updates for event requests and approved events

### Admin Features

- sign in to the manager console
- create, update, and delete events
- review attendee information
- approve or reject student event requests
- inspect pending request queues
- review operational summaries and basic analytics
- receive notifications for newly submitted or updated requests

### Verification Features

- backend unit tests with `unittest`
- API-level tests with FastAPI `TestClient`
- Playwright smoke and critical end-to-end tests
- Lab 3 Playwright automation suite mapped to workbook-style scenarios
- course documents for SRS, test planning, traceability, and defect logging

## Technology Stack

- Frontend: HTML, CSS, vanilla JavaScript
- Backend: FastAPI
- Database: MongoDB
- Backend testing: `unittest`, FastAPI `TestClient`, `mongomock`
- E2E testing: Playwright
- Runtime scripts: PowerShell
- CI/CD: GitHub Actions

## Repository Structure

```text
app/                         FastAPI backend application
app/static/                  Browser UI assets and front-end scripts
docs/                        Coursework documents and verification artifacts
docs/document/               Main report documents, including SRS and test plan
docs/lab_report/             Lab submission reports and spreadsheets
scripts/                     Utility scripts for server startup, reports, and data setup
tests/                       Backend unit and API tests
tests/e2e/                   Playwright end-to-end test suites
.github/workflows/           GitHub Actions CI/CD workflows
docker-compose.yml           Local Docker Compose environment
Dockerfile                   App container definition
package.json                 Playwright dependencies and npm test commands
playwright.config.js         General Playwright configuration
playwright.lab3.config.js    Lab 3 Playwright configuration
requirements.txt             Python dependencies
```

## Documents and Reports

Main coursework documents are stored in `docs/document/`:

- `ERS_SRS_Report.docx`: Software Requirements Specification report
- `ERS_TestPlan_TestCaseSpecification.docx`: test plan and test case specification document

Lab reports are stored in `docs/lab_report/`:

- `ERS_Lab1_Test_Case.xls`
- `ERS_Lab2_Unit_Test_Case.xls`
- `ERS_Lab3_AutomationTool_Report.docx`
- `ERS_Lab4_System_Test_Defect_Log.xlsx`
- `ERS_Lab4_Unit_Test_Defect_Log.xls`

Supporting markdown artifacts are stored directly in `docs/`:

- `project-scope.md`
- `architecture.md`
- `backlog.md`
- `sprint-plan.md`
- `test-plan.md`
- `traceability-matrix.md`
- `defect-log.md`
- `demo-checklist.md`

## Local Setup

### 1. Create Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 2. Install Node.js Dependencies

Playwright requires Node.js and npm. After installing Node.js, run:

```powershell
npm install
npx playwright install chromium
```

If Playwright appears to stop at `100%`, wait until the command returns to the prompt. The download step may be followed by browser extraction.

## Running the System

### Option 1: Run FastAPI Directly

```powershell
python -m uvicorn app.main:app --reload --port 10104
```

Open:

```text
http://127.0.0.1:10104
```

### Option 2: Run Lab 3 Mock Server

This mode enables mock database behavior and demo seed data for stable Playwright execution.

```powershell
.\scripts\run_lab3_server.ps1
```

The script sets:

```text
APP_USE_MOCK_DB=true
APP_SEED_DEMO=true
```

### Option 3: Run with Docker Compose

```powershell
docker compose up --build
```

Services:

- app: `http://127.0.0.1:10104`
- mongo-express: `http://127.0.0.1:8088`

## Demo Accounts

When `APP_SEED_DEMO=true`, the system creates these accounts:

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@example.com` | `Admin123!` |
| Student | `student@example.com` | `Student123!` |

## Backend Testing

Run backend unit and API tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

These tests use `mongomock`, so they do not require a live MongoDB server.

## Playwright Testing

### General E2E Tests

Run all Playwright tests:

```powershell
npm run test:e2e
```

Run smoke tests:

```powershell
npm run test:e2e:smoke
```

Run critical tests:

```powershell
npm run test:e2e:critical
```

### Lab 3 Automation Tool Tests

The Lab 3 suite is located at:

```text
tests/e2e/lab3-review.spec.js
```

The Lab 3 config is located at:

```text
playwright.lab3.config.js
```

Run Lab 3 Playwright automation:

```powershell
npx playwright test --config=playwright.lab3.config.js
```

This config automatically starts the Lab 3 server through:

```text
scripts/run_lab3_server.ps1
```

Current Lab 3 scenarios:

| Scenario | Purpose |
| --- | --- |
| AUTH | Registration, invalid login validation, and successful login |
| EVDASH | Dashboard event listing and event detail navigation |
| RESERVE | Reserve one event and cancel it from the detail page |
| CAPACITY | Validate accepted quantity 5 and rejected quantity 6 |
| BILLQR | Generate QR top-up, lock form, confirm payment, and record transaction |
| REQSUB | Submit an event request and verify request notification |
| ADMINAPR | Admin approves and rejects pending requests |
| NOTIFY | Student receives approval notification with event link |

Run Lab 3 with a visible browser:

```powershell
npx playwright test --config=playwright.lab3.config.js --headed
```

Open the latest Playwright HTML report:

```powershell
npx playwright show-report
```

The Lab 3 HTML report is generated under:

```text
playwright-report/lab3/
```

## Recommended Workflow

1. Review the SRS in `docs/document/ERS_SRS_Report.docx`.
2. Review the test plan in `docs/document/ERS_TestPlan_TestCaseSpecification.docx`.
3. Install Python and Node.js dependencies.
4. Run the app locally or with `scripts/run_lab3_server.ps1`.
5. Execute backend tests.
6. Execute Playwright Lab 3 automation.
7. Use `docs/lab_report/` and `playwright-report/lab3/` as verification evidence.

## CI/CD

The GitHub Actions workflows in `.github/workflows/` run automated verification tasks such as backend tests, app startup checks, and Playwright smoke coverage.
