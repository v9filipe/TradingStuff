import streamlit as st

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹")
st.title("💹 Trade Profit Calculator")

st.markdown("""
Calculate the **leverage, take-profit (TP), and stop-loss (SL)** based on:
- Your **margin**
- Desired **profit target**
- Expected **entry price**
""")

# User inputs
margin = st.number_input("💰 Margin (your money)", min_value=1.0, step=1.0)
profit_target = st.number_input("🎯 Desired profit (€)", min_value=1.0, step=1.0)
entry_price = st.number_input("📍 Expected entry price", min_value=0.0001, step=0.0001, format="%.4f")

if st.button("Calculate"):
    if margin <= 0 or profit_target <= 0 or entry_price <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        # Calculate required leverage
        leverage_required = profit_target / margin

        # Take-Profit and Stop-Loss assuming symmetric price move
        tp_price = entry_price * (1 + (profit_target / (margin * leverage_required)))
        sl_price = entry_price * (1 - (profit_target / (margin * leverage_required)))

        st.subheader("💡 Trade Info")
        st.write(f"⚡ Required leverage to achieve profit: **{leverage_required:.2f}×**")
        st.write(f"🎯 Take-Profit (TP): **{tp_price:.4f}**")
        st.write(f"🛑 Stop-Loss (SL): **{sl_price:.4f}**")
