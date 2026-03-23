from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app import models
from tests.conftest import auth_headers, create_user, login_and_get_token


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def test_valid_reservation_can_be_created(client, facility):
    create_user(client, "user1@example.com")
    token = login_and_get_token(client, "user1@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = start_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    response = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time),
            "end_time": iso(end_time),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["facility_id"] == facility.id
    assert body["status"] == "active"


def test_overlapping_reservations_are_rejected(client, facility):
    create_user(client, "user1@example.com")
    token = login_and_get_token(client, "user1@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = start_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    first = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time),
            "end_time": iso(end_time),
        },
        headers=auth_headers(token),
    )
    assert first.status_code == 201

    overlap = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time + timedelta(minutes=30)),
            "end_time": iso(end_time + timedelta(minutes=30)),
        },
        headers=auth_headers(token),
    )

    assert overlap.status_code == 409
    assert overlap.json()["detail"] == "Time slot is already booked for this facility"


def test_invalid_time_interval_is_rejected(client, facility):
    create_user(client, "user1@example.com")
    token = login_and_get_token(client, "user1@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = start_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time - timedelta(minutes=30)

    response = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time),
            "end_time": iso(end_time),
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "start_time must be earlier than end_time"


def test_user_cannot_cancel_someone_elses_reservation(client, facility):
    create_user(client, "owner@example.com")
    owner_token = login_and_get_token(client, "owner@example.com")

    create_user(client, "other@example.com")
    other_token = login_and_get_token(client, "other@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = start_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    create_response = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time),
            "end_time": iso(end_time),
        },
        headers=auth_headers(owner_token),
    )
    assert create_response.status_code == 201
    reservation_id = create_response.json()["id"]

    cancel_response = client.delete(
        f"/reservations/{reservation_id}",
        headers=auth_headers(other_token),
    )

    assert cancel_response.status_code == 403
    assert cancel_response.json()["detail"] == "Forbidden"


def test_listing_reservations_returns_only_authenticated_users_reservations(client, facility):
    create_user(client, "user1@example.com")
    token1 = login_and_get_token(client, "user1@example.com")

    create_user(client, "user2@example.com")
    token2 = login_and_get_token(client, "user2@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = start_time.replace(minute=0, second=0, microsecond=0)

    first = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time),
            "end_time": iso(start_time + timedelta(hours=1)),
        },
        headers=auth_headers(token1),
    )
    assert first.status_code == 201
    first_body = first.json()

    second = client.post(
        "/reservations",
        json={
            "facility_id": facility.id,
            "start_time": iso(start_time + timedelta(hours=2)),
            "end_time": iso(start_time + timedelta(hours=3)),
        },
        headers=auth_headers(token2),
    )
    assert second.status_code == 201
    second_body = second.json()

    list_user1 = client.get("/reservations", headers=auth_headers(token1))
    assert list_user1.status_code == 200
    body_user1 = list_user1.json()
    assert len(body_user1) == 1
    assert body_user1[0]["id"] == first_body["id"]
    assert body_user1[0]["user_id"] == first_body["user_id"]

    list_user2 = client.get("/reservations", headers=auth_headers(token2))
    assert list_user2.status_code == 200
    body_user2 = list_user2.json()
    assert len(body_user2) == 1
    assert body_user2[0]["id"] == second_body["id"]
    assert body_user2[0]["user_id"] == second_body["user_id"]