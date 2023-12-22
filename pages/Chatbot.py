import time

import google.generativeai as genai
import streamlit as st

import utils

utils.setup_page("Chatbot", icon="🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

# set up gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=st.session_state.messages)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        message["role"], avatar=("🤖" if message["role"] == "model" else "🧑‍💻")
    ):
        st.markdown(message["parts"])

if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"parts": user_input, "role": "user"})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    with st.chat_message("model", avatar="🤖"):
        response_typing = st.empty()
        response = ""
        for chunk in chat.send_message(user_input, stream=True):
            for character in chunk.text:
                time.sleep(0.015)
                response += character
                response_typing.markdown(response + "▌")
        response_typing.markdown(response)
    st.session_state.messages.append({"parts": response, "role": "model"})
