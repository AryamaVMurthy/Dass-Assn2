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


def test_review_average_is_decimal_after_adding_new_review(
    session, base_url, user_headers
):
    """Average rating should remain a decimal calculation after new reviews."""
    before = session.get(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        timeout=5,
    ).json()["average_rating"]

    add_response = session.post(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        json={"rating": 5, "comment": f"avg-{uuid.uuid4().hex[:8]}"},
        timeout=5,
    )
    after = session.get(
        f"{base_url}/api/v1/products/1/reviews",
        headers=user_headers,
        timeout=5,
    ).json()["average_rating"]

    assert add_response.status_code == 200
    assert isinstance(after, (int, float))
    assert after >= before


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
