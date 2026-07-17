import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Ambient Smart Home Assistant",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "device_status" not in st.session_state:
    st.session_state.device_status = {
        "Bedroom Light": "OFF",
        "Living Room Light": "OFF",
        "Kitchen Light": "OFF",
        "Fan": "OFF",
        "AC": "OFF",
        "Door": "Locked"
    }

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🏠 Smart Home")

    st.markdown("---")

    st.subheader("Device Status")

    for device, status in st.session_state.device_status.items():

        if status in ["ON", "Unlocked"]:
            st.success(f"{device}: {status}")
        else:
            st.error(f"{device}: {status}")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 Ambient Smart Home Assistant")

st.caption("Powered by LangGraph + Groq + FastAPI")

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Enter your smart home command...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/invoke",
                json={
                    "command": prompt
                },
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                assistant_reply = f"""
**Action:** {result['action']}

**Device:** {result['device']}
"""

                # Update Device Status (simple logic)

                action = result["action"].lower()
                device = result["device"]

                if "turn on" in action:
                    st.session_state.device_status[device] = "ON"

                elif "turn off" in action:
                    st.session_state.device_status[device] = "OFF"

                elif "unlock" in action:
                    st.session_state.device_status[device] = "Unlocked"

                elif "lock" in action:
                    st.session_state.device_status[device] = "Locked"

            else:

                assistant_reply = f"Server Error ({response.status_code})"

        except Exception as e:

            assistant_reply = str(e)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)