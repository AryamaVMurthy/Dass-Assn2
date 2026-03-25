# Black Box API Testing Report

## 3. System Under Test

For Part 3, black-box testing was performed on the QuickCart REST API using only the provided documentation and the running server. No internal implementation details were used. All tests were written with `pytest` and `requests` under `blackbox/tests/`.

The API was run locally on `http://127.0.0.1:8080` from the provided Docker image. The tests were designed directly from the API documentation, especially the documented validation rules, status codes, and expected response structures. For data-dependent checks such as product prices and stock restoration, the admin inspection endpoints were used as the live database oracle instead of hardcoded assumptions.

## 3.1 Test Design Approach

The test suite covered:
- required request headers
- admin data-inspection endpoints
- profile and address retrieval and validation
- product listing, product detail, and search behavior
- valid requests
- invalid inputs
- missing fields or headers
- wrong values and boundary cases
- user-scoped stateful flows such as cart, checkout, wallet, orders, loyalty, reviews, and support tickets

A mix of passing tests and strict `xfail` tests was used:
- passing tests verified documented behavior that the server implemented correctly
- strict `xfail` tests captured real API defects where the live behavior did not match the documentation

Using strict `xfail` kept the suite executable while still making the bugs visible and reproducible. If any recorded defect was fixed later, the test would become an `XPASS` and signal that the documented bug no longer existed.

## 3.2 Automated Test Files

The final automated test suite included:
- `blackbox/tests/conftest.py`
- `blackbox/tests/test_admin_and_product_details.py`
- `blackbox/tests/test_headers.py`
- `blackbox/tests/test_loyalty_and_reviews.py`
- `blackbox/tests/test_products_and_cart.py`
- `blackbox/tests/test_profile_and_addresses.py`
- `blackbox/tests/test_wallet_checkout_orders_support.py`

## 3.3 Test Cases Covered

### Header Validation
- missing `X-Roll-Number` on admin endpoints returned `401`
- non-integer `X-Roll-Number` returned `400`
- missing `X-User-ID` on user-scoped endpoints returned `400`
- non-existent `X-User-ID` was checked against the documented invalid-header behavior

### Admin / Inspection
- admin users, carts, orders, products, coupons, tickets, and addresses endpoints returned `200`
- admin user detail returned a single object payload

### Profile and Addresses
- profile GET returned the current user payload
- profile update rejected a name shorter than 2 characters
- profile update rejected a phone number that was not exactly 10 digits
- addresses GET returned a list
- valid address creation returned the created address object
- created address could be deleted successfully
- deleting a missing address returned `404`
- adding a new default address cleared the previous default
- address update responses were checked against the documented “return new data” rule
- address creation validation was checked for label, street, city, and pincode constraints

### Products and Cart
- product list supported category filtering
- product list supported price sorting
- product list prices were compared against the admin DB snapshot
- product search filtered by name fragment
- unknown product detail returned `404`
- adding a non-existent product returned `404`
- adding quantity `0` should have returned `400`
- adding a negative quantity should have returned `400`
- cart update rejected quantity `0`
- cart remove returned `404` when the product was not in the cart
- cart clear emptied the cart
- cart item subtotal should have equaled `quantity * unit_price`
- cart total should have equaled the sum of all item subtotals

### Wallet, Checkout, Orders, Coupons, Support
- wallet GET returned the current balance field
- wallet top-up rejected zero and above-limit amounts
- wallet pay rejected insufficient balance
- wallet top-up and direct wallet payment were checked for exact balance changes
- checkout should have rejected an empty cart
- invalid payment methods were rejected
- COD and WALLET checkout started with `PENDING` payment status
- CARD checkout created a `PAID` order
- checkout invoices were checked for `subtotal + GST = total`
- COD above `5000` was rejected
- orders list and detail included a newly created order
- cancelling a missing order returned `404`
- cancelling an order was checked for product-stock restoration
- expired coupons were rejected
- coupon minimum cart value was enforced
- coupon remove returned a success message
- support tickets started as `OPEN`
- support ticket list included newly created tickets
- support ticket subject and message length limits were enforced
- support ticket status moved forward only

