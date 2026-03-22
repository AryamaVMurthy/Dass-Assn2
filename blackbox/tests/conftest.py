"""Shared fixtures and helpers for QuickCart blackbox tests."""

import os

import pytest
import requests


BASE_URL = os.environ.get("QUICKCART_BASE_URL", "http://127.0.0.1:8080")
ROLL_NUMBER = os.environ.get("QUICKCART_ROLL_NUMBER", "1")


@pytest.fixture
def base_url():
    """Return the configured QuickCart base URL."""
    return BASE_URL


@pytest.fixture
def session():
    """Return a requests session for API calls."""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture
def roll_headers():
    """Return headers with only the roll number."""
    return {"X-Roll-Number": ROLL_NUMBER}


@pytest.fixture
def user_headers(roll_headers):
    """Return headers scoped to a known valid user."""
    headers = dict(roll_headers)
    headers["X-User-ID"] = "1"
    return headers
