from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import get_db
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.reservations import router as reservations_router
from app.routers.facilities import router as facilities_router

from contextlib import asynccontextmanager
from fastapi import FastAPI
from env_validation import validate_env

validate_env()

app = FastAPI(title="MPI Court Reservations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(auth_router)
app.include_router(me_router)
app.include_router(reservations_router)
app.include_router(facilities_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "db": "unavailable"},
        )
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_env()
    yield


app = FastAPI(lifespan=lifespan)