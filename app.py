import streamlit as st
import time
from datetime import datetime
from chat_service import ChatService

# Page configuration
st.set_page_config(
    page_title="Thoughtful AI Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .agent-message {
        background: white;
        color: #333;
        padding: 0.75rem 1rem;
        border-radius: 18px;
        margin: 0.5rem 0;
        margin-right: 20%;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .message-time {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 0.25rem;
    }
    
    .welcome-message {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-width: 120px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    
    .stButton > button {
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = {
            "message": "Hello! I'm your Thoughtful AI support assistant. I can help you learn about our automation agents like EVA (Eligibility Verification), CAM (Claims Processing), and PHIL (Payment Posting). What would you like to know?",
            "is_from_agent": True,
            "timestamp": datetime.now(),
            "success": True
        }
        st.session_state.messages.append(welcome_msg)
    
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0

def format_timestamp(timestamp):
    """Format timestamp for display."""
    return timestamp.strftime("%H:%M")

def display_message(message_data):
    """Display a single message with proper styling."""
    message = message_data["message"]
    is_from_agent = message_data["is_from_agent"]
    timestamp = message_data["timestamp"]
    
    if is_from_agent:
        st.markdown(f"""
        <div class="agent-message">
            🤖 <strong>Thoughtful AI Assistant</strong><br>
            {message}
            <div class="message-time">{format_timestamp(timestamp)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="user-message">
            <strong>You</strong> 👤<br>
            {message}
            <div class="message-time">{format_timestamp(timestamp)}</div>
        </div>
        """, unsafe_allow_html=True)

def display_chat_history():
    """Display all messages in the chat history."""
    if st.session_state.messages:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message_data in st.session_state.messages:
            display_message(message_data)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-message">
            <h3>🤖 Welcome to Thoughtful AI Support</h3>
            <p>I'm here to help you learn about our healthcare automation agents.<br>
            Ask me about EVA, CAM, PHIL, or any of our services!</p>
        </div>
        """, unsafe_allow_html=True)

def handle_user_input(user_input):
    """Process user input and generate response."""
    if user_input and user_input.strip():
        # Add user message
        user_message = ChatService.create_user_message(user_input)
        st.session_state.messages.append(user_message)
        st.session_state.message_count += 1
        
        # Show typing indicator
        with st.spinner("🤖 Thinking..."):
            # Process input and get response
            agent_response = ChatService.process_user_input(user_input)
            st.session_state.messages.append(agent_response)
            st.session_state.message_count += 1
        
        # Rerun to update the display
        st.rerun()

def main():
    """Main application function."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Thoughtful AI Customer Support</h1>
        <p>Healthcare Automation Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-box">
            <h4>💬</h4>
            <p><strong>Messages</strong></p>
            <p>{}</p>
        </div>
        """.format(st.session_state.message_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-box">
            <h4>🤖</h4>
            <p><strong>Agents</strong></p>
            <p>EVA, CAM, PHIL</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-box">
            <h4>⚡</h4>
            <p><strong>Status</strong></p>
            <p>Online</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat display
    display_chat_history()
    
    # Input section
    st.markdown("### 💭 Ask me anything about Thoughtful AI")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your question here...",
            placeholder="Ask me about EVA, CAM, PHIL, or our services",
            max_chars=500,
            key="user_input"
        )
    
    with col2:
        send_button = st.button("Send 📤", type="primary")
    
    # Handle input
    if send_button or (user_input and st.session_state.get("last_input") != user_input):
        st.session_state.last_input = user_input
        handle_user_input(user_input)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("## 📋 Quick Info")
        st.markdown("""
        **Available Topics:**
        - 🔍 EVA (Eligibility Verification)
        - 📋 CAM (Claims Processing)  
        - 💰 PHIL (Payment Posting)
        - 🏥 General Thoughtful AI Services
        """)
        
        st.markdown("## 🎯 Sample Questions")
        sample_questions = [
            "What does EVA do?",
            "Tell me about CAM",
            "How does PHIL work?",
            "What are the benefits of using Thoughtful AI's agents?"
        ]
        
        for question in sample_questions:
            if st.button(question, key=f"sample_{question}"):
                handle_user_input(question)
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            # Add welcome message back
            welcome_msg = {
                "message": "Chat cleared! I'm here to help you learn about Thoughtful AI's automation agents. What would you like to know?",
                "is_from_agent": True,
                "timestamp": datetime.now(),
                "success": True
            }
            st.session_state.messages.append(welcome_msg)
            st.rerun()

if __name__ == "__main__":
    main()