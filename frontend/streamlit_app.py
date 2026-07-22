import streamlit as st
import requests
import re
from streamlit_mermaid_interactive import mermaid
import streamlit.components.v1 as components

def render_mermaid(code: str, height: int = 500):
    components.html(
        f"""
        <div class="mermaid">{code}</div>
        <script type="module">
            import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
            mermaid.initialize({{ startOnLoad: true, theme: "default" }});
        </script>
        """,
        height=height,
        scrolling=True,
    )

st.set_page_config(
    page_title="Jira Acceptance Criteria Agent",
    page_icon="🤖",
    layout="wide"
)

def sanitize_and_format_mermaid(raw_code: str) -> str:
    """
    Cleans up double-wrapping, repairs mashed-together keywords,
    and breaks single-line diagrams into valid multi-line Mermaid syntax.
    """
    if not raw_code:
        return ""
    
    # 1. Strip out any existing markdown fences or rogue "mermaid" prefixes
    code = re.sub(r"^```(mermaid)?\s*", "", raw_code, flags=re.IGNORECASE)
    code = re.sub(r"^mermaid\s*", "", code, flags=re.IGNORECASE)
    code = re.sub(r"\s*```$", "", code).strip()
    
    # 2. Fix the missing newline after the initial flowchart declaration
    code = re.sub(r"^(flowchart|graph)\s+(TD|LR|TB|BT|RL)\s*", r"\1 \2\n    ", code, flags=re.IGNORECASE)
    
    # 3. Fix single-line mashups: Insert a newline before any 1-2 letter node ID 
    # that is followed by an arrow (-->) or a shape bracket ([ or { or ()
    node_boundary_pattern = r"\s+\b([A-Z]{1,2})\b(?=\s*(-->|[\{\[\(]))"
    code = re.sub(node_boundary_pattern, r"\n    \1", code)
    
    return code.strip()

def clean_main_response(text: str) -> str:
    """
    Slices away any fenced or raw unfenced mermaid leaks from the main conversational text.
    """
    if not text:
        return ""
    # Remove any fenced blocks
    cleaned = re.sub(r"```mermaid.*?```", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Cut off any raw unfenced leaks starting with 'mermaid flowchart' or 'mermaid graph'
    cleaned = re.sub(r"\bmermaid\s+(flowchart|graph)\b.*$", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()


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
            "nvidia/nemotron-3-ultra-550b-a55b:free"
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
st.caption("Generate professional Jira Acceptance Criteria")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation history cleanly
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(clean_main_response(message["content"]))
            if message.get("mermaid"):
                formatted_chart = sanitize_and_format_mermaid(message["mermaid"])
                
                render_mermaid(formatted_chart)
        else:
            st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Enter a Jira Story...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Generating using {model}..."):
            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={
                        "model": model,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    },
                    timeout=120
                )
                
                data = response.json()
                answer = data.get("response", "")
                mermaid_code = data.get("mermaid")

                # Clean up the main text completely
                clean_answer = clean_main_response(answer)

                with st.container(border=True):
                    st.caption(f"Generated using {model}")
                    st.markdown(clean_answer)
                    
                    # Process and render the diagram visually
                    if mermaid_code:

                        st.markdown("### 🌊 Process Flow")

                        mermaid(
                            mermaid_code,
                            theme="neutral",
                            key="flow"
                        )

            except Exception as e:
                answer = f"""
                        ### ❌ Unable to Generate Response
                        **Reason:**
                        {str(e)}
                        
                        **Please verify:**
                        - Backend is running
                        - Selected model is available
                        """
                mermaid_code = None
                st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "mermaid": mermaid_code
        }
    )