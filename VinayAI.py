import streamlit as st
import os
from groq import Groq

# 1. Configure the page layout and title
st.set_page_config(
    page_title="Vinay's AI", 
    page_icon="💬", 
    layout="centered"
)

st.title("Vinay's AI Assistant")
st.text("Welcome to Vinay's AI Assistant! How can I help you today?")

# 2. Authenticate the API Key (Securely checks Streamlit Secrets or Environment Variables)
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.environ.get("GROQ_API_KEY")

# Stop the app gracefully if the key isn't provided yet
if not api_key:
    st.info("Please add your GROQ_API_KEY to the Streamlit secrets panel to proceed.", icon="🗝️")
    st.stop()

# Initialize the Groq Client
client = Groq(api_key=api_key)

# 3. Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Accept user chat input
if user_input := st.chat_input("What is on your mind? Type Here:"):
    
    # Add user message to history and instantly show it in the UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 6. Generate assistant response with a streaming effect
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Call Groq API with streaming enabled using the llama3 model
        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        
        # Render chunks as they come in to look like typing
        for chunk in stream:
            if chunk.choices.delta.content is not None:
                full_response += chunk.choices.delta.content
                response_placeholder.markdown(full_response + "▌") # Blinking cursor effect
        
        # Display the final complete message without the cursor
        response_placeholder.markdown(full_response)

    # Add the assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 7. Sidebar options (Replaces the server shutdown button with a chat wiper)
st.sidebar.title("Options")
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.rerun()
