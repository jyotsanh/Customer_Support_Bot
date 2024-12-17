import streamlit as st
import requests
import time

# Set page configuration
st.set_page_config(page_title="Hotel BOMO Chatbot", page_icon="🏨", layout="centered")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "bot", "content": "Welcome to Hotel BOMO! How can I help you today? I can assist with bookings, room inquiries, amenities, and more."}
    ]

# Function to send message to API
def send_message_to_api(message):
    try:
        response = requests.post(
            "http://localhost:8000/chat/", 
            params={
                "query": message, 
                "senderId": st.session_state.get('sender_id', '123abc')
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json().get('msg', 'Sorry, I could not process your request.')
    except requests.RequestException as e:
        st.error(f"API Error: {e}")
        return "I'm having trouble connecting to our server. Please try again later."

# Streamlit app layout
def main():
    st.title("🏨 Hotel BOMO Chatbot")

    # Generate a sender ID if not exists
    if 'sender_id' not in st.session_state:
        st.session_state.sender_id = 'abc'  # You might want to generate a unique ID

    # Chat history display
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Message input
    if user_input := st.chat_input("Ask about bookings, rooms, amenities..."):
        # Immediately render user's message
        st.chat_message("user").write(user_input)

        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user", 
            "content": user_input
        })

        # Get bot response
        with st.spinner("Thinking..."):
            bot_response = send_message_to_api(user_input)

        # Immediately render bot's message
        st.chat_message("assistant").write(bot_response)

        # Add bot response to chat history
        st.session_state.chat_history.append({
            "role": "bot", 
            "content": bot_response
        })

    # Optional context information
    with st.sidebar:
        st.header("Hotel BOMO")
        st.info("""
        🔹 24/7 Support
        🔹 Quick Bookings
        🔹 Instant Inquiries
        """)

if __name__ == "__main__":
    main()