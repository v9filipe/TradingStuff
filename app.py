import streamlit as st

st.set_page_config(page_title="v9's Lil Demon V", page_icon="💹", layout="centered")

# --- Full black background ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title with bigger image ---
st.markdown("""
<h1 style='text-align:center;'>
    <img src="https://i.scdn.co/image/ab67616d00001e02dc9b911f1b9a866eba18d1a6" 
         style="height:48px; vertical-align:middle;"> 
    Trade Profit Calculator
</h1>
""", unsafe_allow_html=True)

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

        # --- Display results side by side ---
        res_col1, res_col2, res_col3, res_col4, res_col5 = st.columns(5)

        res_col1.metric("💡 Leverage used", f"{leverage}×")
        res_col2.metric("💡 Position size", f"€{position_size:.2f}")
        res_col3.metric("💡 Change needed", f"{price_change_pct*100:.2f}%")

        # Custom styled TP and SL with bigger numbers, single line, colored
        res_col4.markdown(f"""
        <div style="text-align:center;">
            <span style="font-size:18px; font-weight:600; color: #2ecc71;">🎯 Take-Profit:</span>
            <span style="font-size:22px; font-weight:600; color: #2ecc71;"> {tp_price:.4f}</span>
        </div>
        """, unsafe_allow_html=True)

        res_col5.markdown(f"""
        <div style="text-align:center;">
            <span style="font-size:18px; font-weight:600; color: #ff6b6b;">🛑 Stop-Loss:</span>
            <span style="font-size:22px; font-weight:600; color: #ff6b6b;"> {sl_price:.4f}</span>
        </div>
        """, unsafe_allow_html=True)
