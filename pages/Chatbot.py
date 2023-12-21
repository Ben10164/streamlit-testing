import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import streamlit as st
import random
import time
import streamlit as st
import utils

utils.setup_page("Chatbot", icon="🤖")

st.title("Simple chat")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages_st" not in st.session_state:
    st.session_state.messages_st = []

# set up gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=st.session_state.messages)

# Display chat messages from history on app rerun
for message in st.session_state.messages_st:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # the issue that requires both messages and an st variant 
    # arrises from the fact that gemini expects prompt to be in
    # a set, whereas streamlit does not... 
    # you can remove the brackets around prompt, and then change 
    # the display portion to be messages, but it does some weird stuff
    # in the chat history (chat.history)
    st.session_state.messages_st.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"parts":{prompt},"role":"user"})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in chat.send_message(prompt, stream=True):
            full_response += (chunk.text)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages_st.append({"role": "assistant", "content": full_response})
    st.session_state.messages.append({"parts":{full_response},"role":"model"})
    print(chat.history)