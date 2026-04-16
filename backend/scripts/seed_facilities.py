from decimal import Decimal

from app.db import SessionLocal
from app import models


def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(models.Facility).count()
        if existing > 0:
            print("Facilities already exist. Skipping seed.")
            return

        facilities = [
            models.Facility(
                name="Teren Tenis Central",
                type="tennis",
                location="Brasov, Complex Sportiv Central",
                image_url="/images/facilities/tennis-central.png",
                prices=[
                    models.FacilityPrice(duration="1 hour", price=Decimal("80.00")),
                    models.FacilityPrice(duration="2 hours", price=Decimal("150.00")),
                ],
            ),
            models.Facility(
                name="Teren Tenis Arena Nord",
                type="tennis",
                location="Brasov, Arena Nord",
                image_url="/images/facilities/tennis-arena-nord.png",
                prices=[
                    models.FacilityPrice(duration="1 hour", price=Decimal("85.00")),
                    models.FacilityPrice(duration="2 hours", price=Decimal("160.00")),
                ],
            ),
            models.Facility(
                name="Teren Fotbal Field A",
                type="football",
                location="Brasov, Stadionul Municipal",
                image_url="/images/facilities/football-field-a.png",
                prices=[
                    models.FacilityPrice(duration="1 hour", price=Decimal("180.00")),
                    models.FacilityPrice(duration="2 hours", price=Decimal("340.00")),
                ],
            ),
            models.Facility(
                name="Sala Sport Indoor Pro",
                type="basketball",
                location="Brasov, Sala Polivalenta",
                image_url="/images/facilities/basketball.png",
                prices=[
                    models.FacilityPrice(duration="1 hour", price=Decimal("140.00")),
                    models.FacilityPrice(duration="2 hours", price=Decimal("260.00")),
                ],
            ),
            models.Facility(
                name="Court MultiSport South",
                type="multisport",
                location="Brasov, Zona Tractorul",
                image_url="/images/facilities/multisport.png",
                prices=[
                    models.FacilityPrice(duration="1 hour", price=Decimal("100.00")),
                    models.FacilityPrice(duration="2 hours", price=Decimal("190.00")),
                ],
            ),
        ]

        db.add_all(facilities)
        db.commit()
        print("Seeded facilities with prices and images.")
    finally:
        db.close()


if __name__ == "__main__":
    main()