"""Utility functions for product management and cart operations."""

from typing import Dict, List, Optional

def calculate_total(cart: Dict[str, int], prices: Dict[str, float]) -> float:
    """Calculate the total price of items in the cart.

    Args:
        cart: Dictionary of product names and quantities
        prices: Dictionary of product names and their prices

    Returns:
        Total price as float
    """
    return sum(prices.get(product, 0) * quantity for product, quantity in cart.items())

def get_product_list() -> List[Dict[str, str]]:
    """Return a list of available products with their details.

    Returns:
        List of dictionaries containing product information
    """
    return [
        {"name": "Laptop", "price": "999.99", "description": "High-performance laptop"},
        {"name": "Phone", "price": "699.99", "description": "Latest smartphone"},
        {"name": "Headphones", "price": "149.99", "description": "Noise-cancelling headphones"},
        {"name": "Keyboard", "price": "89.99", "description": "Mechanical gaming keyboard"},
    ]

def validate_cart(cart: Dict[str, int]) -> bool:
    """Validate that all items in cart have positive quantities.

    Args:
        cart: Dictionary of product names and quantities

    Returns:
        True if cart is valid, False otherwise
    """
    return all(quantity > 0 for quantity in cart.values())
