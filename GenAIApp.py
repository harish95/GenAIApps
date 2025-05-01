import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

# Streamlit app UI
st.set_page_config(page_title="Gemini Chat (Streaming)", page_icon="✨")
st.title("💬 Chat with Gemini (Streaming Response)")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input from user
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user's message instantly
    with st.chat_message("user"):
        st.markdown(user_input)

    # Placeholder for Gemini's response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Stream the response from Gemini
            stream = model.generate_content(user_input, stream=True)

            for chunk in stream:
                if chunk.candidates:
                    part = chunk.candidates[0].content.parts[0].text
                    full_response += part
                    response_placeholder.markdown(full_response)
        
            # Save assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")
