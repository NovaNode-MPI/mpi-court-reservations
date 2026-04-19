# QA Test Cases – Reservations (M1)

## Scope

This document defines the manual QA test cases for the reservation flow in M1.

Focus areas:

- valid reservation creation
- invalid reservation intervals
- overlap protection
- ownership / authorization
- unauthorized access to protected endpoints

## Preconditions

Before running the cases:

1. Backend is running
2. Database is available
3. At least one facility exists in the database
4. Use Postman or Thunder Client to send requests
5. Base URL:
   ```text
   http://127.0.0.1:8000
   ```

## Test data

Example users:

- User A: `usera@example.com` / `password123`
- User B: `userb@example.com` / `password123`

Example valid future time slot:

- `start_time`: `2026-05-01T10:00:00Z`
- `end_time`: `2026-05-01T11:00:00Z`

Example overlapping slot:

- `start_time`: `2026-05-01T10:30:00Z`
- `end_time`: `2026-05-01T11:30:00Z`

## Authentication setup in Postman / Thunder Client

### Step 1: Register users

#### Request

```http
POST /auth/register
Content-Type: application/json
```

#### Body

```json
{
  "email": "usera@example.com",
  "password": "password123"
}
```

Repeat for:

```json
{
  "email": "userb@example.com",
  "password": "password123"
}
```

### Step 2: Log in and save tokens

#### Request

```http
POST /auth/login
Content-Type: application/json
```

#### Body

```json
{
  "email": "usera@example.com",
  "password": "password123"
}
```

Save the returned `access_token` as **User A token**.

Repeat for User B and save **User B token**.

### Step 3: Use Bearer token on protected endpoints

For protected endpoints, send:

```http
Authorization: Bearer <token>
```

---

## TC-01 – Valid create reservation

### Goal

Verify that a valid reservation can be created.

### Request

```http
POST /reservations
Authorization: Bearer <User A token>
Content-Type: application/json
```

### Body

```json
{
  "facility_id": 1,
  "start_time": "2026-05-01T10:00:00Z",
  "end_time": "2026-05-01T11:00:00Z"
}
```

### Expected result

- HTTP status: `201`
- Response contains:
  - `facility_id = 1`
  - correct `user_id`
  - `status = "active"`

---

## TC-02 – Reject invalid interval (`start_time >= end_time`)

### Goal

Verify that an invalid interval is rejected.

### Request

```http
POST /reservations
Authorization: Bearer <User A token>
Content-Type: application/json
```

### Body

```json
{
  "facility_id": 1,
  "start_time": "2026-05-01T11:00:00Z",
  "end_time": "2026-05-01T10:00:00Z"
}
```

### Expected result

- HTTP status: `400`
- Response body includes:
  - `error_code = "bad_request"`
  - message indicating `start_time must be earlier than end_time`

---

## TC-03 – Reject overlap on same facility

### Goal

Verify that overlapping reservations for the same facility are rejected.

### Preconditions

A valid reservation already exists for facility `1`:

- `2026-05-01T10:00:00Z` to `2026-05-01T11:00:00Z`

### Request

```http
POST /reservations
Authorization: Bearer <User A token>
Content-Type: application/json
```

### Body

```json
{
  "facility_id": 1,
  "start_time": "2026-05-01T10:30:00Z",
  "end_time": "2026-05-01T11:30:00Z"
}
```

### Expected result

- HTTP status: `409`
- Response body includes:
  - `error_code = "conflict"`
  - message indicating the time slot is already booked for this facility

---

## TC-04 – User B cannot cancel User A reservation

### Goal

Verify ownership protection on reservation cancel.

### Preconditions

User A has created a reservation and its `id` is known.

### Request

```http
DELETE /reservations/{reservation_id}
Authorization: Bearer <User B token>
```

### Expected result

- HTTP status: `403`
- Response body includes:
  - `error_code = "forbidden"`
  - message = `Forbidden`

---

## TC-05 – User B list does not include User A reservations

### Goal

Verify that reservation listing is isolated per authenticated user.

### Preconditions

- User A has at least one reservation
- User B has a different reservation or no reservations

### Request

```http
GET /reservations
Authorization: Bearer <User B token>
```

### Expected result

- HTTP status: `200`
- Response contains only User B reservations
- User A reservation IDs do not appear in the list

---

## TC-06 – Unauthorized create reservation

### Goal

Verify that protected endpoints reject unauthenticated access.

### Request

```http
POST /reservations
Content-Type: application/json
```

### Body

```json
{
  "facility_id": 1,
  "start_time": "2026-05-01T12:00:00Z",
  "end_time": "2026-05-01T13:00:00Z"
}
```

### Expected result

- HTTP status: `401`

---

## TC-07 – Unauthorized list reservations

### Goal

Verify that reservation listing requires authentication.

### Request

```http
GET /reservations
```

### Expected result

- HTTP status: `401`

---

## TC-08 – Unauthorized get reservation by id

### Goal

Verify that reservation details require authentication.

### Request

```http
GET /reservations/{reservation_id}
```

### Expected result

- HTTP status: `401`

---

## TC-09 – Unauthorized cancel reservation

### Goal

Verify that reservation cancel requires authentication.

### Request

```http
DELETE /reservations/{reservation_id}
```

### Expected result

- HTTP status: `401`

---

## Notes for Postman / Thunder Client

### In Postman

- Create a collection named `MVP Reservations QA`
- Save one request per test case
- Save User A token and User B token as collection or environment variables
- Reuse `{{baseUrl}}` = `http://127.0.0.1:8000`

### In Thunder Client

- Create a collection for the reservation tests
- Save separate requests for each case
- Reuse the same base URL
- Manually paste Bearer tokens into the Authorization tab

## Pass criteria

The reservation flow passes QA for M1 if:

- valid reservation creation works
- invalid intervals are rejected
- overlaps are rejected
- ownership rules are enforced
- protected reservation endpoints require authentication
