import streamlit as st

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="centered")
st.title("💹 Trade Profit Calculator")

# --- Centered inputs with narrower boxes ---
col1, col2 = st.columns(2)

with col1:
    margin = st.number_input("💰 Margin (your money)", min_value=1.0, step=1.0, key="margin", format="%.2f")
    leverage = st.number_input("⚡ Leverage", min_value=1.0, step=1.0, key="leverage", format="%.1f")

with col2:
    profit_target = st.number_input("🎯 Desired profit (€)", min_value=1.0, step=1.0, key="profit", format="%.2f")
    entry_price = st.number_input("📍 Expected entry price", min_value=0.0001, step=0.0001, format="%.4f", key="entry")

# Reduce width of number inputs
st.markdown(
    """
    <style>
    div.row-widget.stNumberInput > div {max-width: 220px;}
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Calculate"):
    if margin <= 0 or leverage <= 0 or profit_target <= 0 or entry_price <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        # Calculate to
