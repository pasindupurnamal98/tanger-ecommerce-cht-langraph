# import streamlit as st
# import requests
# import json
# from datetime import datetime

# # Configure the page
# st.set_page_config(
#     page_title="Singer Assistant",
#     page_icon="🎵",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         text-align: center;
#         color: #1f4e79;
#         font-size: 2.5rem;
#         font-weight: bold;
#         margin-bottom: 1rem;
#     }
    
#     .chat-container {
#         max-height: 500px;
#         overflow-y: auto;
#         padding: 1rem;
#         border: 1px solid #e0e0e0;
#         border-radius: 10px;
#         background-color: #f8f9fa;
#         margin-bottom: 1rem;
#     }
    
#     .user-message {
#         background-color: #007bff;
#         color: white;
#         padding: 0.5rem 1rem;
#         border-radius: 15px;
#         margin: 0.5rem 0;
#         margin-left: 20%;
#         text-align: right;
#     }
    
#     .bot-message {
#         background-color: #e9ecef;
#         color: #333;
#         padding: 0.5rem 1rem;
#         border-radius: 15px;
#         margin: 0.5rem 0;
#         margin-right: 20%;
#     }
    
#     .quick-action-btn {
#         margin: 0.2rem;
#         padding: 0.5rem 1rem;
#         border: none;
#         border-radius: 20px;
#         background-color: #28a745;
#         color: white;
#         cursor: pointer;
#         font-size: 0.9rem;
#     }
    
#     .quick-action-btn:hover {
#         background-color: #218838;
#     }
    
#     .sidebar-section {
#         background-color: #f1f3f4;
#         padding: 1rem;
#         border-radius: 10px;
#         margin-bottom: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Backend API URL
# API_URL = "http://127.0.0.1:8000/chat"

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     # Add welcome message
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": "Hello! I'm Singer Assistant. How can I help you today? You can use the quick action buttons below or type your question directly.",
#         "timestamp": datetime.now().strftime("%H:%M")
#     })

# if "chat_input_key" not in st.session_state:
#     st.session_state.chat_input_key = 0

# # Helper function to send message to backend
# def send_message_to_backend(message):
#     try:
#         response = requests.post(
#             API_URL,
#             json={"user_message": message},
#             timeout=30
#         )
#         if response.status_code == 200:
#             return response.json()["response"]
#         else:
#             return f"Error: {response.status_code} - {response.text}"
#     except requests.exceptions.RequestException as e:
#         return f"Connection error: {str(e)}"

# # Helper function to add message to chat
# def add_message(role, content):
#     st.session_state.messages.append({
#         "role": role,
#         "content": content,
#         "timestamp": datetime.now().strftime("%H:%M")
#     })

# # Helper function to handle quick actions
# def handle_quick_action(action_text):
#     add_message("user", action_text)
#     with st.spinner("Singer Assistant is thinking..."):
#         response = send_message_to_backend(action_text)
#     add_message("assistant", response)
#     # Force rerun to update chat
#     st.rerun()

# # Main layout
# col1, col2 = st.columns([3, 1])

# with col1:
#     # Header
#     st.markdown('<h1 class="main-header">🎵 Singer Assistant</h1>', unsafe_allow_html=True)
    
#     # Quick Action Buttons
#     st.subheader("Quick Actions")
    
#     # Create buttons in rows
#     button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    
#     with button_col1:
#         if st.button("📦 Track My Order", key="track_order", use_container_width=True):
#             handle_quick_action("I want to track my order. Please help me check my order status.")
        
#         if st.button("🔧 Spare Parts", key="spare_parts", use_container_width=True):
#             handle_quick_action("I need information about spare parts for my Singer product.")
    
#     with button_col2:
#         if st.button("📋 Order Information", key="order_info", use_container_width=True):
#             handle_quick_action("I need information about my orders and order history.")
        
#         if st.button("↩️ Returns/Exchanges", key="returns", use_container_width=True):
#             handle_quick_action("I want to know about returns and exchanges policy.")
    
#     with button_col3:
#         if st.button("🛡️ Warranty Status", key="warranty", use_container_width=True):
#             handle_quick_action("I want to check the warranty status of my Singer product.")
        
#         if st.button("📍 Store Locations", key="stores", use_container_width=True):
#             handle_quick_action("I need to find Singer store locations near me.")
    
#     with button_col4:
#         if st.button("ℹ️ Product Information", key="product_info", use_container_width=True):
#             handle_quick_action("I need information about Singer products and their features.")
        
