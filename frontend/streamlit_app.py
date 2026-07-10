import streamlit as st
import requests

st.set_page_config(
    page_title="Jira Acceptance Criteria Agent",
    page_icon="🤖",
    layout="wide"
)

with st.sidebar:

    st.title("🤖 AI Acceptance Criteria")

    try:
        response = requests.get(
        "http://localhost:8000/health",
        timeout=2
        )

        if response.status_code == 200:
            st.success("🟢 Backend Connected")
        else:
            st.error("🔴 Backend Disconnected")

    except requests.exceptions.RequestException:
        st.error("🔴 Backend Disconnected")

    st.markdown("---")

    model = st.selectbox(
        "Model",
        [
            "llama3.1:8b",
            "qwen3:8b",
            "qwen3.5:2b"
        ]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.2,
        0.1
    )

    max_tokens = st.slider(
        "Max Tokens",
        256,
        4096,
        1024
    )

    st.markdown("---")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.title("🤖 AI Acceptance Criteria Generator")

st.caption(
    "Generate professional Jira Acceptance Criteria using Local LLMs."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input
prompt = st.chat_input(
    "Enter a Jira Story..."
)

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        

        with st.spinner(
            f"Generating using {model}..."
        ):

            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={
                        "model": model,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "messages": st.session_state.messages
                    }
                )

                answer = response.json()["response"]
                with st.container(border=True):

                    st.caption(
                        f"Generated using {model}"
                    )

                    st.markdown(answer)
            except Exception as e:
                answer = f"""
                        ### ❌ Unable to Generate Response

                        Reason

                        {str(e)}

                        Please verify

                        - Backend is running
                        - Ollama is running
                        - Selected model exists
                        """

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )