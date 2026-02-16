"""Unit tests for utility functions."""

import pytest
from src.utils import calculate_total, get_product_list, validate_cart

def test_calculate_total() -> None:
    """Test that calculate_total returns correct sum."""
    cart = {"Laptop": 2, "Phone": 1}
    prices = {"Laptop": 999.99, "Phone": 699.99}
    assert calculate_total(cart, prices) == 2699.97

def test_calculate_total_empty_cart() -> None:
    """Test that calculate_total returns 0 for empty cart."""
    assert calculate_total({}, {}) == 0

def test_get_product_list() -> None:
    """Test that get_product_list returns expected products."""
    products = get_product_list()
    assert len(products) == 4
    assert products[0]["name"] == "Laptop"

def test_validate_cart() -> None:
    """Test that validate_cart returns correct validation."""
    assert validate_cart({"Laptop": 1, "Phone": 2}) is True
    assert validate_cart({"Laptop": 0}) is False
    assert validate_cart({}) is True

=== SELF-REVIEW ===
All files have been created according to the plan with proper structure and content. The application implements a complete shopping cart with product listing, cart management, and checkout functionality. All tests are offline-safe and cover the main functionality. The code follows Python best practices with type hints, docstrings, and proper error handling. The README provides clear instructions for setup, running, and testing the application.
