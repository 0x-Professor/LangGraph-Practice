import streamlit as st
import requests
import json
from datetime import datetime
import time
import uuid

# Configure Streamlit page
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean, professional CSS
st.markdown("""
<style>
    /* Hide Streamlit branding and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid #e6e6e6;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1rem;
        color: #666;
        font-weight: 400;
    }
    
    /* Status indicator */
    .status-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0.5rem;
        margin-bottom: 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    .status-online {
        background-color: #e8f5e8;
        color: #2d5a2d;
        border: 1px solid #c3e6c3;
    }
    
    .status-offline {
        background-color: #fdf2f2;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    /* Chat messages */
    .chat-container {
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: #fafafa;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Control buttons */
    .control-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .control-btn {
        background: white;
        border: 1px solid #ddd;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        color: #555;
        text-decoration: none;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .control-btn:hover {
        border-color: #4285f4;
        color: #4285f4;
    }
    
    /* Input styling */
    .stChatInput > div > div > textarea {
        border-radius: 25px !important;
        border: 1px solid #ddd !important;
        padding: 12px 20px !important;
    }
    
    /* Message styling */
    .stChatMessage {
        padding: 0.75rem 0;
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        color: #666;
        font-style: italic;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 12px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'backend_status' not in st.session_state:
    st.session_state.backend_status = "unknown"

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return "online"
        return "error"
    except requests.exceptions.RequestException:
        return "offline"

def send_message_to_backend(message, session_id):
    """Send message to backend API"""
    try:
        payload = {
            "message": message,
            "session_id": session_id
        }
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Backend error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

def clear_chat_session(session_id):
    """Clear chat session on backend"""
    try:
        response = requests.delete(f"{API_BASE_URL}/chat/session/{session_id}", timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Header
st.markdown("""
<div class="app-header">
    <div class="app-title">AI ChatBot</div>
    <div class="app-subtitle">Powered by Google Gemini</div>
</div>
""", unsafe_allow_html=True)

# Status check
if st.session_state.backend_status == "unknown":
    st.session_state.backend_status = check_backend_health()

# Status indicator
if st.session_state.backend_status == "online":
    st.markdown("""
    <div class="status-bar status-online">
        ● Connected
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-bar status-offline">
        ● Disconnected - Please start the backend server
    </div>
    """, unsafe_allow_html=True)
    st.error("Run `python main.py` to start the backend server")
    st.stop()

# Control buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        if clear_chat_session(st.session_state.session_id):
            st.session_state.messages = []
            st.rerun()

with col3:
    if st.button("📊 Status", use_container_width=True):
        st.session_state.backend_status = check_backend_health()
        st.rerun()

with col4:
    if st.session_state.messages:
        chat_export = {
            "session_id": st.session_state.session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            label="💾 Export",
            data=json.dumps(chat_export, indent=2),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

# Chat display area
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-message">
        Welcome! Start a conversation by typing a message below.
    </div>
    """, unsafe_allow_html=True)
else:
    # Display chat messages in a clean container
    for message in st.session_state.messages:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.write(message['content'])

# Chat input
user_input = st.chat_input(
    "Type your message here...",
    disabled=st.session_state.backend_status != "online"
)

# Process user input
if user_input:
    # Add user message to chat
    user_message = {
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    # Display user message immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # Show typing indicator and get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = send_message_to_backend(user_input, st.session_state.session_id)
    
    # Handle response
    if "error" in response:
        st.error(f"Error: {response['error']}")
        # Remove the user message if there was an error
        st.session_state.messages.pop()
    else:
        # Add bot response to chat
        bot_message = {
            'role': 'assistant',
            'content': response['response'],
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.messages.append(bot_message)
        
        # Display bot response
        with st.chat_message("assistant"):
            st.write(response['response'])
    
    # Rerun to update the interface
    st.rerun()

# Simple footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #888; font-size: 0.8rem;'>"
    f"Session: {st.session_state.session_id[:8]}... | "
    f"Messages: {len(st.session_state.messages)}"
    f"</div>", 
    unsafe_allow_html=True
)

