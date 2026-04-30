import streamlit as st

st.set_page_config(page_title="Restaurant App", layout="wide")

# Menu
Menu = {
    'Burger': 50, 'Pizza': 120, 'Cola': 60, 'Pasta': 150, 'Coffee': 70,
    'Sandwich': 90, 'Ice Cream': 90, 'Tea': 50, 'Samosa': 30, 'Chai': 40,
    'Pav Bhaji': 120, 'Chole': 140, 'Vada Pav': 50, 'Dosa': 130, 'Paneer': 180
}

# Session cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "sales" not in st.session_state:
    st.session_state.sales = {}

st.title("🍽️ Smart Restaurant Management System")

# Menu UI
st.subheader("📋 Menu")

cols = st.columns(3)

for i, (item, price) in enumerate(Menu.items()):
    with cols[i % 3]:
        st.markdown(f"### {item}")
        st.write(f"₹{price}")
        
        qty = st.number_input(f"Qty {item}", min_value=0, key=item)
        
        if st.button(f"Add {item}", key=f"btn_{item}"):
            if qty > 0:
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + qty

# Cart
st.subheader("🛒 Cart")

total = 0

if st.session_state.cart:
    for item, qty in st.session_state.cart.items():
        price = Menu[item] * qty
        total += price
        st.write(f"{item} × {qty} = ₹{price}")

    st.markdown(f"### 💵 Total: ₹{total}")

    if st.button("Place Order"):
        for item, qty in st.session_state.cart.items():
            st.session_state.sales[item] = st.session_state.sales.get(item, 0) + qty
        st.session_state.cart = {}
        st.success("Order placed!")

    if st.button("Clear Cart"):
        st.session_state.cart = {}

else:
    st.info("Cart empty")

# Sales
st.subheader("📊 Sales")

if st.button("Show Sales"):
    if st.session_state.sales:
        st.write(st.session_state.sales)
    else:
        st.warning("No sales yet")