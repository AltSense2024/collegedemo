import streamlit as st
import requests
import os

# Configure page
st.set_page_config(
    page_title="AltSense Assistant",
    page_icon="🎓",
    layout="wide"
)

# API Configuration - using environment variables for security
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
HF_SPACE_URL = st.secrets.get("HF_SPACE_URL", "https://your-private-space.hf.space")

def call_private_ai_api(message, chat_history=[]):
    """Call your private Hugging Face Space API securely"""
    try:
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "data": [message, chat_history]
        }
        
        response = requests.post(
            f"{HF_SPACE_URL}/gradio_api/call/generate_answer",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("data", ["Sorry, no response received"])[0]
        else:
            return "Sorry, I'm having trouble connecting to the AI service."
            
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return "Sorry, there was an error processing your request."

# Main Streamlit Interface
def main():
    st.title("🎓 M.M.E.S Women's Arts and Science College")
    st.subheader("AI Assistant - Ask anything about our college!")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Chat interface
    with st.container():
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask about courses, admissions, facilities..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Extract chat history for context
                    chat_history = [(msg["content"], "") for msg in st.session_state.messages[:-1] 
                                  if msg["role"] == "user"]
                    
                    # Call private AI API
                    response = call_private_ai_api(prompt, chat_history)
                    st.markdown(response)
            
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with college info
    with st.sidebar:
        st.markdown("### 🏫 About M.M.E.S College")
        st.markdown("""
        - **Founded:** 1918
        - **Location:** Maliankara, Kerala
        - **Courses:** UG & PG programs
        - **Focus:** Women's education
        """)
        
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()
