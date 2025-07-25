import streamlit as st
import requests
import json
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Singer Assistant",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
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
        background-color: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: 20%;
        text-align: right;
    }
    
    .bot-message {
        background-color: #e9ecef;
        color: #333;
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
    
    .quick-action-btn {
        margin: 0.2rem;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 20px;
        background-color: #28a745;
        color: white;
        cursor: pointer;
        font-size: 0.9rem;
    }
    
    .quick-action-btn:hover {
        background-color: #218838;
    }
    
    .sidebar-section {
        background-color: #f1f3f4;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://127.0.0.1:8000/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm Singer Assistant. How can I help you today? You can use the quick action buttons below or type your question directly.",
        "timestamp": datetime.now().strftime("%H:%M")
    })

if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0

# Helper function to send message to backend
def send_message_to_backend(message):
    try:
        response = requests.post(
            API_URL,
            json={"user_message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"

# Helper function to add message to chat
def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# Helper function to handle quick actions
def handle_quick_action(action_text):
    add_message("user", action_text)
    with st.spinner("Singer Assistant is thinking..."):
        response = send_message_to_backend(action_text)
    add_message("assistant", response)
    # Force rerun to update chat
    st.rerun()

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    # Header
    st.markdown('<h1 class="main-header">🎵 Singer Assistant</h1>', unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.subheader("Quick Actions")
    
    # Create buttons in rows
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    
    with button_col1:
        if st.button("📦 Track My Order", key="track_order", use_container_width=True):
            handle_quick_action("I want to track my order. Please help me check my order status.")
        
        if st.button("🔧 Spare Parts", key="spare_parts", use_container_width=True):
            handle_quick_action("I need information about spare parts for my Singer product.")
    
    with button_col2:
        if st.button("📋 Order Information", key="order_info", use_container_width=True):
            handle_quick_action("I need information about my orders and order history.")
        
        if st.button("↩️ Returns/Exchanges", key="returns", use_container_width=True):
            handle_quick_action("I want to know about returns and exchanges policy.")
    
    with button_col3:
        if st.button("🛡️ Warranty Status", key="warranty", use_container_width=True):
            handle_quick_action("I want to check the warranty status of my Singer product.")
        
        if st.button("📍 Store Locations", key="stores", use_container_width=True):
            handle_quick_action("I need to find Singer store locations near me.")
    
    with button_col4:
        if st.button("ℹ️ Product Information", key="product_info", use_container_width=True):
            handle_quick_action("I need information about Singer products and their features.")
        
        if st.button("🚚 Delivery Information", key="delivery", use_container_width=True):
            handle_quick_action("I want to know about delivery options and shipping information.")
    
    st.divider()
    
    # Chat Display
    st.subheader("Chat")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You ({message["timestamp"]}):</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>Singer Assistant ({message["timestamp"]}):</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input(
        "Type your message here...", 
        key=f"chat_input_{st.session_state.chat_input_key}"
    )
    
    if user_input:
        # Add user message
        add_message("user", user_input)
        
        # Get bot response
        with st.spinner("Singer Assistant is thinking..."):
            response = send_message_to_backend(user_input)
        
        # Add bot response
        add_message("assistant", response)
        
        # Increment key to clear input
        st.session_state.chat_input_key += 1
        
        # Rerun to update chat
        st.rerun()

with col2:
    # Sidebar with additional information
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("💡 Tips")
    st.markdown("""
    **For Order Tracking:**
    - Provide your User ID (e.g., USR001)
    
    **For Spare Parts:**
    - Mention your Product ID (e.g., PRD001)
    
    **Quick Help:**
    - Use the buttons above for common queries
    - Type naturally - I understand conversational language!
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("📞 Contact Info")
    st.markdown("""
    **Customer Service:**
    - Phone: 1-800-SINGER
    - Email: support@singer.com
    - Hours: 9 AM - 6 PM (Mon-Fri)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("🔄 Actions")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        # Add welcome message back
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm Singer Assistant. How can I help you today? You can use the quick action buttons below or type your question directly.",
            "timestamp": datetime.now().strftime("%H:%M")
        })
        st.rerun()
    
    if st.button("Refresh Connection", use_container_width=True):
        st.success("Connection refreshed!")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Singer Assistant - Powered by AI | Always here to help!</div>", 
    unsafe_allow_html=True
)

# Auto-scroll to bottom of chat (JavaScript)
st.markdown("""
<script>
    var chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)