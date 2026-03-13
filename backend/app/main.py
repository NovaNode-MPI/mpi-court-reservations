from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.reservations import router as reservations_router

app = FastAPI(title="MPI Court Reservations")
app.include_router(auth_router)
app.include_router(me_router)
app.include_router(reservations_router)


@app.get("/health")
def health():
    return {"status": "ok"}