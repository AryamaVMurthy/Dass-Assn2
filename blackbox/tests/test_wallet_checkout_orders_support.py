"""Blackbox tests for wallet, checkout, orders, coupons, and support tickets."""

import uuid

import pytest


@pytest.fixture
def clean_cart(session, base_url, user_headers):
    """Ensure the cart is empty before and after a test."""
    session.delete(f"{base_url}/api/v1/cart/clear", headers=user_headers, timeout=5)
    yield
    session.delete(f"{base_url}/api/v1/cart/clear", headers=user_headers, timeout=5)


@pytest.mark.xfail(
    strict=True,
    reason="BUG: wallet pay deducts more than the requested amount",
)
def test_wallet_add_and_pay_change_balance_by_exact_amount(
    session, base_url, user_headers
):
    """Wallet operations should change balance by the requested amount only."""
    before = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
        timeout=5,
    ).json()["wallet_balance"]

    top_up = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 100},
        timeout=5,
    )
    after_top_up = top_up.json()["wallet_balance"]

    payment = session.post(
        f"{base_url}/api/v1/wallet/pay",
        headers=user_headers,
        json={"amount": 1},
        timeout=5,
    )
    after_payment = payment.json()["wallet_balance"]

    assert top_up.status_code == 200
    assert payment.status_code == 200
    assert after_top_up == round(before + 100, 2)
    assert after_payment == round(after_top_up - 1, 2)


def test_checkout_card_creates_paid_order_with_expected_invoice_values(
    session, base_url, user_headers, clean_cart
):
    """CARD checkout should create a PAID order and consistent invoice amounts."""
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 1, "quantity": 1},
        timeout=5,
    )
    checkout = session.post(
        f"{base_url}/api/v1/checkout",
        headers=user_headers,
        json={"payment_method": "CARD"},
        timeout=5,
    )

    order_id = checkout.json()["order_id"]
    invoice = session.get(
        f"{base_url}/api/v1/orders/{order_id}/invoice",
        headers=user_headers,
        timeout=5,
    )

    assert checkout.status_code == 200
    assert checkout.json()["payment_status"] == "PAID"
    assert invoice.status_code == 200
    assert invoice.json()["subtotal"] + invoice.json()["gst_amount"] == invoice.json()[
        "total_amount"
    ]


def test_checkout_rejects_cod_above_5000(session, base_url, user_headers, clean_cart):
    """COD should be rejected for totals above 5000."""
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 42, "quantity": 20},
        timeout=5,
    )
    response = session.post(
        f"{base_url}/api/v1/checkout",
        headers=user_headers,
        json={"payment_method": "COD"},
        timeout=5,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "COD not allowed for amount > 5000"


@pytest.mark.xfail(
    strict=True,
    reason="BUG: expired coupons are accepted instead of being rejected",
)
def test_expired_coupon_should_be_rejected(session, base_url, user_headers, clean_cart):
    """Expired coupons should not be applied to the cart."""
    session.post(
        f"{base_url}/api/v1/cart/add",
        headers=user_headers,
        json={"product_id": 42, "quantity": 20},
        timeout=5,
    )
    response = session.post(
        f"{base_url}/api/v1/coupon/apply",
        headers=user_headers,
        json={"coupon_code": "EXPIRED100"},
        timeout=5,
    )

    assert response.status_code == 400


def test_support_ticket_status_only_moves_forward(session, base_url, user_headers):
    """Support tickets should allow only forward status transitions."""
    create = session.post(
        f"{base_url}/api/v1/support/ticket",
        headers=user_headers,
        json={
            "subject": f"Issue {uuid.uuid4().hex[:8]}",
            "message": "hello world",
        },
        timeout=5,
    )

    assert create.status_code == 200
    assert create.json()["status"] == "OPEN"
    assert create.json()["message"] == "hello world"

    ticket_id = create.json()["ticket_id"]
    invalid = session.put(
        f"{base_url}/api/v1/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=5,
    )
    first_valid = session.put(
        f"{base_url}/api/v1/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "IN_PROGRESS"},
        timeout=5,
    )
    second_valid = session.put(
        f"{base_url}/api/v1/support/tickets/{ticket_id}",
        headers=user_headers,
        json={"status": "CLOSED"},
        timeout=5,
    )

    assert invalid.status_code == 400
    assert first_valid.status_code == 200
    assert first_valid.json()["status"] == "IN_PROGRESS"
    assert second_valid.status_code == 200
    assert second_valid.json()["status"] == "CLOSED"
