# MPI – Sports Facility Reservations (NovaNode)

A simple booking platform that allows users to reserve sports facilities (courts/fields) for a time interval, preventing overlapping reservations.

---

## 1. Description & Objectives

### Description

Sports facilities are often booked informally (messages/phone calls), which can lead to double bookings, lack of transparency, and difficulties in tracking reservations.

### Objectives

- Provide a clear reservation flow: register/login → browse facilities → book → view/cancel.
- Prevent overlapping reservations for the same facility and time interval.
- Use a clean ALM process (Issues, GitHub Projects, PR reviews, CI/CD, Docker, deployment).

### Target Users

- Users who want to book a sports facility (tennis court, football field, etc.)
- Facility managers (future enhancement) who want an overview of bookings

---

## 2. Team & Roles

| Student Name      | Champion Role           | GitHub Username     |
| ----------------- | ----------------------- | ------------------- |
| Alexandra Scarlat | Backend                 | @AlexandraScarlat15 |
| Andra Stoica      | Frontend                | @andrastefania      |
| Elena Strugari    | DevOps / Infrastructure | @Elena-Strugari     |
| Mario Voicu       | QA / Testing            | @MarioAndreiVoicu   |

Each champion owns the deliverables of their area. Implementation can be shared across the team.

---

## 3. Architecture & Technologies

- **Backend:** Python FastAPI (OpenAPI/Swagger)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Tooling:** Vite
- **Styling:** Plain CSS

### DevOps & Infrastructure

- **CI/CD:** GitHub Actions
- **Docker:** Docker Compose (API + PostgreSQL)
- **Deploy:** Render (planned MVP deployment platform)

## Testing

For M1, the project uses:

- **Unit tests**: limited use for small isolated logic/helpers where appropriate
- **Integration tests**: main automated testing level for the backend API
- **E2E / smoke testing**: manual end-to-end validation of the MVP flow

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

### Current automated coverage

The current automated focus is backend integration testing, including:

- authentication flows
- reservation creation
- overlap rejection
- invalid interval rejection
- ownership/authorization rules
- listing only the authenticated user’s reservations

### Minimum MVP smoke flow

1. Register a new user
2. Log in
3. Open the facilities page
4. Verify facilities are displayed
5. Create a reservation
6. Open **My Reservations**
7. Verify the reservation is visible
8. Cancel the reservation
9. Verify the reservation status/behavior is updated correctly

---

## 4. Core Functionalities

The current or planned application features include:

- user registration and login
- facility listing and browsing
- reservation creation for a selected time slot
- prevention of overlapping reservations
- viewing existing reservations
- cancellation of reservations
- API documentation through Swagger/OpenAPI

---

## 5. Local Setup (How to run the project)

### Prerequisites

Before running the project locally, make sure you have:

- **Docker Desktop**
- **Python** installed locally if you want to run the backend outside Docker
- the required backend dependencies installed in your local Python environment when using `make migrate` or `make run`

### Run with Docker Compose

Clone the repository and start the local services:

```bash
git clone https://github.com/NovaNode-MPI/mpi-court-reservations.git
cd mpi-court-reservations
make up
```

### Backend environment setup

Before running the backend locally, create a local environment file:

```bash
cp backend/.env.example backend/.env
```
