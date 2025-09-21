import streamlit as st
import time

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="wide")

# CSS for clean dark dashboard look
st.markdown("""
<style>
body {
    background-color: #121212;
    color: #ffffff;
    font-family: 'Arial', sans-serif;
}
.panel {
    background-color: #1e1e1e;
    border-radius: 15px;
    padding: 40px;
    margin: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    color: white;
    text-align: center;
    min-height: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    height: 55px;
    width: 100%;
    font-size: 18px;
    border-radius: 12px;
    transition: all 0.2s;
}
.stButton>button:hover {
    background-color: #45a049;
    transform: scale(1.02);
}
.stNumberInput>div>div>input {
    font-size: 18px;
    height: 50px;
    text-align: center;
}
.tp-text {
    color: #2ecc71;
    font-size: 2.2em;
    font-weight: bold;
    margin: 30px 0;
}
.sl-text {
    color: #e74c3c;
    font-size: 2.2em;
    font-weight: bold;
    margin: 30px 0;
}
h1, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center; margin-bottom:30px;'>💹 Trade Profit Calculator</h1>", unsafe_allow_html=True)

# Two main panels: Inputs | Outputs
col_input, col_output = st.columns(2)

with col_input:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h3>⚡ Inputs</h3>", unsafe_allow_html=True)

    margin = st.number_input("Margin (€)", min_value=1.0, step=1.0, key="margin")
    profit_target = st.number_input("Desired profit (€)", min_value=1.0, step=1.0, key="profit")
    entry_price = st.number_input("Entry price", min_value=0.0001, step=0.0001, format="%.4f", key="entry")
    leverage_input = st.number_input("Leverage (1× - 500×)", min_value=1.0, max_value=500.0, value=1.0, step=0.1, key="leverage")

    calculate = st.button("Calculate")
    st.markdown("</div>", unsafe_allow_html=True)

with col_output:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h3>📊 Trade Info</h3>", unsafe_allow_html=True)

    if calculate:
        if margin <= 0 or profit_target <= 0 or entry_price <= 0 or leverage_input <= 0:
            st.error("Please enter valid positive numbers!")
        else:
            price_change_pct = profit_target / (margin * leverage_input)
            tp_price = entry_price * (1 + price_change_pct)
            sl_price = entry_price * (1 - price_change_pct)

            tp_placeholder = st.empty()
            sl_placeholder = st.empty()

            steps = 20
            for i in range(1, steps+1):
                factor = i / steps
                tp_placeholder.markdown(f"<div class='tp-text'>🎯 TP: {entry_price*(1 + price_change_pct*factor):.4f}</div>", unsafe_allow_html=True)
                sl_placeholder.markdown(f"<div class='sl-text'>🛑 SL: {entry_price*(1 - price_change_pct*factor):.4f}</div>", unsafe_allow_html=True)
                time.sleep(0.03)
    else:
        st.markdown("<p style='color:gray;'>Results will appear here after calculation</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
