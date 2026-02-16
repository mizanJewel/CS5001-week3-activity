"""Unit tests for the main application logic."""

import pytest
from unittest.mock import MagicMock, patch
import streamlit as st
from src.main import main

def test_main_initializes_cart() -> None:
    """Test that main initializes the cart in session state."""
    with patch("streamlit.session_state") as mock_session:
        mock_session.__contains__.return_value = False
        mock_session.__setitem__ = MagicMock()
        main()
        mock_session.__setitem__.assert_called_once_with("cart", {})

def test_main_adds_to_cart() -> None:
    """Test that main adds items to cart when button is clicked."""
    with patch("streamlit.session_state") as mock_session:
        mock_session.__contains__.return_value = True
        mock_session.cart = {}
        mock_session.button = MagicMock(return_value=True)
        mock_session.number_input = MagicMock(return_value=2)
        main()
        assert "Laptop" in mock_session.cart
        assert mock_session.cart["Laptop"] == 2

def test_main_checkout_valid_cart() -> None:
    """Test that main processes checkout for valid cart."""
    with patch("streamlit.session_state") as mock_session:
        mock_session.__contains__.return_value = True
        mock_session.cart = {"Laptop": 1}
        mock_session.button = MagicMock(return_value=True)
        main()
        assert mock_session.cart == {}
