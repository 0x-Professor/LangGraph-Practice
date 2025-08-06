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
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #4caf50;
    }
    .status-offline {
        background-color: #f44336;
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

def load_chat_history(session_id):
    """Load chat history from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/chat/history/{session_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("messages", [])
        return []
    except requests.exceptions.RequestException:
        return []

def clear_chat_session(session_id):
    """Clear chat session on backend"""
    try:
        response = requests.delete(f"{API_BASE_URL}/chat/session/{session_id}", timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI ChatBot</h1>
    <p>Powered by Google Gemini via LangGraph</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Chat Controls")
    
    # Backend status check
    if st.button("🔄 Check Backend Status"):
        st.session_state.backend_status = check_backend_health()
    
    # Display status
    status_color = "status-online" if st.session_state.backend_status == "online" else "status-offline"
    status_text = "🟢 Online" if st.session_state.backend_status == "online" else "🔴 Offline"
    
    st.markdown(f"""
    <div class="sidebar-info">
        <h4>Backend Status</h4>
        <span class="status-indicator {status_color}"></span>
        {status_text}
    </div>
    """, unsafe_allow_html=True)
    
    # Session information
    st.markdown(f"""
    <div class="sidebar-info">
        <h4>Session Info</h4>
        <p><strong>Session ID:</strong><br>{st.session_state.session_id[:8]}...</p>
        <p><strong>Messages:</strong> {len(st.session_state.messages)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat controls
    st.subheader("💬 Chat Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat"):
            if clear_chat_session(st.session_state.session_id):
                st.session_state.messages = []
                st.success("Chat cleared!")
                st.rerun()
            else:
                st.error("Failed to clear chat")
    
    with col2:
        if st.button("🔄 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.success("New session started!")
            st.rerun()
    
    # Load history button
    if st.button("📥 Load History"):
        history = load_chat_history(st.session_state.session_id)
        if history:
            st.session_state.messages = history
            st.success(f"Loaded {len(history)} messages!")
            st.rerun()
        else:
            st.info("No history found")
    
    # Export chat
    if st.session_state.messages:
        chat_export = {
            "session_id": st.session_state.session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            label="📤 Export Chat",
            data=json.dumps(chat_export, indent=2),
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Main chat interface
st.header("💭 Chat Interface")

# Check backend status periodically
if st.session_state.backend_status == "unknown":
    st.session_state.backend_status = check_backend_health()

# Show connection warning if backend is offline
if st.session_state.backend_status != "online":
    st.error("⚠️ Backend is not available. Please start the backend server first.")
    st.code("python main.py", language="bash")
    st.stop()

# Chat display area
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info("👋 Welcome! Start a conversation by typing a message below.")
    else:
        # Display chat messages
        for i, message in enumerate(st.session_state.messages):
            if message['role'] == 'user':
                with st.chat_message("user", avatar="👤"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(message['content'])

# Chat input
with st.container():
    # Use columns for better layout
    input_col, send_col = st.columns([4, 1])
    
    with input_col:
        user_input = st.chat_input(
            "Type your message here...",
            key="chat_input",
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
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)
        
        # Show typing indicator
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                # Send to backend
                response = send_message_to_backend(user_input, st.session_state.session_id)
        
        # Handle response
        if "error" in response:
            st.error(f"❌ Error: {response['error']}")
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
            with st.chat_message("assistant", avatar="🤖"):
                st.write(response['response'])
        
        # Rerun to update the interface
        st.rerun()

# Footer with additional information
with st.expander("ℹ️ About this ChatBot"):
    st.markdown("""
    **Features:**
    - 🤖 Powered by Google Gemini 2.0 Flash
    - 🔄 Session persistence
    - 📊 Message history
    - 💾 Export/Import functionality
    - 🎨 Rich UI with real-time status
    
    **Technical Stack:**
    - Frontend: Streamlit
    - Backend: FastAPI + LangGraph
    - AI Model: Google Gemini via LangChain
    
    **Instructions:**
    1. Make sure the backend server is running (`python main.py`)
    2. Type your message in the chat input
    3. Use sidebar controls to manage your session
    """)

