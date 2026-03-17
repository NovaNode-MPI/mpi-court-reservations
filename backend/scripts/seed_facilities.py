from app.db import SessionLocal
from app import models

def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(models.Facility).count()
        if existing > 0:
            print("Facilities already exist. Skipping seed.")
            return

        db.add_all([
            models.Facility(name="Court 1", type="tennis", location="MPI Gym"),
            models.Facility(name="Court 2", type="tennis", location="MPI Gym"),
            models.Facility(name="Field A", type="football", location="MPI Stadium"),
        ])
        db.commit()
        print("Seeded facilities.")
    finally:
        db.close()

if __name__ == "__main__":
    main()