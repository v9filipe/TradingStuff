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
        # Calculate total position
        position_size = margin * leverage

        # Required % change on total position to hit profit
        price_change_pct = profit_target / position_size  # decimal

        # TP and SL
        tp_price = entry_price * (1 + price_change_pct)
        sl_price = entry_price * (1 - price_change_pct)

        # --- Display results side by side with custom sizes ---
        res_col1, res_col2, res_col3, res_col4, res_col5 = st.columns(5)

        res_col1.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:18px; font-weight:600;'>💡 Leverage used</div>
            <div style='font-size:16px;'>{leverage}×</div>
        </div>
        """, unsafe_allow_html=True)

        res_col2.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:18px; font-weight:600;'>💡 Position size</div>
            <div style='font-size:16px;'>€{position_size:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        res_col3.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:18px; font-weight:600;'>💡 Required price change</div>
            <div style='font-size:16px;'>{price_change_pct*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

        res_col4.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:18px; font-weight:600;'>🎯 Take-Profit (TP)</div>
            <div style='font-size:16px;'>{tp_price:.4f}</div>
        </div>
        """, unsafe_allow_html=True)

        res_col5.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:18px; font-weight:600;'>🛑 Stop-Loss (SL)</div>
            <div style='font-size:16px;'>{sl_price:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
