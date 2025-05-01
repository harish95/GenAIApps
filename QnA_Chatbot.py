import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Configure the Gemini client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize the model
model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')

# Setup Streamlit page
st.set_page_config(page_title="QnA Chatbot with Gemini", page_icon="🤖")
st.title("🤖 QnA Chatbot using Gemini API")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to generate response from Gemini
def get_gemini_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Display the chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# User input at the bottom
user_question = st.chat_input("Ask a question...")

if user_question:
    # Save user question
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    # Display user's message instantly
    with st.chat_message("user"):
        st.markdown(user_question)

    # Get Gemini's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            gemini_response = get_gemini_response(user_question)
            st.markdown(gemini_response)

    # Save Gemini's response
    st.session_state.chat_history.append({"role": "assistant", "content": gemini_response})
