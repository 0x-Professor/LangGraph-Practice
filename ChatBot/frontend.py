import streamlit as st
import requests
import json
from datetime import datetime
import time
import uuid
import asyncio
from typing import Generator

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
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #f0f0f0, #e8e8e8);
        border-radius: 15px;
        font-style: italic;
        color: #666;
        animation: pulse 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        100% { opacity: 1.0; }
    }
    
    /* Typewriter effect styling */
    .typewriter-text {
        line-height: 1.6;
        word-wrap: break-word;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Blinking cursor for typewriter effect */
    .typewriter-cursor {
        display: inline-block;
        width: 2px;
        height: 1.2em;
        background-color: #4285f4;
        animation: blink 1s infinite;
        margin-left: 1px;
        vertical-align: text-bottom;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    /* Status indicators for typewriter */
    .typewriter-status {
        font-size: 0.8rem;
        color: #888;
        font-style: italic;
        padding: 0.25rem 0;
    }
    
    /* Enhanced message styling */
    .message-content {
        line-height: 1.6;
        word-wrap: break-word;
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
if 'streaming_enabled' not in st.session_state:
    st.session_state.streaming_enabled = True
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False
if 'typewriter_speed' not in st.session_state:
    st.session_state.typewriter_speed = 0.03  # Seconds between characters

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
    """Send message to backend API (non-streaming)"""
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

def stream_message_from_backend(message, session_id) -> Generator[dict, None, None]:
    """Stream message from backend API using Server-Sent Events"""
    try:
        payload = {
            "message": message,
            "session_id": session_id
        }
        
        with requests.post(
            f"{API_BASE_URL}/chat/stream",
            json=payload,
            stream=True,
            timeout=60,
            headers={'Accept': 'text/event-stream'}
        ) as response:
            
            if response.status_code != 200:
                yield {"error": f"Backend error: {response.status_code}"}
                return
            
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        yield data
                    except json.JSONDecodeError:
                        continue
                        
    except requests.exceptions.RequestException as e:
        yield {"error": f"Connection error: {str(e)}"}

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
    <div class="app-subtitle">Powered by Google Gemini with Streaming</div>
</div>
""", unsafe_allow_html=True)

# Status check
if st.session_state.backend_status == "unknown":
    st.session_state.backend_status = check_backend_health()

# Status indicator
if st.session_state.backend_status == "online":
    streaming_status = "🟢 Streaming" if st.session_state.streaming_enabled else "🔵 Standard"
    st.markdown(f"""
    <div class="status-bar status-online">
        ● Connected - {streaming_status}
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
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.is_streaming = False
        st.rerun()

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        if clear_chat_session(st.session_state.session_id):
            st.session_state.messages = []
            st.session_state.is_streaming = False
            st.rerun()

with col3:
    streaming_label = "📡 Stream ON" if st.session_state.streaming_enabled else "📡 Stream OFF"
    if st.button(streaming_label, use_container_width=True):
        st.session_state.streaming_enabled = not st.session_state.streaming_enabled
        st.rerun()

with col4:
    if st.button("📊 Status", use_container_width=True):
        st.session_state.backend_status = check_backend_health()
        st.rerun()

with col5:
    if st.session_state.messages:
        chat_export = {
            "session_id": st.session_state.session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages,
            "streaming_enabled": st.session_state.streaming_enabled
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
    streaming_info = "with real-time streaming" if st.session_state.streaming_enabled else "in standard mode"
    st.markdown(f"""
    <div class="welcome-message">
        Welcome! Start a conversation by typing a message below.<br>
        <small>Currently running {streaming_info}</small>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display chat messages
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
    disabled=st.session_state.backend_status != "online" or st.session_state.is_streaming
)

# Process user input
if user_input and not st.session_state.is_streaming:
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
    
    # Set streaming state
    st.session_state.is_streaming = True
    
    # Create placeholder for assistant response
    with st.chat_message("assistant"):
        if st.session_state.streaming_enabled:
            # Streaming mode with typewriter effect
            response_placeholder = st.empty()
            status_placeholder = st.empty()
            
            # Show initial typing indicator
            status_placeholder.markdown('<div class="typing-indicator">AI is thinking...</div>', unsafe_allow_html=True)
            
            full_response = ""
            displayed_text = ""
            error_occurred = False
            
            try:
                # Collect all chunks first
                all_chunks = []
                for chunk_data in stream_message_from_backend(user_input, st.session_state.session_id):
                    if chunk_data.get('type') == 'chunk':
                        all_chunks.append(chunk_data.get('content', ''))
                    elif chunk_data.get('type') == 'complete':
                        full_response = chunk_data.get('full_response', ''.join(all_chunks))
                        break
                    elif chunk_data.get('type') == 'error':
                        error_occurred = True
                        st.error(f"Error: {chunk_data.get('error', 'Unknown error')}")
                        break
                
                if not error_occurred and full_response:
                    # Clear typing indicator
                    status_placeholder.empty()
                    
                    # Display typewriter effect
                    status_placeholder.markdown('<div class="typewriter-status">Typing response...</div>', unsafe_allow_html=True)
                    
                    # Typewriter effect - display character by character
                    for i in range(len(full_response) + 1):
                        displayed_text = full_response[:i]
                        if i < len(full_response):
                            # Show cursor while typing
                            response_placeholder.markdown(
                                f'<div class="typewriter-text">{displayed_text}<span class="typewriter-cursor"></span></div>',
                                unsafe_allow_html=True
                            )
                        else:
                            # Final display without cursor
                            response_placeholder.markdown(
                                f'<div class="typewriter-text">{displayed_text}</div>',
                                unsafe_allow_html=True
                            )
                        
                        # Delay between characters
                        time.sleep(st.session_state.typewriter_speed)
                    
                    # Remove status
                    status_placeholder.empty()
                    
                    # Add bot response to chat history
                    bot_message = {
                        'role': 'assistant',
                        'content': full_response,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.session_state.messages.append(bot_message)
                else:
                    # Remove user message if there was an error
                    if error_occurred:
                        st.session_state.messages.pop()
                    
            except Exception as e:
                st.error(f"Streaming error: {str(e)}")
                status_placeholder.empty()
                # Remove user message on error
                st.session_state.messages.pop()
        
        else:
            # Standard mode (non-streaming) with typewriter effect
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
                
                # Display bot response with typewriter effect
                response_text = response['response']
                response_placeholder = st.empty()
                
                for i in range(len(response_text) + 1):
                    displayed_text = response_text[:i]
                    if i < len(response_text):
                        response_placeholder.markdown(
                            f'<div class="typewriter-text">{displayed_text}<span class="typewriter-cursor"></span></div>',
                            unsafe_allow_html=True
                        )
                    else:
                        response_placeholder.markdown(
                            f'<div class="typewriter-text">{displayed_text}</div>',
                            unsafe_allow_html=True
                        )
                    time.sleep(st.session_state.typewriter_speed)
    
    # Reset streaming state
    st.session_state.is_streaming = False
    
    # Rerun to update the interface
    st.rerun()

# Simple footer with streaming info
streaming_mode = "Streaming Mode" if st.session_state.streaming_enabled else "Standard Mode"
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #888; font-size: 0.8rem;'>"
    f"Session: {st.session_state.session_id[:8]}... | "
    f"Messages: {len(st.session_state.messages)} | "
    f"Mode: {streaming_mode}"
    f"</div>", 
    unsafe_allow_html=True
)

