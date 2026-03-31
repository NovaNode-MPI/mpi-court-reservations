from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app import schemas
from app.config import CORS_ORIGINS
from app.db import get_db
from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.reservations import router as reservations_router
from app.routers.facilities import router as facilities_router

app = FastAPI(title="MPI Court Reservations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


def _default_error_code(status_code: int) -> str:
    mapping = {
        400: "bad_request",
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "validation_error",
        500: "internal_server_error",
        503: "service_unavailable",
    }
    return mapping.get(status_code, "unknown_error")


def _error_response(
    status_code: int,
    message: str,
    details=None,
    error_code: str | None = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    payload = schemas.ErrorResponse(
        error_code=error_code or _default_error_code(status_code),
        message=message,
        details=details,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(),
        headers=headers,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "message" in exc.detail:
        return _error_response(
            status_code=exc.status_code,
            error_code=exc.detail.get("error_code"),
            message=exc.detail["message"],
            details=exc.detail.get("details"),
            headers=exc.headers,
        )

    if isinstance(exc.detail, str):
        return _error_response(
            status_code=exc.status_code,
            message=exc.detail,
            details=None,
            headers=exc.headers,
        )

    return _error_response(
        status_code=exc.status_code,
        message="Request failed",
        details=exc.detail,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return _error_response(
        status_code=422,
        error_code="validation_error",
        message="Request validation failed",
        details=exc.errors(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return _error_response(
        status_code=500,
        error_code="internal_server_error",
        message="Internal server error",
        details=None,
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
        return _error_response(
            status_code=503,
            error_code="service_unavailable",
            message="Database unavailable",
            details=None,
        )