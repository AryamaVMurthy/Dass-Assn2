"""Blackbox coverage for admin inspection and product detail endpoints."""

import pytest


@pytest.mark.parametrize(
    ("path", "expected_type"),
    [
        ("/api/v1/admin/users", list),
        ("/api/v1/admin/users/1", dict),
        ("/api/v1/admin/carts", list),
        ("/api/v1/admin/orders", list),
        ("/api/v1/admin/products", list),
        ("/api/v1/admin/coupons", list),
        ("/api/v1/admin/tickets", list),
        ("/api/v1/admin/addresses", list),
    ],
)
def test_admin_inspection_endpoints_return_documented_payload_shapes(
    session, base_url, roll_headers, path, expected_type
):
    """Admin inspection endpoints should respond with JSON collections or objects."""
    response = session.get(f"{base_url}{path}", headers=roll_headers, timeout=10)

    assert response.status_code == 200
    assert isinstance(response.json(), expected_type)


def test_product_detail_returns_404_for_unknown_product(session, base_url, user_headers):
    """Unknown product IDs should return a 404 error."""
    response = session.get(
        f"{base_url}/api/v1/products/999999",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Product not found"


def test_product_search_filters_by_name_fragment(session, base_url, user_headers):
    """Product search should narrow results by product name fragments."""
    response = session.get(
        f"{base_url}/api/v1/products?search=app",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 200
    assert response.json()
    assert all("app" in item["name"].lower() for item in response.json())
