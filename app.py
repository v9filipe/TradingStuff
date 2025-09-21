import streamlit as st
import time

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="wide")

# CSS for glassmorphism and centered content
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e1e2f, #2c3e50);
    font-family: 'Arial', sans-serif;
}
.glass-box {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    text-align: center;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border-radius: 12px;
    transition: all 0.3s;
}
.stButton>button:hover {
    background-color: #45a049;
    transform: scale(1.05);
}
.tp-text {
    color: #2ecc71;
    font-size: 1.8em;
    font-weight: bold;
    margin: 20px 0;
}
.sl-text {
    color: #e74c3c;
    font-size: 1.8em;
    font-weight: bold;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; color:white;'>💹 Trade Profit Calculator</h1>", unsafe_allow_html=True)

# Two columns: Inputs | Trade Info
col_input, col_output = st.columns([1,1])

with col_input:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h3>⚡ Inputs</h3>", unsafe_allow_html=True)
    margin = st.number_input("💰 Margin (€)", min_value=1.0, step=1.0)
    profit_target = st.number_input("🎯 Desired profit (€)", min_value=1.0, step=1.0)
    entry_price = st.number_input("📍 Entry price", min_value=0.0001, step=0.0001, format="%.4f")
    leverage_input = st.number_input(
        "⚡ Leverage (1× - 500×)",
        min_value=1.0,
        max_value=500.0,
        value=1.0,
        step=0.1
    )
    calculate = st.button("Calculate")
    st.markdown("</div>", unsafe_allow_html=True)

with col_output:
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 Trade Info</h3>", unsafe_allow_html=True)
    tp_placeholder = st.empty()
    sl_placeholder = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)

# Calculation and animation
if calculate:
    if margin <= 0 or profit_target <= 0 or entry_price <= 0 or leverage_input <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        price_change_pct = profit_target / (margin * leverage_input)
        tp_price = entry_price * (1 + price_change_pct)
        sl_price = entry_price * (1 - price_change_pct)

        # Animate TP/SL with nicer style
        steps = 20
        for i in range(1, steps+1):
            factor = i / steps
            tp_placeholder.markdown(f"<div class='tp-text'>🎯 TP: {entry_price*(1 + price_change_pct*factor):.4f}</div>", unsafe_allow_html=True)
            sl_placeholder.markdown(f"<div class='sl-text'>🛑 SL: {entry_price*(1 - price_change_pct*factor):.4f}</div>", unsafe_allow_html=True)
            time.sleep(0.03)