#         if st.button("🚚 Delivery Information", key="delivery", use_container_width=True):
#             handle_quick_action("I want to know about delivery options and shipping information.")
    
#     st.divider()
    
#     # Chat Display
#     st.subheader("Chat")
    
#     # Chat container
#     chat_container = st.container()
    
#     with chat_container:
#         # Display chat messages
#         for message in st.session_state.messages:
#             if message["role"] == "user":
#                 st.markdown(f"""
#                 <div class="user-message">
#                     <strong>You ({message["timestamp"]}):</strong><br>
#                     {message["content"]}
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="bot-message">
#                     <strong>Singer Assistant ({message["timestamp"]}):</strong><br>
#                     {message["content"]}
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     # Chat input
#     user_input = st.chat_input(
#         "Type your message here...", 
#         key=f"chat_input_{st.session_state.chat_input_key}"
#     )
    
#     if user_input:
#         # Add user message
#         add_message("user", user_input)
        
#         # Get bot response
#         with st.spinner("Singer Assistant is thinking..."):
#             response = send_message_to_backend(user_input)
        
#         # Add bot response
#         add_message("assistant", response)
        
#         # Increment key to clear input
#         st.session_state.chat_input_key += 1
        
#         # Rerun to update chat
#         st.rerun()

# with col2:
#     # Sidebar with additional information
#     st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#     st.subheader("💡 Tips")
#     st.markdown("""
#     **For Order Tracking:**
#     - Provide your User ID (e.g., USR001)
    
#     **For Spare Parts:**
#     - Mention your Product ID (e.g., PRD001)
    
#     **Quick Help:**
#     - Use the buttons above for common queries
#     - Type naturally - I understand conversational language!
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#     st.subheader("📞 Contact Info")
#     st.markdown("""
#     **Customer Service:**
#     - Phone: 1-800-SINGER
#     - Email: support@singer.com
#     - Hours: 9 AM - 6 PM (Mon-Fri)
#     """)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#     st.subheader("🔄 Actions")
#     if st.button("Clear Chat History", use_container_width=True):
#         st.session_state.messages = []
#         # Add welcome message back
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": "Hello! I'm Singer Assistant. How can I help you today? You can use the quick action buttons below or type your question directly.",
#             "timestamp": datetime.now().strftime("%H:%M")
#         })
#         st.rerun()
    
#     if st.button("Refresh Connection", use_container_width=True):
#         st.success("Connection refreshed!")
#     st.markdown('</div>', unsafe_allow_html=True)

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: #666;'>Singer Assistant - Powered by AI | Always here to help!</div>", 
#     unsafe_allow_html=True
# )

# # Auto-scroll to bottom of chat (JavaScript)
# st.markdown("""
# <script>
#     var chatContainer = document.querySelector('.chat-container');
#     if (chatContainer) {
#         chatContainer.scrollTop = chatContainer.scrollHeight;
#     }
# </script>
# """, unsafe_allow_html=True)

