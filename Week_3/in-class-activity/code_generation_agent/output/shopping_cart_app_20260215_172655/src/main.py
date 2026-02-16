"""Main Streamlit application for the shopping cart."""

import streamlit as st
from utils import calculate_total, get_product_list, validate_cart

def main() -> None:
    """Run the shopping cart application."""
    st.title("Shopping Cart App")

    # Initialize session state
    if "cart" not in st.session_state:  
        st.session_state.cart = {}

    # Get product list
    products = get_product_list()

    # Display products
    st.header("Products")
    for product in products:
        with st.expander(f"{product['name']} - ${product['price']}"):
            st.write(product["description"])
            quantity = st.number_input(
                "Quantity",
                min_value=0,
                max_value=10,
                key=f"quantity_{product['name']}",
            )
            if st.button(f"Add to Cart", key=f"add_{product['name']}"):
                if quantity > 0:
                    st.session_state.cart[product["name"]] = quantity
                    st.success(f"Added {quantity} {product['name']}(s) to cart!")
                else:
                    st.warning("Please select a quantity greater than 0")

    # Display cart
    st.header("Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty")
    else:
        for product, quantity in st.session_state.cart.items():
            st.write(f"{product}: {quantity}")
        total = calculate_total(st.session_state.cart, {p["name"]: float(p["price"]) for p in products})
        st.write(f"Total: ${total:.2f}")

        if st.button("Checkout"):
            if validate_cart(st.session_state.cart):
                st.success("Order placed successfully!")
                st.session_state.cart = {}
            else:
                st.error("Invalid cart items")

if __name__ == "__main__":
    main()
