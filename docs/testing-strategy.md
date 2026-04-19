# Testing Strategy (M1 - MVP)

## 1. Scope for M1

For M1, we use three testing levels:

- **Unit tests**: limited use for small isolated logic/helpers where appropriate.
- **Integration tests**: main automated testing level for the backend API.
- **E2E / smoke testing**: manual end-to-end validation of the MVP user flow.

For M1, the priority is to verify that the backend API works correctly, that the main reservation rules are enforced, and that the basic user flow can be validated from the UI.

## 2. Tools

### Unit tests

- **pytest**

### Integration tests

- **pytest**
- **FastAPI TestClient**
- **SQLite test database**
- **pytest fixtures** for isolated setup and reusable helpers

### E2E / smoke testing

- **Manual browser testing** in local development

## 3. What we test

### Authentication

- user registration with valid data
- login with valid credentials
- rejection of invalid credentials
- authenticated access to protected endpoints

### Reservations

- valid reservation creation
- rejection of overlapping reservations
- rejection of invalid time intervals
- ownership rules (a user cannot modify or cancel another user’s reservation)
- listing only the authenticated user’s reservations

### Facilities

- listing available facilities
- retrieving a facility by id

## 4. Current automated test focus

For M1, the main automated focus is **backend integration testing**.

This matches the current backend test setup, which already uses:

- `pytest`
- FastAPI `TestClient`
- a separate SQLite test database
- fixtures/helpers in `conftest.py`

Existing reservation tests already cover the main MVP backend rules:

- valid reservation creation
- overlap rejection
- invalid interval rejection
- ownership restrictions
- per-user reservation listing

## 5. How to run tests locally

### Backend automated tests

From the `backend` folder:

```bash
pytest
```

If needed, activate the virtual environment first and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

## 6. Minimum MVP smoke flow

The minimum manual E2E flow for M1 is:

1. Open the frontend application
2. Register a new user
3. Log in with that user
4. Open the facilities page
5. Verify facilities are displayed
6. Create a reservation
7. Open **My Reservations**
8. Verify the reservation is visible
9. Cancel the reservation
10. Verify the reservation status/behavior is updated correctly

## 7. Notes

- Backend integration tests are the main reliable automated testing layer for M1.
- Manual smoke testing is used for the MVP end-to-end flow.
- A fuller automated E2E setup can be added in a later milestone after the frontend reservation flow is fully completed.
