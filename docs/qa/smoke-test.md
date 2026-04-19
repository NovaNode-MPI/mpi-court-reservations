# QA Smoke Test Checklist (M1)

## Scope

This checklist is used for quick MVP validation after important changes or before a release/demo.

The goal is to confirm that the main user flow still works end to end.

## Preconditions

Before running the smoke test:

1. Backend is running
2. Database is available
3. Frontend is running
4. At least one facility exists in the database
5. Use a fresh test user if possible

Base URLs:

- Frontend: `http://localhost:5173`
- Backend: `http://127.0.0.1:8000`

---

## ST-01 – Register new user

### Action

Create a new user account from the frontend or via `POST /auth/register`.

### Expected result

- Status code: `201`
- User is created successfully
- Response contains:
  - `id`
  - `email`
  - `created_at`

### Validation points

- registration does not return an error
- duplicate email should not be used for this smoke test
- the created user can be used in the next steps

---

## ST-02 – Log in and capture token

### Action

Log in with the new user via frontend or `POST /auth/login`.

### Expected result

- Status code: `200`
- Response contains:
  - `access_token`
  - `token_type = bearer`

### Validation points

- login succeeds with the registered credentials
- a valid token is returned
- if using the frontend, the user is redirected into the app

---

## ST-03 – Access `/me` with token

### Action

Call:

```http
GET /me
Authorization: Bearer <token>
```

### Expected result

- Status code: `200`
- Response contains the authenticated user data

### Validation points

- returned email matches the logged-in user
- protected endpoint accepts the token
- request fails with `401` if the token is missing or invalid

---

## ST-04 – List facilities

### Action

Call:

```http
GET /facilities
```

or open the facilities page in the frontend.

### Expected result

- Status code: `200`
- At least one facility is returned/displayed

### Validation points

- facilities are visible
- returned/displayed facility data is not empty
- user can identify a facility to use in the reservation test

---

## ST-05 – Create reservation

### Action

Create a reservation for a valid future time slot using:

- frontend flow, if available
- or `POST /reservations`

Example request:

```http
POST /reservations
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "facility_id": 1,
  "start_time": "2026-05-01T10:00:00Z",
  "end_time": "2026-05-01T11:00:00Z"
}
```

### Expected result

- Status code: `201`
- Response contains:
  - reservation `id`
  - correct `user_id`
  - correct `facility_id`
  - `status = "active"`

### Validation points

- reservation is created successfully
- the chosen slot is valid
- no overlap/conflict error is returned for a free slot

---

## ST-06 – Confirm reservation appears in My Reservations

### Action

Open the **My Reservations** page in the frontend or call:

```http
GET /reservations
Authorization: Bearer <token>
```

### Expected result

- Status code: `200`
- The newly created reservation appears in the user’s reservation list

### Validation points

- reservation ID appears in the response or UI
- reservation belongs to the logged-in user
- reservation data matches the slot created in ST-05

---

## Optional follow-up check – Cancel reservation

### Action

Cancel the created reservation from the frontend or via:

```http
DELETE /reservations/{reservation_id}
Authorization: Bearer <token>
```

### Expected result

- Status code: `200`
- Reservation status changes to `canceled`

### Validation points

- cancel action succeeds for the owner
- reservation is no longer treated as active
- ownership rules still apply

---

## Pass criteria

The smoke test passes if all core steps succeed:

1. user can register
2. user can log in
3. `/me` works with token
4. facilities can be listed
5. reservation can be created
6. reservation appears in My Reservations

## Notes

- Use a fresh user and a future time slot when possible
