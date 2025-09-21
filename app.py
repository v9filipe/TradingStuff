import streamlit as st
import time

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="wide")

st.markdown("""
# 💹 Trade Profit Calculator

Calculate **Take-Profit (TP)** and **Stop-Loss (SL)** for your trade based on:
- Your **margin**
- Desired **profit target**
- Expected **entry price**
- Chosen leverage
""")

# Columns for inputs and outputs
col_input, col_output = st.columns([1, 1])

with col_input:
    st.subheader("⚡ Inputs")
    margin = st.number_input("💰 Margin (your money)", min_value=1.0, step=1.0)
    profit_target = st.number_input("🎯 Desired profit (€)", min_value=1.0, step=1.0)
    entry_price = st.number_input("📍 Expected entry price", min_value=0.0001, step=0.0001, format="%.4f")
    leverage_input = st.number_input(
        "⚡ Enter leverage (1× - 500×)",
        min_value=1.0,
        max_value=500.0,
        value=1.0,
        step=0.1
    )
    calculate = st.button("Calculate")

with col_output:
    st.subheader("📊 Trade Info")
    leverage_placeholder = st.empty()
    change_placeholder = st.empty()
    tp_box = st.empty()
    sl_box = st.empty()
    bar_placeholder = st.empty()

# Function to draw bar
def draw_bar(entry, tp, sl, width=500):
    entry_pos = 50
    tp_pos = entry_pos + (tp - entry) / entry * 200
    sl_pos = entry_pos - (entry - sl) / entry * 200
    bar_html = f"""
    <div style='position: relative; width:{width}px; height:30px; background-color:#eee; border-radius:5px;'>
        <div style='position:absolute; left:{entry_pos}px; width:2px; height:30px; background-color:black;'></div>
        <div style='position:absolute; left:{tp_pos}px; width:2px; height:30px; background-color:green;'></div>
        <div style='position:absolute; left:{sl_pos}px; width:2px; height:30px; background-color:red;'></div>
    </div>
    """
    return bar_html

# Calculate and animate
if calculate:
    if margin <= 0 or profit_target <= 0 or entry_price <= 0 or leverage_input <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        price_change_pct = profit_target / (margin * leverage_input)
        tp_price = entry_price * (1 + price_change_pct)
        sl_price = entry_price * (1 - price_change_pct)

        # Animate numbers
        steps = 20
        for i in range(1, steps + 1):
            factor = i / steps
            leverage_placeholder.markdown(f"Selected leverage: **{leverage_input:.2f}×**")
            change_placeholder.markdown(f"Required price change: **{price_change_pct*100*factor:.2f}%**")
            tp_box.markdown(f"<div style='background-color:#d4edda; padding:10px; border-radius:5px;'>🎯 Take-Profit (TP): **{entry_price*(1 + price_change_pct*factor):.4f}**</div>", unsafe_allow_html=True)
            sl_box.markdown(f"<div style='background-color:#f8d7da; padding:10px; border-radius:5px;'>🛑 Stop-Loss (SL): **{entry_price*(1 - price_change_pct*factor):.4f}**</div>", unsafe_allow_html=True)
            bar_placeholder.markdown(draw_bar(entry_price, entry_price*(1 + price_change_pct*factor), entry_price*(1 - price_change_pct*factor)), unsafe_allow_html=True)
            time.sleep(0.05)
