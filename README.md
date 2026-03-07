# MPI – Sports Facility Reservations (NovaNode)

> A simple booking platform that allows users to reserve sports facilities (courts/fields) for a time interval, preventing overlapping reservations.

## 1. Description & Objectives

### Description
Sports facilities are often booked informally (messages/phone calls), which can lead to double bookings, lack of transparency, and difficulties in tracking reservations.

### Objectives
- Provide a clear reservation flow: register/login → browse facilities → book → view/cancel.
- Prevent overlapping reservations for the same facility and time interval.
- Use a clean ALM process (Issues, GitHub Projects, PR reviews, CI/CD, Docker, deploy).

### Target Users
- Users who want to book a sports facility (tennis court, football field, etc.).
- Facility managers (future enhancement) who want an overview of bookings.

## 2. Team & Roles

| Student Name | Champion Role | GitHub Username |
|------------|---------------|----------------|
| Alexandra Scarlat | Backend | @AlexandraScarlat15 |
| Andra Stoica | Frontend | @andrastefania |
| Elena Strugari | DevOps / Infrastructure | @Elena-Strugari |
| Mario Voicu | QA / Testing | @MarioAndreiVoicu |

> Each champion owns the deliverables of their area. The implementation can be shared across the team.

## 3. Architecture & Technologies

- **Backend:** Python FastAPI (OpenAPI/Swagger)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript
- **Tooling:** Vite
- **Styling:** Plain CSS
- **Testing:** TBD (QA champion will decide)
- **CI/CD:** TBD (DevOps champion will decide)
- **Docker:** TBD (DevOps champion will decide)
- **Deploy:** TBD (DevOps champion will decide)

## 4. Local Setup (How to run the project)

> This section will be updated once Docker Compose is available.

```bash
git clone https://github.com/NovaNode-MPI/mpi-court-reservations.git
cd mpi-court-reservations
docker compose up --build
```
## Frontend Local Setup

```bash
cd frontend
npm install
npm run dev
```

This starts the frontend development server locally.

## 5. Workflow (short)

- No direct pushes to `main`
- Each task must have an Issue (no issue = no code)
- All changes go through Pull Requests
- PRs must reference issues using: `Closes #<issue-id>`
- At least 1 reviewer approval is required before merge

## 6. Project Management

- GitHub Project board: **NovaNode – Team Board**
- Milestones:
  - **M1 - MVP** (reservation flow)
  - **M2 - Enhancements**

## 7. Links

- Project board: https://github.com/orgs/NovaNode-MPI/projects/1
- Live URL: TBD (will be added after deployment)
