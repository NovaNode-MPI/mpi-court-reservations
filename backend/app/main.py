from fastapi import FastAPI

app = FastAPI(title="MPI Court Reservations")

@app.get("/health")
def health():
    return {"status": "ok"}