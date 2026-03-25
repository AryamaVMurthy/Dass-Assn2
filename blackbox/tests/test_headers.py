"""Smoke tests for required QuickCart headers."""

import pytest


def test_admin_endpoint_requires_roll_number_header(session, base_url):
    """Admin endpoints should reject requests without X-Roll-Number."""
    response = session.get(f"{base_url}/api/v1/admin/users", timeout=5)

    assert response.status_code == 401
    assert response.json()["error"] == "Missing X-Roll-Number header"


def test_admin_endpoint_rejects_non_integer_roll_number(session, base_url):
    """Admin endpoints should reject non-integer roll numbers."""
    response = session.get(
        f"{base_url}/api/v1/admin/users",
        headers={"X-Roll-Number": "abc"},
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "X-Roll-Number must be a valid integer"


def test_user_endpoint_requires_user_id_header(session, base_url, roll_headers):
    """User-scoped endpoints should reject requests without X-User-ID."""
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers=roll_headers,
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Missing X-User-ID header"


@pytest.mark.parametrize("user_id", ["0", "-1", "abc"])
def test_user_endpoint_rejects_invalid_user_id_formats(
    session, base_url, roll_headers, user_id
):
    """User-scoped endpoints should reject malformed or non-positive user IDs."""
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers={**roll_headers, "X-User-ID": user_id},
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "X-User-ID must be a valid positive integer"


@pytest.mark.xfail(
    strict=True,
    reason="BUG: non-existent X-User-ID returns 404 instead of the documented 400",
)
def test_user_endpoint_rejects_non_existent_user_id_with_400(session, base_url):
    """User-scoped endpoints should treat unknown user IDs as invalid headers."""
    response = session.get(
        f"{base_url}/api/v1/profile",
        headers={"X-Roll-Number": "2024101043", "X-User-ID": "999999"},
        timeout=5,
    )

    assert response.status_code == 400
