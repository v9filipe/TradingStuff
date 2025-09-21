import streamlit as st
import time

st.set_page_config(page_title="Trade Profit Calculator", page_icon="💹", layout="wide")

# Dark theme CSS
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        height: 100%;
        margin: 0;
        background-color: #0b0b0c;
        color: #e5e5e5;
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }
    .main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        text-align: center;
    }
    label, .stNumberInput label {
        color: #ffffff !important;
        font-size: 16px;
    }
    input[type=number], .stTextInput>div>input {
        height: 48px;
        font-size: 18px;
        text-align: center;
        background: #1c1c1e;
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        height: 52px;
        width: 220px;
        font-size: 17px;
        border-radius: 10px;
        margin: 18px auto;
        display: block;
    }
    .outputs {
        display: flex;
        justify-content: center;
        gap: 60px;
        margin-top: 20px;
    }
    .tp { color: #2ecc71; font-size: 2em; font-weight: 700; }
    .sl { color: #ff6b6b; font-size: 2em; font-weight: 700; }
    .results-title { 
        margin-top: 30px; 
        font-size: 20px; 
        font-weight: 600; 
        color: #9aa0a6;
    }
    </style>
    """, unsafe_allow_html=True
)

# Wrapper div
st.markdown('<div class="main">', unsafe_allow_html=True)

# Title
st.markdown("<h1 style='color:white;'>💹 Trade Profit Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9aa0a6;'>Enter your trade details and press <b>Calculate</b></p>", unsafe_allow_html=True)

# Inputs
margin = st.number_input("Margin (€)", min_value=1.0, step=1.0, value=100.0, key="margin")
profit_target = st.number_input("Desired profit (€)", min_value=1.0, step=1.0, value=50.0, key="profit")
entry_price = st.number_input("Entry price", min_value=0.0001, step=0.0001, format="%.4f", value=1.45, key="entry")
leverage_input = st.number_input("Leverage (1× - 500×)", min_value=1.0, max_value=500.0, value=1.0, step=0.1, key="leverage")

calculate = st.button("Calculate")

# Output
if not st.session_state.get("calculated", False) and not calculate:
    st.markdown('<div style="color:#9aa0a6;">Results will appear here after you press <b>Calculate</b>.</div>', unsafe_allow_html=True)
else:
    if calculate:
        st.session_state["calculated"] = True

    if margin <= 0 or profit_target <= 0 or entry_price <= 0 or leverage_input <= 0:
        st.error("Please enter valid positive numbers!")
    else:
        position_size = margin * leverage_input
        price_change_pct = profit_target / position_size
        tp_price = entry_price * (1 + price_change_pct)
        sl_price = entry_price * (1 - price_change_pct)

        # Subtitle
        st.markdown('<div class="results-title">📊 Results</div>', unsafe_allow_html=True)

        # Animated output (side by side)
        tp_ph = st.empty()

        steps = 18
        for i in range(1, steps + 1):
            factor = i / steps
            tp_val = entry_price * (1 + price_change_pct * factor)
            sl_val = entry_price * (1 - price_change_pct * factor)
            html = f"""
            <div class="outputs">
                <div class="tp">🎯 TP: {tp_val:.4f}</div>
                <div class="sl">🛑 SL: {sl_val:.4f}</div>
            </div>
            """
            tp_ph.markdown(html, unsafe_allow_html=True)
            time.sleep(0.02)

        final_html = f"""
        <div class="outputs">
            <div class="tp">🎯 TP: {tp_price:.4f}</div>
            <div class="sl">🛑 SL: {sl_price:.4f}</div>
        </div>
        """
        tp_ph.markdown(final_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