###frontend session management
import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Singer Assistant",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1.5rem;
        border: 2px solid #e3f2fd;
        border-radius: 20px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 5px 25px;
        margin: 1rem 0;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 25px 5px;
        margin: 1rem 0;
        margin-right: 15%;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        animation: slideInLeft 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .quick-action-container {
        background: linear-gradient(145deg, #ffffff 0%, #f0f8ff 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid #e3f2fd;
    }
    
    .stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 15px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        margin-bottom: 0.5rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .sidebar-section {
        background: linear-gradient(145deg, #ffffff 0%, #f0f8ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e3f2fd;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online {
        background-color: #4CAF50;
    }
    
    .status-offline {
        background-color: #f44336;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .session-info {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #333;
        font-size: 0.85rem;
    }
    
    .message-timestamp {
        font-size: 0.75rem;
        opacity: 0.8;
        margin-bottom: 0.5rem;
    }
    
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        margin: 1rem 0;
        margin-right: 15%;
        padding: 1rem 1.5rem;
        background: #f0f0f0;
        border-radius: 25px 25px 25px 5px;
        color: #666;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        background-color: #667eea;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .dot:nth-child(2) { animation-delay: 0.2s; }
    .dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    .stChatInput > div > div > div > div {
        border-radius: 25px;
        border: 2px solid #e3f2fd;
        background: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URLs
API_BASE_URL = "http://127.0.0.1:8000"
CHAT_URL = f"{API_BASE_URL}/chat"
SESSION_HISTORY_URL = f"{API_BASE_URL}/session"
SESSIONS_URL = f"{API_BASE_URL}/sessions"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "🎵 Hello! I'm Singer Assistant, your AI-powered customer service companion. I'm here to help you with orders, spare parts, warranties, and much more! How can I assist you today?",
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if "chat_input_key" not in st.session_state:
    st.session_state.chat_input_key = 0

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

if "connection_status" not in st.session_state:
    st.session_state.connection_status = "offline"

# Helper function to check backend connection
def check_backend_connection():
    try:
        response = requests.get(f"{API_BASE_URL}/sessions", timeout=5)
        return response.status_code == 200
    except:
        return False

# Helper function to send message to backend
def send_message_to_backend(message, session_id):
    try:
        response = requests.post(
            CHAT_URL,
            json={
                "user_message": message,
                "session_id": session_id
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return data["response"], data.get("session_id", session_id)
        else:
            return f"❌ Error: {response.status_code} - {response.text}", session_id
    except requests.exceptions.RequestException as e:
        return f"🔌 Connection error: {str(e)}", session_id

# Helper function to get session history
def get_session_history(session_id):
    try:
        response = requests.get(f"{SESSION_HISTORY_URL}/{session_id}/history", timeout=10)
        if response.status_code == 200:
            return response.json()["history"]
        return []
    except:
        return []

# Helper function to clear session
def clear_backend_session(session_id):
    try:
        response = requests.delete(f"{SESSION_HISTORY_URL}/{session_id}", timeout=10)
        return response.status_code == 200
    except:
        return False

# Helper function to add message to chat
def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

# Helper function to show typing indicator
def show_typing_indicator():
    st.session_state.is_typing = True

def hide_typing_indicator():
    st.session_state.is_typing = False

# Helper function to handle quick actions
def handle_quick_action(action_text):
    add_message("user", action_text)
    show_typing_indicator()
    st.rerun()

# Check connection status
st.session_state.connection_status = "online" if check_backend_connection() else "offline"

# Main layout
col1, col2 = st.columns([3, 1])

with col1:
    # Header with connection status
    st.markdown('<h1 class="main-header">🎵 Singer Assistant</h1>', unsafe_allow_html=True)
    
    # Connection status indicator
    status_class = "status-online" if st.session_state.connection_status == "online" else "status-offline"
    status_text = "🟢 Connected" if st.session_state.connection_status == "online" else "🔴 Disconnected"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="status-indicator {status_class}"></span>
        <strong>{status_text}</strong> | Session: {st.session_state.session_id[:8]}...
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown('<div class="quick-action-container">', unsafe_allow_html=True)
    st.subheader("🚀 Quick Actions")
    
    # Create buttons in rows
    button_col1, button_col2, button_col3, button_col4 = st.columns(4)
    
    with button_col1:
        if st.button("📦 Track Order", key="track_order", use_container_width=True):
            handle_quick_action("I want to track my order. Please help me check my order status.")
        
        if st.button("🔧 Spare Parts", key="spare_parts", use_container_width=True):
            handle_quick_action("I need information about spare parts for my Singer product.")
    
    with button_col2:
        if st.button("📋 Order History", key="order_info", use_container_width=True):
            handle_quick_action("I need information about my orders and order history.")
        
        if st.button("↩️ Returns", key="returns", use_container_width=True):
            handle_quick_action("I want to know about returns and exchanges policy.")
    
    with button_col3:
        if st.button("🛡️ Warranty", key="warranty", use_container_width=True):
            handle_quick_action("I want to check the warranty status of my Singer product.")
        
        if st.button("📍 Store Locator", key="stores", use_container_width=True):
            handle_quick_action("I need to find Singer store locations near me.")
    
    with button_col4:
        if st.button("ℹ️ Product Info", key="product_info", use_container_width=True):
            handle_quick_action("I need information about Singer products and their features.")
        
        if st.button("🚚 Delivery", key="delivery", use_container_width=True):
            handle_quick_action("I want to know about delivery options and shipping information.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat Display
    st.subheader("💬 Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat messages
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="message-timestamp">You - {message["timestamp"]}</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <div class="message-timestamp">Singer Assistant - {message["timestamp"]}</div>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Show typing indicator if bot is typing
        if st.session_state.is_typing:
            st.markdown("""
            <div class="typing-indicator">
                Singer Assistant is typing
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle pending quick action
    if st.session_state.is_typing and len(st.session_state.messages) > 0:
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "user":
            # Get bot response
            response, new_session_id = send_message_to_backend(
                last_message["content"], 
                st.session_state.session_id
            )
            
            # Update session ID if changed
            st.session_state.session_id = new_session_id
            
            # Add bot response
            add_message("assistant", response)
            hide_typing_indicator()
            st.rerun()
    
    # Chat input
    user_input = st.chat_input(
        "💭 Type your message here...", 
        key=f"chat_input_{st.session_state.chat_input_key}",
        disabled=st.session_state.connection_status == "offline"
    )
    
    if user_input and st.session_state.connection_status == "online":
        # Add user message
        add_message("user", user_input)
        
        # Show typing indicator and get bot response
        show_typing_indicator()
        response, new_session_id = send_message_to_backend(
            user_input, 
            st.session_state.session_id
        )
        
        # Update session ID if changed
        st.session_state.session_id = new_session_id
        
        # Add bot response
        add_message("assistant", response)
        hide_typing_indicator()
        
        # Increment key to clear input
        st.session_state.chat_input_key += 1
        
        # Rerun to update chat
        st.rerun()

with col2:
    # Session Information
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("🔗 Session Info")
    st.markdown(f"""
    <div class="session-info">
        <strong>Session ID:</strong><br>
        {st.session_state.session_id[:16]}...<br>
        <strong>Messages:</strong> {len(st.session_state.messages)}<br>
        <strong>Status:</strong> {st.session_state.connection_status.title()}
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tips section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("💡 Smart Tips")
    st.markdown("""
    **🎯 For Better Results:**
    
    **Order Tracking:**
    - Mention your User ID (USR001, USR002, etc.)
    - Ask about "my orders" naturally
    
    **Spare Parts:**
    - Provide Product ID (PRD001, PRD002, etc.)
    - Describe your product model
    
    **💬 Conversation Tips:**
    - I remember our conversation context
    - Ask follow-up questions naturally
    - Use the quick action buttons for common queries
    
    **🔄 Try saying:**
    - "Check my other orders"
    - "What about spare parts?"
    - "Tell me more about that"
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats section
    if st.session_state.connection_status == "online":
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("📊 Quick Stats")
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{len(st.session_state.messages)}</h3>
                <p>Messages</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.markdown(f"""
            <div class="metric-container">
                <h3>{user_messages}</h3>
                <p>Your Queries</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Info
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("📞 Need Human Help?")
    st.markdown("""
    **Customer Service:**
    - ☎️ Phone: 1-800-SINGER
    - ✉️ Email: support@singer.com
    - 🕒 Hours: 9 AM - 6 PM (Mon-Fri)
    - 🌐 Website: singer.com/support
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Actions section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader("🔄 Session Actions")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            # Clear backend session
            if st.session_state.connection_status == "online":
                clear_backend_session(st.session_state.session_id)
            
            # Clear frontend messages
            st.session_state.messages = []
            # Add welcome message back
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎵 Hello! I'm Singer Assistant, your AI-powered customer service companion. I'm here to help you with orders, spare parts, warranties, and much more! How can I assist you today?",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.success("✅ Chat cleared!")
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 New Session", use_container_width=True):
            # Create new session
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": "🎵 Hello! I'm Singer Assistant, your AI-powered customer service companion. I'm here to help you with orders, spare parts, warranties, and much more! How can I assist you today?",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            st.success("✅ New session started!")
            st.rerun()
    
    if st.button("🔌 Test Connection", use_container_width=True):
        if check_backend_connection():
            st.success("✅ Connection successful!")
            st.session_state.connection_status = "online"
        else:
            st.error("❌ Connection failed!")
            st.session_state.connection_status = "offline"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>Singer Assistant v2.0</strong> - Powered by AI & LangGraph<br>
    Session: {st.session_state.session_id[:8]}... | Status: {st.session_state.connection_status.title()}<br>
    Always here to help! 🎵
</div>
""", unsafe_allow_html=True)

# Auto-refresh connection status every 30 seconds
if 'last_connection_check' not in st.session_state:
    st.session_state.last_connection_check = datetime.now()

current_time = datetime.now()
if (current_time - st.session_state.last_connection_check).seconds > 30:
    st.session_state.connection_status = "online" if check_backend_connection() else "offline"
    st.session_state.last_connection_check = current_time
