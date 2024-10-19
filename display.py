import tempfile
import streamlit as st
import requests
import json
from bot import chat_bot

# Define your Flask API URL
API_URL = 'http://192.168.29.152:5050/knowledge_graph'

# Login/Register state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_register_page():
    # Login/Register state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    st.title("InfoElixir: Login / Register")
    
    choice = st.radio("Select an option:", ["Login", "Register"])
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if choice == "Register":
        if st.button("Register"):
            # Handle user registration (you'd need a backend for this)
            st.success("Registration successful! You can now log in.")
    
    if choice == "Login":
        if st.button("Login"):
            # Handle user authentication (you'd need a backend for this)
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
    # Redirect to the knowledge graph operations page
            st.rerun()

def knowledge_graph_operations():
    st.title("InfoElixir: Knowledge Graph Operations")

    # Upload file
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "doc","wav","mp3"])
    file_path = None
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            file_path = temp_file.name  # Get the absolute path of the temp file
            st.success("File uploaded and saved temporarily!")
            st.write(f"File saved at: {file_path}")

    # Input for subject and topic
    name = st.text_input("Name")
    subject = st.text_input("Subject")
    topic = st.text_area("Topic")

    if st.button("Add Subject"):
        if name and subject and file_path:
            data = {
                'name': name,
                'subject': subject,
                'topic': {
                    "title":topic,
                    "file_path":file_path
                }
            }
            response = requests.post(f"{API_URL}/add_subject", json=data)
            if response.status_code == 201:
                st.success("Subject added successfully!")
            else:
                st.error("Failed to add subject.")

    if st.button("Create Graph"):
        if name and subject and file_path:
            data = {
                'name': name,
                'subject': subject,
                'topic': {
                    "title":topic,
                    "file_path":file_path
                }
            }
            response = requests.post(f"{API_URL}/create", json=data)
            if response.status_code == 201:
                st.success("Graph created successfully!")
            else:
                st.error("Failed to create graph.")

    if st.button("Update Topics"):
        if name and subject and file_path:
            data = {
                'name': name,
                'subject': subject,
                'topic': {
                    "title":topic,
                    "file_path":file_path
                }
            }
            response = requests.put(f"{API_URL}/update_topics", json=data)
            if response.status_code == 200:
                st.success("Topics updated successfully!")
            else:
                st.error("Failed to update topics.")

    if st.button("Delete Subject"):
        if name and subject and file_path:
            data = {
                'name': name,
                'subject': subject,
            }
            response = requests.delete(f"{API_URL}/delete_subject", json=data)
            if response.status_code == 200:
                st.success("Subject deleted successfully!")
            else:
                st.error("Failed to delete subject.")

def chatbot_page():
    chat_bot()

# Main app logic
def main():
    # Sidebar for navigation
    st.sidebar.title("InfoElixir")
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        options = st.sidebar.radio("Go to", ["Knowledge Graph Operations","Chatbot"])
    else:
        options = st.sidebar.radio("Go to", ["Login / Register"])
    
    if options == "Login / Register":
        login_register_page()
    elif options == "Knowledge Graph Operations":
        if st.session_state.get('logged_in', False):
            knowledge_graph_operations()
        else:
            st.warning("Please log in first.")
    elif options == "Chatbot":
        if st.session_state.get('logged_in', False):
            chatbot_page()
        else:
            st.warning("Please log in first.")

if __name__ == '__main__':
    main()

