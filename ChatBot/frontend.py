import streamlit as st
message_history = st.session_state.get('messages', [])
if not message_history:
    message_history = [
        {'role': 'user', 'content': "Hello, how are you today?"},
        {'role': 'assistant', 'content': "I'm doing well, thank you! How can I assist you today?"}
    ]
    st.session_state['messages'] = message_history
else:
    message_history = st.session_state['messages']
for message in message_history:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_message = st.chat_input("Type your message here...", key="user_input")
if user_message:
    with st.chat_message("user"):
        st.text(user_message)
        
