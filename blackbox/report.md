# Black Box API Testing Report

## 3. System Under Test

For Part 3, I performed black-box testing on the QuickCart REST API using only the provided documentation and the running server. I did not rely on internal implementation details. All tests were written with `pytest` and `requests` under `blackbox/tests/`.

The API was run locally on `http://127.0.0.1:8080` from the provided Docker image. The tests were designed directly from the API documentation, especially the documented validation rules, status codes, and expected response structures. For data-dependent checks such as product prices, I used the admin inspection endpoints as the live database oracle instead of hardcoded assumptions.

## 3.1 Test Design Approach

The test suite covers:
- required request headers
- admin data-inspection endpoints
- profile and address retrieval and validation
- product listing, product detail, and search behavior
- valid requests
- invalid inputs
- missing fields or headers
- wrong values and boundary cases
- user-scoped stateful flows such as cart, checkout, wallet, orders, and tickets

I used a mix of:
- passing tests for documented behavior that the server implements correctly
- strict `xfail` tests for real bugs where the live server behavior does not match the documentation

Using strict `xfail` keeps the suite executable while still making the bugs visible and reproducible. If a bug is unexpectedly fixed later, the test will become an `XPASS` and signal that the recorded defect is no longer present.

## 3.2 Automated Test Files

The final automated test suite includes:
- `blackbox/tests/conftest.py`
- `blackbox/tests/test_admin_and_product_details.py`
- `blackbox/tests/test_headers.py`
- `blackbox/tests/test_profile_and_addresses.py`
- `blackbox/tests/test_products_and_cart.py`
- `blackbox/tests/test_wallet_checkout_orders_support.py`
- `blackbox/tests/test_loyalty_and_reviews.py`

## 3.3 Test Cases Covered

### Header Validation
- Missing `X-Roll-Number` on admin endpoints returns `401`
- Non-integer `X-Roll-Number` returns `400`
- Missing `X-User-ID` on user-scoped endpoints returns `400`

### Admin / Inspection
- admin users, carts, orders, products, coupons, tickets, and addresses endpoints return `200`
- admin user detail endpoint returns a single object payload

### Profile and Addresses
- profile GET returns the current user payload
- profile update rejects a name shorter than 2 characters
- profile update rejects a phone number that is not exactly 10 digits
- addresses GET returns a list
- valid address creation returns the created address object
- created address can be deleted successfully
- deleting a missing address returns `404`
- adding a new default address clears the previous default
- address update response should return new data

### Products and Cart
- product list supports category filtering
- product list supports price sorting
- product list prices should match the admin DB snapshot
- product search filters by name fragment
- unknown product detail returns `404`
- adding a non-existent product returns `404`
- adding quantity `0` should return `400`
- cart update rejects quantity `0`
- cart remove returns `404` when the product is not in the cart
- cart clear empties the cart
- cart item subtotal should equal `quantity * unit_price`
- cart total should equal the sum of all item subtotals

### Wallet, Checkout, Orders, Coupons, Support
- wallet GET returns the current balance field
- wallet top-up rejects zero and above-limit amounts
- wallet pay rejects insufficient balance
- wallet top-up and payment should change balance by the exact requested amount
- checkout should reject an empty cart
- invalid payment methods should be rejected
- COD and WALLET checkout start with `PENDING` payment status
- CARD checkout should create a `PAID` order
- checkout invoice should satisfy `subtotal + GST = total`
- COD above `5000` should be rejected
- orders list and detail should include a newly created order
- cancelling a missing order should return `404`
- expired coupons should be rejected
- coupon minimum cart value is enforced
- coupon remove endpoint should return success
- support tickets should start as `OPEN`
- support ticket list should include newly created tickets
- support ticket subject and message length limits are enforced
- support ticket status should only move forward

### Loyalty and Reviews
- loyalty GET returns the current points balance
- loyalty redeem rejects `0` points
- loyalty redeem rejects redemptions above available points
- review average matches the arithmetic mean of returned ratings
- review rating below `1` should be rejected
- empty review comments are rejected

## 3.4 Verification

The complete suite was run with:

```bash
.venv/bin/pytest blackbox/tests -q
```

Final result:

```text
40 passed, 9 xfailed in 0.94s
```

