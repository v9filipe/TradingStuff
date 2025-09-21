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
        # Calculate exact leverage needed
        leverage_required = profit_target / margin

        st.subheader("💡 Exact leverage needed")
        st.success(f"To achieve your profit target, you need approximately **{leverage_required:.2f}× leverage**")

        # Slider to adjust leverage
        st.subheader("⚡ Adjust leverage")
        leverage_slider = st.slider(
            "Choose your leverage",
            min_value=1.0,
            max_value=500.0,
            value=1.0,
            step=1.0
        )

        # Show marker for exact leverage
        st.markdown(f"🎯 **Exact leverage:** {leverage_required:.2f}×")

        # Calculate TP/SL for chosen leverage
        price_change_pct = profit_target / (margin * leverage_slider)
        tp_price = entry_price * (1 + price_change_pct)
        sl_price = entry_price * (1 - price_change_pct)

        st.subheader("📊 Trade info with chosen leverage")
        st.write(f"Selected leverage: **{leverage_slider:.2f}×**")
        st.write(f"Required price change: **{price_change_pct*100:.2f}%**")
        st.write(f"🎯 Take-Profit (TP): **{tp_price:.4f}**")
        st.write(f"🛑 Stop-Loss (SL): **{sl_price:.4f}**")

        # Optional visual bar
        st.markdown(
            f"<div style='position: relative; width: 100%; height: 20px; background-color: #eee;'>"
            f"<div style='position: absolute; left: {(leverage_required/500)*100:.2f}%; width: 2px; height: 20px; background-color: red;'></div>"
            f"</div>",
            unsafe_allow_html=True
        )
