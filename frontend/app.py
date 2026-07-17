import streamlit as st

from utils import (
    send_command,
    get_devices,
    reset_home,
)

from styles import PAGE_STYLE

st.set_page_config(

    page_title="Ambient Smart Home",

    page_icon="🏠",

    layout="wide"
)

st.markdown(PAGE_STYLE, unsafe_allow_html=True)

# ------------------------
# Session State
# ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------
# Layout
# ------------------------

left, right = st.columns([1, 2])

# ========================
# Sidebar
# ========================

with left:

    st.title("🏠 Smart Home")

    devices = get_devices()

    icons = {

        "Light": "💡",

        "Fan": "🌀",

        "AC": "❄",

        "Door": "🔒"
    }

    for device, status in devices.items():

        if "Light" in device:
            icon = icons["Light"]

        elif "Fan" in device:
            icon = icons["Fan"]

        elif "AC" in device:
            icon = icons["AC"]

        else:
            icon = icons["Door"]

        css = "status-on"

        if status in ["OFF", "Locked"]:

            css = "status-off"

        st.markdown(
            f"""
<div class="device-card">
<h4>{icon} {device}</h4>
<p class="{css}">{status}</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    if st.button("🔄 Reset Home"):

        reset_home()

        st.rerun()

# ===========================
# Chat
# ===========================

with right:

    st.markdown(
        '<div class="chat-title">🤖 Ambient Smart Home Assistant</div>',
        unsafe_allow_html=True,
    )

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    prompt = st.chat_input("Control your smart home...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        result = send_command(prompt)

        answer = result["response"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

        st.rerun()