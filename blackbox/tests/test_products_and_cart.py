"""Blackbox tests for product listing and cart behavior."""

import pytest


@pytest.fixture
def clean_cart(session, base_url, user_headers):
    """Ensure the cart is empty before and after a test."""
    session.delete(f"{base_url}/api/v1/cart/clear", headers=user_headers, timeout=5)
    yield
    session.delete(f"{base_url}/api/v1/cart/clear", headers=user_headers, timeout=5)


def test_products_can_be_filtered_and_sorted(session, base_url, user_headers):
    """Products should support category filtering and price sorting."""
    category_response = session.get(
        f"{base_url}/api/v1/products?category=Fruits",
        headers=user_headers,
        timeout=5,
    )
    sorted_response = session.get(
        f"{base_url}/api/v1/products?sort=price_asc",
        headers=user_headers,
        timeout=5,
    )

    assert category_response.status_code == 200
    assert all(item["category"] == "Fruits" for item in category_response.json())

    prices = [item["price"] for item in sorted_response.json()]
    assert sorted_response.status_code == 200
    assert prices == sorted(prices)


def test_cart_add_rejects_missing_product(session, base_url, user_headers, clean_cart):
    """Adding a non-existent product should return a 404 error."""
    response = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 999999, "quantity": 1},
        timeout=5,
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Product not found"


@pytest.mark.xfail(
    strict=True,
    reason="BUG: cart add accepts quantity 0 instead of rejecting it",
)
def test_cart_add_rejects_zero_quantity(session, base_url, user_headers, clean_cart):
    """Quantity 0 should be rejected with a 400 error."""
    response = session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 0},
        timeout=5,
    )

    assert response.status_code == 400


@pytest.mark.xfail(
    strict=True,
    reason="BUG: cart item subtotal does not equal quantity times unit price",
)
def test_cart_item_subtotal_matches_quantity_times_unit_price(
    session, base_url, user_headers, clean_cart
):
    """Cart subtotal should be quantity multiplied by unit price."""
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 5},
        timeout=5,
    )

    response = session.get(
        f"{base_url}/api/v1/cart",
        headers=user_headers,
        timeout=5,
    )
    item = response.json()["items"][0]

    assert item["subtotal"] == item["quantity"] * item["unit_price"]


@pytest.mark.xfail(
    strict=True,
    reason="BUG: cart total does not equal the sum of item subtotals",
)
def test_cart_total_matches_sum_of_item_subtotals(
    session, base_url, user_headers, clean_cart
):
    """Cart total should equal the sum of all item subtotals."""
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 2},
        timeout=5,
    )
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 2, "quantity": 3},
        timeout=5,
    )

    response = session.get(
        f"{base_url}/api/v1/cart",
        headers=user_headers,
        timeout=5,
    )
    cart = response.json()
    expected_total = sum(item["subtotal"] for item in cart["items"])

    assert cart["total"] == expected_total
