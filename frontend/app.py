import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Smart Home Assistant",
    page_icon="🏠",
    layout="wide"
)

# -----------------------
# Session State
# -----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "devices" not in st.session_state:

    st.session_state.devices = requests.get(
        f"{API_URL}/devices"
    ).json()

THREAD_ID = "gaurav"

# -----------------------
# Title
# -----------------------

st.title("🏠 Smart Home Assistant")

left, right = st.columns([2, 1])

# ===================================================
# CHAT
# ===================================================

with left:

    st.subheader("💬 Chat")

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Type your command...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = requests.post(

            f"{API_URL}/chat",

            json={
                "thread_id": THREAD_ID,
                "command": prompt
            }

        ).json()

        assistant_response = response["response"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )

        st.session_state.devices = response["devices"]

        st.rerun()

# ===================================================
# DEVICE DASHBOARD
# ===================================================

with right:

    st.subheader("🏠 Devices")

    ICONS = {
        "Bedroom Light": "💡",
        "Kitchen Light": "💡",
        "Living Room Light": "💡",
        "Fan": "🌀",
        "AC": "❄️",
        "Door": "🚪"
    }

    for device, status in st.session_state.devices.items():

        icon = ICONS.get(device, "🔹")

        if status == "ON":
            emoji = "🟢"

        elif status == "OFF":
            emoji = "⚪"

        elif status == "Locked":
            emoji = "🔒"

        elif status == "Unlocked":
            emoji = "🔓"

        else:
            emoji = "🔵"

        st.write(f"{icon} **{device}**")

        st.write(f"{emoji} {status}")

        st.divider()

    if st.button("🔄 Reset Devices"):

        response = requests.post(
            f"{API_URL}/reset"
        ).json()

        st.session_state.devices = response["devices"]

        st.success(response["message"])

        st.rerun()