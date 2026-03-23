"""Blackbox tests for loyalty points and product reviews."""

import uuid

import pytest


def test_loyalty_redeem_rejects_zero_and_insufficient_points(
    session, base_url, user_headers
):
    """Loyalty redemption should reject zero and overly large redemptions."""
    zero_response = session.post(
        f"{base_url}/api/v1/loyalty/redeem",
        headers=user_headers,
        json={"points": 0},
        timeout=5,
    )
    too_many_response = session.post(
        f"{base_url}/api/v1/loyalty/redeem",
        headers=user_headers,
        json={"points": 999999},
        timeout=5,
    )

    assert zero_response.status_code == 400
    assert zero_response.json()["error"] == "Points must be >= 1"
    assert too_many_response.status_code == 400
    assert too_many_response.json()["error"] == "Insufficient points"


def test_loyalty_get_returns_points_balance(session, base_url, user_headers):
    """The loyalty endpoint should expose the user's current points balance."""
    response = session.get(
        f"{base_url}/api/v1/loyalty",
        headers=user_headers,
        timeout=10,
    )

    assert response.status_code == 200
    assert "loyalty_points" in response.json()


def test_wallet_rejects_invalid_top_up_amounts(session, base_url, user_headers):
    """Wallet top-up should reject zero and above-limit amounts."""
    zero_response = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 0},
        timeout=10,
    )
    too_large_response = session.post(
        f"{base_url}/api/v1/wallet/add",
        headers=user_headers,
        json={"amount": 100001},
        timeout=10,
    )

    assert zero_response.status_code == 400
    assert too_large_response.status_code == 400


def test_wallet_pay_rejects_insufficient_balance(session, base_url, user_headers):
    """Wallet payments above the available balance should fail."""
    balance = session.get(
        f"{base_url}/api/v1/wallet",
        headers=user_headers,
        timeout=10,
    ).json()["wallet_balance"]
    response = session.post(
        f"{base_url}/api/v1/wallet/pay",
        headers=user_headers,
        json={"amount": balance + 100000},
        timeout=10,
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Insufficient balance"


def test_review_average_is_decimal_after_adding_new_review(
    session, base_url, user_headers
):
    """Average rating should remain a decimal calculation after new reviews."""
    add_response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json={"rating": 5, "comment": f"avg-{uuid.uuid4().hex[:8]}"},
        timeout=10,
    )
    after_response = session.get(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        timeout=10,
    )
    after_payload = after_response.json()
    ratings = [review["rating"] for review in after_payload["reviews"]]
    expected_average = sum(ratings) / len(ratings)

    assert add_response.status_code == 200
    assert after_response.status_code == 200
    assert after_payload["average_rating"] == pytest.approx(expected_average)


@pytest.mark.xfail(
    strict=True,
    reason="BUG: reviews endpoint accepts rating 0 instead of rejecting it",
)
def test_review_rejects_rating_below_one(session, base_url, user_headers):
    """Ratings below 1 should be rejected with a 400 error."""
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json={"rating": 0, "comment": "bad"},
        timeout=5,
    )

    assert response.status_code == 400


@pytest.mark.xfail(
    strict=True,
    reason="BUG: reviews endpoint accepts ratings above 5 instead of rejecting them",
)
def test_review_rejects_rating_above_five(session, base_url, user_headers):
    """Ratings above 5 should be rejected with a 400 error."""
    response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json={"rating": 6, "comment": "too high"},
        timeout=5,
    )

    assert response.status_code == 400
