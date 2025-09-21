import streamlit as st
import pandas as pd

st.set_page_config(page_title="Leverage & TP/SL Calculator", page_icon="💹", layout="wide")
st.title("📊 Leverage & TP/SL Calculator")

st.markdown("""
This app calculates **exact leverage**, **take-profit (TP)**, and **stop-loss (SL)** based on:
- Your **margin**
- Desired **profit target**
- **Entry price**
- Expected **price move (%)**
""")

# User inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    margin = st.number_input("💰 Margin (your money)", min_value=1.0, step=1.0)
with col2:
    profit_target = st.number_input("🎯 Profit target (€)", min_value=1.0, step=1.0)
with col3:
    entry_price = st.number_input("📍 Entry price", min_value=0.0001, step=0.0001, format="%.4f")
with col4:
    price_move_pct = st.number_input("📈 Expected price move (%)", min_value=0.01, step=0.01, value=2.0)

price_move = price_move_pct / 100

if st.button("Calculate"):
    if margin <= 0 or profit_target <= 0 or entry_price <= 0 or price_move <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        required_roi = profit_target / margin
        st.subheader("🔹 Required ROI")
        st.write(f"**{required_roi*100:.2f}%** on your margin")

        # Exact leverage
        exact_leverage = required_roi / price_move
        st.subheader("💡 Exact Leverage Needed")
        st.success(f"With a **{price_move_pct:.2f}% expected price move**, you need **{exact_leverage:.2f}× leverage**")

        st.markdown("---")
        st.subheader("📊 TP & SL Table for Leverages 1× to 100×")

        # Build table
        data = []
        for lev in range(1, 101):
            tp_price = entry_price * (1 + required_roi / lev)
            sl_price = entry_price * (1 - required_roi / lev)
            highlight = lev == round(exact_leverage)
            data.append({
                "Leverage": f"{lev}× {'⬅️ Exact' if highlight else ''}",
                "Take-Profit (TP)": tp_price,
                "Stop-Loss (SL)": sl_price
            })

        df = pd.DataFrame(data)
        # Color formatting
        def color_tp(val):
            return 'background-color: #d4edda'  # green
        def color_sl(val):
            return 'background-color: #f8d7da'  # red

        styled_df = df.style.applymap(color_tp, subset=["Take-Profit (TP)"]) \
                            .applymap(color_sl, subset=["Stop-Loss (SL)"])
        st.dataframe(styled_df, height=500)

        st.subheader("ℹ️ Notes")
        st.write("""
        - Exact leverage is calculated based on your **expected price move**.  
        - TP is highlighted in **green**, SL in **red**.  
        - Use the table to pick a leverage that fits your **risk tolerance**.  
        - Always consider fees and slippage when placing real trades.
        """)
