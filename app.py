import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Restaurant App", layout="wide")

# 🎨 Header
st.title("🍽️ Smart Restaurant Management System")
st.caption("Order multiple items easily + Live sales tracking")

# Fetch menu
menu = requests.get(f"{API_URL}/menu").json()

# 🛒 Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 📋 Menu display (grid style)
st.subheader("📋 Menu")

cols = st.columns(3)

for i, (item, price) in enumerate(menu.items()):
    with cols[i % 3]:
        st.markdown(f"""
        ### 🍴 {item}
        💰 Price: ₹{price}
        """)
        
        qty = st.number_input(f"Qty for {item}", min_value=0, step=1, key=item)
        
        if st.button(f"Add {item}", key=f"btn_{item}"):
            if qty > 0:
                st.session_state.cart[item] = st.session_state.cart.get(item, 0) + qty
                st.success(f"Added {qty} {item}")
            else:
                st.warning("Enter quantity > 0")

# 🛒 Cart Section
st.subheader("🛒 Your Cart")

total = 0

if st.session_state.cart:
    for item, qty in st.session_state.cart.items():
        price = menu[item] * qty
        total += price
        st.write(f"{item} × {qty} = ₹{price}")

    st.markdown(f"### 💵 Total: ₹{total}")

    # 🔥 Place order (multiple items)
    if st.button("✅ Place Full Order"):
        for item, qty in st.session_state.cart.items():
            requests.post(f"{API_URL}/order", json={
                "item": item,
                "quantity": qty
            })
        
        st.success("🎉 Order placed successfully!")
        st.session_state.cart = {}

    # ❌ Clear cart
    if st.button("🗑️ Clear Cart"):
        st.session_state.cart = {}

else:
    st.info("Cart is empty")

# 📊 Sales Report
st.subheader("📊 Sales Report")

if st.button("Show Sales"):
    sales = requests.get(f"{API_URL}/sales").json()
    
    if sales:
        for item, qty in sales.items():
            st.write(f"{item}: {qty} sold")
    else:
        st.warning("No sales yet")