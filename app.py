import streamlit as st

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹")
st.title("💹 Trade Profit Calculator")

st.markdown("""
Calculate the **Take-Profit (TP)** and **Stop-Loss (SL)** for your trade based on:
- Margin (money you put in)
- Chosen leverage
- Desired profit
- Expected entry price
""")

# User inputs
margin = st.number_input("💰 Margin (your money)", min_value=1.0, step=1.0)
leverage = st.number_input("⚡ Leverage", min_value=1.0, step=1.0)
profit_target = st.number_input("🎯 Desired profit (€)", min_value=1.0, step=1.0)
entry_price = st.number_input("📍 Expected entry price", min_value=0.0001, step=0.0001, format="%.4f")

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
        sl_price = entry_price * (1 - price_change_pct)  # symmetric

        st.subheader("📊 Trade Details")
        st.write(f"💡 Leverage used: **{leverage}×**")
        st.write(f"💡 Position size: **€{position_size:.2f}**")
        st.write(f"💡 Required price change: **{price_change_pct*100:.2f}%**")
        st.write(f"🎯 Take-Profit (TP): **{tp_price:.4f}**")
        st.write(f"🛑 Stop-Loss (SL): **{sl_price:.4f}**")
