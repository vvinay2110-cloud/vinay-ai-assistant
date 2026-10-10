print("Starting Vinay's AI Assistant...")

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import ollama
import os
import signal
import streamlit.web.cli as stcli
import sys

# Configure page layout
st.set_page_config(page_title="Vinay's AI", page_icon="💬", layout="centered")
st.title("Vinay's AI Assistant")

st.text("Welcome to Vinay's AI Assistant! How can I help you today?")

# Choose which Ollama model to use (Ensure you ran 'ollama pull <model>' first)
MODEL_NAME = "llama3" 

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user chat input
if user_input := st.chat_input("What is on your mind? Type Here:"):
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response with streaming effect
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Call Ollama API with streaming enabled
        stream = ollama.chat(
            model=MODEL_NAME,
            messages=st.session_state.messages,
            stream=True,
        )
        
        for chunk in stream:
            full_response += chunk['message']['content']
            response_placeholder.markdown(full_response + "▌") # Blinking cursor effect
            
        response_placeholder.markdown(full_response) # Final message without cursor
        
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

if st.sidebar.button("❌ Shut Down Assistant"):
    st.sidebar.write("Stopping assistant server...")
    # This sends a termination signal to the active python process
    os.kill(os.getpid(), signal.SIGINT)
    print("Stopping Assistant...")

# Keep your main Python launcher at the very bottom
if __name__ == "__main__":

    if not os.environ.get("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())


if __name__ == "__main__":
    if not os.environ.get("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "true"
        # Adding the flag to stop the server when the browser window/tab closes
        sys.argv = [
            "streamlit", 
            "run", 
            __file__, 
            "--server.headless=true"
        ]
        sys.exit(stcli.main())