The expected failures correspond to actual API defects confirmed against the documentation.

## 3.5 Bugs Found

### Bug 1: Address update returns old data instead of updated data
- Endpoint: `PUT /api/v1/addresses/{address_id}`
- Request:
  - Method: `PUT`
  - URL: `/api/v1/addresses/{address_id}`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"street": "<new street>", "is_default": true}`
- Expected result:
  - status `200`
  - response should show the updated address data
- Actual result:
  - status `200`
  - response still shows the old street and old `is_default` value
- Why it is a bug:
  - the documentation explicitly says the response must show the new updated data

### Bug 2: Cart accepts quantity `0`
- Endpoint: `POST /api/v1/cart/add`
- Request:
  - Method: `POST`
  - URL: `/api/v1/cart/add`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"product_id": 1, "quantity": 0}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - item is added to cart
- Why it is a bug:
  - the documentation says quantity must be at least `1`

### Bug 3: Cart item subtotal is incorrect
- Endpoint: `GET /api/v1/cart`
- Request:
  - after adding product `1` with quantity `5`
- Expected result:
  - subtotal should equal `5 * 120 = 600`
- Actual result:
  - subtotal returned as `88`
- Why it is a bug:
  - the documentation says each item subtotal must be `quantity * unit_price`

### Bug 4: Cart total is incorrect
- Endpoint: `GET /api/v1/cart`
- Request:
  - after adding multiple cart items
- Expected result:
  - total should equal the sum of all item subtotals
- Actual result:
  - total returned does not match the subtotal sum
- Why it is a bug:
  - the documentation says the cart total must include every item and equal the subtotal sum

### Bug 5: Wallet pay deducts more than the requested amount
- Endpoint: `POST /api/v1/wallet/pay`
- Request:
  - Method: `POST`
  - URL: `/api/v1/wallet/pay`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"amount": 1}`
- Expected result:
  - wallet balance should decrease by exactly `1`
- Actual result:
  - the API returns success but reduces the balance by `1.6`
- Why it is a bug:
  - the documentation says the exact amount requested must be deducted and no extra amount should be taken

### Bug 6: Expired coupons are accepted
- Endpoint: `POST /api/v1/coupon/apply`
- Request:
  - Method: `POST`
  - URL: `/api/v1/coupon/apply`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"coupon_code": "EXPIRED100"}`
- Expected result:
  - status `400`
  - coupon should be rejected because it is expired
- Actual result:
  - status `200`
  - coupon is applied and discount is granted
- Why it is a bug:
  - the documentation says expired coupons must not be accepted

### Bug 7: Reviews endpoint accepts rating `0`
- Endpoint: `POST /api/v1/products/{product_id}/reviews`
- Request:
  - Method: `POST`
  - URL: `/api/v1/products/1/reviews`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"rating": 0, "comment": "bad"}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - review is created successfully
- Why it is a bug:
  - the documentation says rating must be between `1` and `5`

### Bug 8: Checkout accepts an empty cart
- Endpoint: `POST /api/v1/checkout`
- Request:
  - Method: `POST`
  - URL: `/api/v1/checkout`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
  - Body: `{"payment_method": "CARD"}`
- Expected result:
  - status `400`
  - checkout should fail because the cart is empty
- Actual result:
  - status `200`
  - an order is created with zero totals
- Why it is a bug:
  - the documentation explicitly says the cart must not be empty during checkout

### Bug 9: Product list price does not match the admin DB snapshot
- Endpoint: `GET /api/v1/products`
- Request:
  - Method: `GET`
  - URL: `/api/v1/products?sort=price_asc`
  - Headers: `X-Roll-Number: 1`, `X-User-ID: 1`
- Expected result:
  - every user-facing product price should match the latest price returned by `GET /api/v1/admin/products`
- Actual result:
  - at least one product differs; for example product `27` (`Coriander - 100g`) returned price `20` in the user list while the admin DB snapshot returned `15`
- Why it is a bug:
  - the documentation says the product price shown to users must be the exact real price stored in the database

## 3.6 Summary

The black-box suite now covers the major documented endpoint groups of the QuickCart API and identifies nine reproducible API defects. The tests are executable, isolated enough for repeated runs, and use strict expected-failure markers for the documented bugs so the suite remains useful while still exposing contract violations.