### Loyalty and Reviews
- loyalty GET returned the current points balance
- loyalty redeem rejected `0` points
- loyalty redeem rejected redemptions above available points
- review average matched the arithmetic mean of returned ratings
- review rating below `1` should have been rejected
- review rating above `5` should have been rejected
- empty review comments were rejected

## 3.4 Verification

The complete suite was run with:

```bash
.venv/bin/pytest blackbox/tests -q
```

Final result:

```text
40 passed, 15 xfailed in 1.05s
```

The expected failures corresponded to real API defects confirmed against the documentation.

## 3.5 Bugs Found

### Bug 1: Non-existent `X-User-ID` returned `404` instead of the documented `400`
- Endpoint: `GET /api/v1/profile`
- Request:
  - Method: `GET`
  - URL: `/api/v1/profile`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 999999`
- Expected result:
  - status `400`
  - the user header should have been treated as invalid
- Actual result:
  - status `404`
  - response body said `User not found`
- Why it was a bug:
  - the documentation stated that missing or invalid `X-User-ID` values returned `400`

### Bug 2: Address update returned old data instead of updated data
- Endpoint: `PUT /api/v1/addresses/{address_id}`
- Request:
  - Method: `PUT`
  - URL: `/api/v1/addresses/{address_id}`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"street": "<new street>", "is_default": true}`
- Expected result:
  - status `200`
  - response should have shown the updated address data
- Actual result:
  - status `200`
  - response still showed the old street and old `is_default` value
- Why it was a bug:
  - the documentation explicitly said that the response had to show the new updated data

### Bug 3: Address creation accepted a non-digit pincode
- Endpoint: `POST /api/v1/addresses`
- Request:
  - Method: `POST`
  - URL: `/api/v1/addresses`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"label":"HOME","street":"12345 Main St","city":"Delhi","pincode":"12AB56","is_default":false}`
- Expected result:
  - status `400`
  - pincode should have been rejected because it was not exactly six digits
- Actual result:
  - status `200`
  - the address was created successfully
- Why it was a bug:
  - the documentation required the pincode to be exactly six digits

### Bug 4: Cart accepted quantity `0`
- Endpoint: `POST /api/v1/cart/add`
- Request:
  - Method: `POST`
  - URL: `/api/v1/cart/add`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"product_id": 1, "quantity": 0}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - the item was added to the cart
- Why it was a bug:
  - the documentation said quantity had to be at least `1`

### Bug 5: Cart accepted negative quantity
- Endpoint: `POST /api/v1/cart/add`
- Request:
  - Method: `POST`
  - URL: `/api/v1/cart/add`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"product_id": 1, "quantity": -1}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - the item was added to the cart
- Why it was a bug:
  - the documentation said zero or negative quantities had to be rejected

### Bug 6: Cart item subtotal was incorrect
- Endpoint: `GET /api/v1/cart`
- Request:
  - after adding product `1` with quantity `5`
- Expected result:
  - subtotal should have equaled `5 * 120 = 600`
- Actual result:
  - subtotal was returned as `88`
- Why it was a bug:
  - the documentation said each item subtotal had to be `quantity * unit_price`

### Bug 7: Cart total was incorrect
- Endpoint: `GET /api/v1/cart`
- Request:
  - after adding multiple cart items
- Expected result:
  - total should have equaled the sum of all item subtotals
- Actual result:
  - total did not match the subtotal sum
- Why it was a bug:
  - the documentation said the cart total had to include every item and equal the subtotal sum

### Bug 8: Wallet pay deducted more than the requested amount
- Endpoint: `POST /api/v1/wallet/pay`
- Request:
  - Method: `POST`
  - URL: `/api/v1/wallet/pay`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"amount": 1}`
