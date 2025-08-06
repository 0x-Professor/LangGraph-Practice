import streamlit as st
with st.chat_message("user"):
    st.text("Hello, how are you today?")
with st.chat_message("assistant"):
    st.text("I'm doing well, thank you! How can I assist you today?")
    
user_message = st.chat_input("Type your message here...", key="user_input")
if user_message:
    with st.chat_message("user"):
        st.text(user_message)