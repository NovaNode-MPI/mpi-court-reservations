# DevOps Plan

## Goal
Define the MVP approach for CI/CD, Docker-based local development, and cloud deployment.

## Chosen deployment platform
We will use **Render** as the initial deployment platform for the MVP.

## Why Render
- Simple GitHub integration
- Good fit for small MVP deployments
- Works well with Docker-based services
- Easy to configure environment variables and deploy settings
- Suitable for backend API deployment with PostgreSQL

## CI/CD plan

### CI provider
We will use **GitHub Actions**.

### CI triggers
- Pull requests targeting `main`
- Pushes to `main`

### Minimum CI jobs
- Backend tests

### Optional follow-up CI jobs
- Frontend build
- Frontend lint

## Deployment plan

### Deploy trigger
- Deploy after merge to `main`

### Planned production setup
- Backend API deployed as a cloud web service
- PostgreSQL deployed as a managed database
- Frontend deployment can be added in a follow-up step if needed

## Local Docker approach

### Docker strategy
For local development, the project uses Docker Compose with:
- API
- PostgreSQL database

The frontend can continue to run locally outside Docker for now.

### Local run
```bash
docker compose up --build