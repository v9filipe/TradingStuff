import streamlit as st
import time

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="wide")

# Minimal CSS for a clean dark theme and slightly larger centered inputs
st.markdown(
    """
    <style>
    :root {
        --bg: #0b0b0c;
        --panel: #141516;
        --muted: #9aa0a6;
        --accent: #4CAF50;
    }
    body {
        background-color: var(--bg);
        color: #FFFFFF;
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }
    .panel {
        background-color: var(--panel);
        border-radius: 12px;
        padding: 28px;
        margin: 8px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        min-height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .panel h3 { margin-top: 0; margin-bottom: 16px; color: #ffffff; }
    .muted { color: var(--muted); margin-bottom: 10px; }
    /* enlarge numeric inputs */
    input[type=number], .stTextInput>div>input {
        height: 48px;
        font-size: 18px;
        text-align: center;
        background: transparent;
        color: #fff;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
    }
    .stButton>button {
        background-color: var(--accent);
        color: white;
        height: 52px;
        width: 100%;
        font-size: 17px;
        border-radius: 10px;
    }
    .tp { color: #2ecc71; font-size: 2em; font-weight: 700; margin: 14px 0; text-align:center; }
    .sl { color: #ff6b6b; font-size: 2em; font-weight: 700; margin: 14px 0; text-align:center; }
    </style>
    """, unsafe_allow_html=True
)

# Title centered
st.markdown("""
<div style="text-align:center; padding-top:6px; padding-bottom:6px;">
    <h1 style="margin:0; color:#fff;">💹 Trade Profit Calculator</h1>
    <p style="color: #9aa0a6; margin-top:6px;">Enter your trade details and press <b>Calculate</b></p>
</div>
""", unsafe_allow_html=True)

# Two main panels side-by-side (Inputs | Trade Info)
left_col, right_col = st.columns(2)

# INPUTS panel (always visible)
with left_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<h3>⚡ Inputs</h3>', unsafe_allow_html=True)

    margin = st.number_input("Margin (€)", min_value=1.0, step=1.0, value=100.0, key="margin")
    profit_target = st.number_input("Desired profit (€)", min_value=1.0, step=1.0, value=50.0, key="profit")
    entry_price = st.number_input("Entry price", min_value=0.0001, step=0.0001, format="%.4f", value=1.45, key="entry")
    leverage_input = st.number_input("Leverage (1× - 500×)", min_value=1.0, max_value=500.0, value=1.0, step=0.1, key="leverage")

    calculate = st.button("Calculate")
    st.markdown('</div>', unsafe_allow_html=True)

# OUTPUT panel (always visible but shows placeholder text until calculate)
with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Trade Info</h3>', unsafe_allow_html=True)

    if not st.session_state.get("calculated", False) and not calculate:
        st.markdown('<div style="color:#9aa0a6">Results will appear here after you press <b>Calculate</b>.</div>', unsafe_allow_html=True)
    else:
        if calculate:
            st.session_state["calculated"] = True
            st.session_state["margin"] = margin
            st.session_state["profit_target"] = profit_target
            st.session_state["entry_price"] = entry_price
            st.session_state["leverage_input"] = leverage_input

        margin_v = st.session_state.get("margin", margin)
        profit_v = st.session_state.get("profit_target", profit_target)
        entry_v = st.session_state.get("entry_price", entry_price)
        leverage_v = st.session_state.get("leverage_input", leverage_input)

        if margin_v <= 0 or profit_v <= 0 or entry_v <= 0 or leverage_v <= 0:
            st.error("Please enter valid positive numbers!")
        else:
            position_size = margin_v * leverage_v
            price_change_pct = profit_v / position_size  # decimal
            tp_price = entry_v * (1 + price_change_pct)
            sl_price = entry_v * (1 - price_change_pct)

            tp_ph = st.empty()
            sl_ph = st.empty()
            steps = 18
            for i in range(1, steps + 1):
                factor = i / steps
                tp_ph.markdown(f'<div class="tp">🎯 TP: {entry_v * (1 + price_change_pct * factor):.4f}</div>', unsafe_allow_html=True)
                sl_ph.markdown(f'<div class="sl">🛑 SL: {entry_v * (1 - price_change_pct * factor):.4f}</div>', unsafe_allow_html=True)
                time.sleep(0.02)

            tp_ph.markdown(f'<div class="tp">🎯 TP: {tp_price:.4f}</div>', unsafe_allow_html=True)
            sl_ph.markdown(f'<div class="sl">🛑 SL: {sl_price:.4f}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
