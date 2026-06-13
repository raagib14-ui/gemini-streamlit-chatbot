import streamlit as st
from google import genai

st.title("♊ Gemini AI Chatbot")

# Initialize the API key variable
api_key = None

# 1. Smart API Key Configuration
# Check if the secret exists in Streamlit Cloud first
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    with st.sidebar:
        st.header("Status")
        st.success("🤖 Chatbot is live and ready!")
else:
    # Fallback for local testing in Jupyter/Command Prompt
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter Gemini API Key (Local Testing):", type="password")
        st.info("💡 Leave empty if deploying to Streamlit Cloud with Secrets.")

# 2. Block execution if no key is found anywhere
if not api_key:
    st.warning("Please configure your Gemini API Key to start chatting.")
    st.stop()

# 3. Initialize Client & Stateful Chat Session
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=api_key)

if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = st.session_state.gemini_client.chats.create(
        model="gemini-2.5-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Render existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("Ask Gemini anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            response = st.session_state.gemini_chat.send_message(prompt)
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
