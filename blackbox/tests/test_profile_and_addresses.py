"""Blackbox tests for profile and address endpoints."""

import uuid

import pytest


def _unique_street():
    return f"Street {uuid.uuid4().hex[:12]}"


def test_profile_update_rejects_short_name(session, base_url, user_headers):
    """Profile update should reject names shorter than 2 characters."""
    response = session.put(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
        json={"name": "A", "phone": "1234567890"},
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Name must be between 2 and 50 characters"


def test_profile_update_rejects_invalid_phone(session, base_url, user_headers):
    """Profile update should reject phone numbers that are not 10 digits."""
    response = session.put(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
        json={"name": "Valid Name", "phone": "12345"},
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Phone must be exactly 10 digits"


def test_profile_get_returns_current_user_payload(session, base_url, user_headers):
    """Profile GET should return the current user's profile payload."""
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == 1
    assert "wallet_balance" in response.json()
    assert "loyalty_points" in response.json()


def test_addresses_get_returns_a_list(session, base_url, user_headers):
    """Addresses GET should return the user's address list."""
    response = session.get(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_address_create_and_delete_round_trip(session, base_url, user_headers):
    """A valid address should be created and then deletable."""
    payload = {
        "label": "HOME",
        "street": _unique_street(),
        "city": "Delhi",
        "pincode": "123456",
        "is_default": False,
    }
    create_response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=payload,
        timeout=5,
    )

    assert create_response.status_code == 200
    created = create_response.json()["address"]
    assert created["street"] == payload["street"]
    assert created["city"] == payload["city"]
    assert created["pincode"] == payload["pincode"]

    delete_response = session.delete(
        f"{base_url}/api/v1/addresses/{created['address_id']}",
        headers=user_headers,
        timeout=5,
    )

    assert delete_response.status_code == 200


def test_delete_missing_address_returns_404(session, base_url, user_headers):
    """Deleting an unknown address should return 404."""
    response = session.delete(
        f"{base_url}/api/v1/addresses/999999",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 404


@pytest.mark.xfail(
    strict=True,
    reason="BUG: address update response returns old data instead of updated data",
)
def test_address_update_response_should_show_new_data(session, base_url, user_headers):
    """The update endpoint should return the updated address payload."""
    payload = {
        "label": "HOME",
        "street": _unique_street(),
        "city": "Mumbai",
        "pincode": "654321",
        "is_default": False,
    }
    create_response = session.post(
        f"{base_url}/api/v1/addresses",
        headers=user_headers,
        json=payload,
        timeout=5,
    )
    created = create_response.json()["address"]
    updated_street = _unique_street()

    try:
        update_response = session.put(
            f"{base_url}/api/v1/addresses/{created['address_id']}",
            headers=user_headers,
            json={"street": updated_street, "is_default": True},
            timeout=5,
        )

        assert update_response.status_code == 200
        assert update_response.json()["address"]["street"] == updated_street
        assert update_response.json()["address"]["is_default"] is True
    finally:
        session.delete(
            f"{base_url}/api/v1/addresses/{created['address_id']}",
            headers=user_headers,
            timeout=5,
        )
