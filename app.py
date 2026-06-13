import streamlit as st
from google import genai

st.title("♊ Gemini AI Chatbot")

# 1. Setup API Key Input in Sidebar
with st.sidebar:
    st.header("Configuration")
    # Prompt user for API key, or look for it in Streamlit Secrets if left blank
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    # Automatically fallback to Streamlit Secrets if available in the cloud
    if not api_key and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    
    st.info(
        "💡 Don't have an API key? Get one from [Google AI Studio](https://aistudio.google.com/)."
    )

# 2. Check if API Key is available
if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to start chatting.")
    st.stop()

# 3. Initialize the Google GenAI Client & Session State securely using the variable
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=api_key)

# We use the official GenAI chat helper to maintain stateful history automatically
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
        model="gemini-2.5-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Render existing chat history in Streamlit UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("Ask Gemini anything..."):
    # Render user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Store user message in local history tracking (for rendering)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Render Assistant placeholder and call the Gemini API
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            # Send message to Gemini using the stateful chat session
            response = st.session_state.gemini_chat.send_message(prompt)
            
            # Display response text 
            response_placeholder.markdown(response.text)
            
            # Store assistant message in local history tracking
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
