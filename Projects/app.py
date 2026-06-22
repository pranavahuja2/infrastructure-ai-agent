"""Infrastructure AI Agent — Streamlit Application (AWS Bedrock + Claude)."""

import streamlit as st
from agent.engine import get_client, get_agent_response, generate_summary, parse_phase

# --- Page Config ---
st.set_page_config(
    page_title="Infrastructure AI Agent",
    page_icon="🏗️",
    layout="wide",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🏗️ Infra AI Agent")
    st.markdown("**Your AI Solutions Engineer**")
    st.markdown("---")

    # Region selector
    region = st.selectbox(
        "AWS Region",
        ["us-east-1", "us-west-2", "eu-west-1"],
        index=0,
        help="Select the AWS region where Bedrock is enabled",
    )

    st.markdown("---")

    # Phase tracker
    st.markdown("### 📍 Session Progress")
    if "phase_info" in st.session_state:
        phase = st.session_state.phase_info
        phase_labels = {
            "DISCOVERY": "1. Discovery",
            "DEEP_DIVE": "2. Technical Deep-Dive",
            "REQUIREMENTS": "3. Requirements",
            "ARCHITECTURE": "4. Architecture",
            "SUMMARY": "5. Executive Summary",
        }
        current_label = phase_labels.get(phase["phase"], phase["phase"])
        st.markdown(f"**Current Phase:** {current_label}")
        st.progress(phase["progress"] / 100)
    else:
        st.markdown("**Current Phase:** Not started")
        st.progress(0)

    st.markdown("---")

    # Action buttons
    if st.button("📄 Generate Executive Summary", use_container_width=True):
        st.session_state.generate_summary = True

    if st.button("🗑️ Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.phase_info = {"phase": "DISCOVERY", "progress": 0}
        st.session_state.pop("generate_summary", None)
        st.rerun()

    st.markdown("---")
    st.markdown(
        "**How to use:**\n"
        "1. Describe your project\n"
        "2. Answer the agent's questions\n"
        "3. Get architecture recommendations\n"
        "4. Generate your executive summary"
    )
    st.markdown("---")
    st.markdown("*Powered by AWS Bedrock + Claude*")

# --- Main Chat Area ---
st.title("🏗️ Infrastructure Discovery Agent")
st.caption("I'll help you discover requirements and design your infrastructure architecture.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "phase_info" not in st.session_state:
    st.session_state.phase_info = {"phase": "DISCOVERY", "progress": 0}

# Create Bedrock client
try:
    client = get_client(region)
except Exception as e:
    st.error(f"Failed to connect to AWS Bedrock: {e}\n\nMake sure your AWS credentials are configured.")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle summary generation
if st.session_state.get("generate_summary"):
    st.session_state.pop("generate_summary")
    if not st.session_state.messages:
        st.warning("Start a conversation first before generating a summary.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Generating executive summary..."):
                project_name = "Infrastructure Project"
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        project_name = msg["content"][:50]
                        break
                summary = generate_summary(client, st.session_state.messages, project_name)
                st.markdown(summary)
                st.download_button(
                    label="📥 Download Summary (Markdown)",
                    data=summary,
                    file_name="executive_summary.md",
                    mime="text/markdown",
                )
        st.session_state.messages.append({"role": "assistant", "content": summary})

# Chat input
if prompt := st.chat_input("Describe your project or answer the agent's questions..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = get_agent_response(client, st.session_state.messages)

                # Parse phase info
                st.session_state.phase_info = parse_phase(response)

                # Display response (hide phase tracking line)
                display_response = "\n".join(
                    line for line in response.split("\n")
                    if not line.strip().startswith("[PHASE:")
                )
                st.markdown(display_response)
            except Exception as e:
                st.error(f"Error getting response: {e}")
                response = None

    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
