"""Smoke tests for required QuickCart headers."""


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
