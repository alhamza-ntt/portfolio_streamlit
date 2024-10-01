import streamlit as st
import time
import urllib.request
import json
import requests


import streamlit as st

import requests

BASE_URL = "https://portfolionew.azurewebsites.net"


class BrowserSession:
    def __init__(self):
        self.session = requests.Session()

    def send_message(self, message):
        url = f"{BASE_URL}/send_message"
        data = {"content": message}
        response = self.session.post(url, json=data)
        return response.json()

    def get_history(self):
        url = f"{BASE_URL}/get_history"
        response = self.session.get(url)
        return response.json()

def clear_all_sessions():
    url = f"{BASE_URL}/clear_all_sessions"
    response = requests.post(url)
    return response.json()

def list_users():
    url = f"{BASE_URL}/list_users"
    response = requests.get(url)
    return response.json()

def get_user_history(user_id):
    url = f"{BASE_URL}/get_user_history/{user_id}"
    response = requests.get(url)
    return response.json()


# Initialize the ChatbotClient for each user session
if 'client' not in st.session_state:
    st.session_state.client = BrowserSession()  # Create a new client for each user

# Function to handle sending a message
def handle_send_message(message):
    if message:
        response = st.session_state.client.send_message(message)["response"]
        return response  # Return the response instead of writing it directly

st.title("Simple chat UI For Portfolio")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display assistant's response
    with st.chat_message("assistant"):
        response = handle_send_message(prompt)  # Get the response from the function
        st.markdown(response)  # Display the response in the assistant's chat
    st.session_state.messages.append({"role": "assistant", "content": response})