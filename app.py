import streamlit as st
import asyncio

from agent import root_agent, get_agent_response
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Standard Python libraries
import warnings
import logging

import os
import dotenv
import random

# --- Asyncio Configuration for Streamlit ---
# Required to run async ADK functions within Streamlit's synchronous environment
import nest_asyncio
nest_asyncio.apply()

dotenv.load_dotenv()

# --- Basic Configuration ---
warnings.filterwarnings("ignore") # Suppress common warnings
logging.basicConfig(level=logging.ERROR) # Reduce log verbosity
logger = logging.getLogger(__name__)

st.title("🏥 Medicare Guide!")

# Show welcome message only on first load
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = True
    st.session_state.user_id = f"streamlit_user_{random.randint(1, 100000)}"
    st.session_state.session_id = f"streamlit_session_{random.randint(1, 100000)}"
    # Main welcome message
    st.markdown("""        
    ### 💡 Examples of questions you can ask me:
    - "What are the different parts of Medicare?"
    - "When can I enroll in Medicare?"
    - "What's the difference between Original Medicare and Medicare Advantage?"
    """)
    
# Disclaimer
st.info("🔔 Note: I provide information from the official [Medicare & You Handbook 2025](https://www.medicare.gov/publications/10050-medicare-and-you.pdf), but am not perfect! I will always do my best to provide page numbers, and I strongly suggest checking for yourself.")

# --- Initialize ADK Runner and Session Service ---
@st.cache_resource # Cache the runner and session service infrastructure
def initialize_adk_infra(_root_agent):
    if not _root_agent:
        st.error("Cannot initialize ADK Infra, Root Agent not available.")
        st.stop()

    app_name="Medicare Guide"
    session_service = InMemorySessionService()
    adk_session = session_service.create_session(
        app_name=app_name,
        user_id=st.session_state.user_id,
        session_id=st.session_state.session_id,
    )

    runner = Runner(
        app_name="Medicare Guide",
        agent=root_agent,
        session_service=session_service,
    )
    
    return {
        "runner": runner, "session_service": session_service,
        "app_name": app_name, "user_id": st.session_state.user_id, "session_id": st.session_state.session_id
        }


# --- Get ADK infrastructure components ---
# This uses the cached infrastructure unless cleared.
adk_infra = initialize_adk_infra(root_agent)
runner = adk_infra["runner"]
session_service = adk_infra["session_service"]
app_name = adk_infra["app_name"]
user_id = adk_infra["user_id"]
session_id = adk_infra["session_id"]
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        try:
            response_text = asyncio.run(get_agent_response(runner, prompt, user_id, session_id))
            st.markdown(response_text, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred during agent interaction: {e}")
            response_text = f"Sorry, a critical error occurred: {e}"
            logger.error(f"An error occurred during agent interaction: {e}", exc_info=True)
            
    st.session_state.messages.append({"role": "assistant", "content": response_text})        