- Expected result:
  - wallet balance should have decreased by exactly `1`
- Actual result:
  - the API returned success but reduced the balance by `1.6`
- Why it was a bug:
  - the documentation said the exact amount requested had to be deducted and no extra amount should have been taken

### Bug 9: Expired coupons were accepted
- Endpoint: `POST /api/v1/coupon/apply`
- Request:
  - Method: `POST`
  - URL: `/api/v1/coupon/apply`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"coupon_code": "EXPIRED100"}`
- Expected result:
  - status `400`
  - the coupon should have been rejected because it was expired
- Actual result:
  - status `200`
  - the coupon was applied and the discount was granted
- Why it was a bug:
  - the documentation said expired coupons had to be rejected

### Bug 10: Checkout accepted an empty cart
- Endpoint: `POST /api/v1/checkout`
- Request:
  - Method: `POST`
  - URL: `/api/v1/checkout`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"payment_method": "CARD"}`
- Expected result:
  - status `400`
  - checkout should have failed because the cart was empty
- Actual result:
  - status `200`
  - an order was created with zero totals
- Why it was a bug:
  - the documentation explicitly said the cart must not be empty during checkout

### Bug 11: Cancelled orders did not restore stock
- Endpoint: `POST /api/v1/orders/{order_id}/cancel`
- Request:
  - Method: `POST`
  - URL: `/api/v1/orders/{order_id}/cancel`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: none
- Expected result:
  - status `200`
  - product stock should have been restored to the pre-checkout quantity
- Actual result:
  - status `200`
  - product stock remained reduced after cancellation
- Why it was a bug:
  - the documentation said that cancelled orders had to add all items back to stock

### Bug 12: Product list price did not match the admin DB snapshot
- Endpoint: `GET /api/v1/products`
- Request:
  - Method: `GET`
  - URL: `/api/v1/products?sort=price_asc`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
- Expected result:
  - every user-facing product price should have matched the latest price returned by `GET /api/v1/admin/products`
- Actual result:
  - at least one product differed; for example product `27` (`Coriander - 100g`) returned price `20` in the user list while the admin DB snapshot returned `15`
- Why it was a bug:
  - the documentation said the product price shown to users had to be the exact real price stored in the database

### Bug 13: Reviews endpoint accepted rating `0`
- Endpoint: `POST /api/v1/products/{product_id}/reviews`
- Request:
  - Method: `POST`
  - URL: `/api/v1/products/1/reviews`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"rating": 0, "comment": "bad"}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - the review was created successfully
- Why it was a bug:
  - the documentation said rating had to be between `1` and `5`

### Bug 14: Reviews endpoint accepted rating above `5`
- Endpoint: `POST /api/v1/products/{product_id}/reviews`
- Request:
  - Method: `POST`
  - URL: `/api/v1/products/1/reviews`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"rating": 6, "comment": "too high"}`
- Expected result:
  - status `400`
- Actual result:
  - status `200`
  - the review was created successfully
- Why it was a bug:
  - the documentation said rating had to stay within the closed interval `1..5`

### Bug 15: Profile update accepted phone values containing letters
- Endpoint: `PUT /api/v1/profile`
- Request:
  - Method: `PUT`
  - URL: `/api/v1/profile`
  - Headers: `X-Roll-Number: 2024101043`, `X-User-ID: 1`
  - Body: `{"name":"Valid Name","phone":"12345abcde"}`
- Expected result:
  - status `400`
  - the phone number should have been rejected because it was not exactly ten digits
- Actual result:
  - status `200`
  - the profile update succeeded
- Why it was a bug:
  - the documentation required the phone number to contain exactly ten digits, not merely ten characters

## 3.6 Summary

The black-box suite covered the major documented endpoint groups of the QuickCart API and identified fifteen reproducible contract violations. The tests remained executable, isolated enough for repeated runs, and useful for ongoing verification because strict expected-failure markers were used for every confirmed defect.
