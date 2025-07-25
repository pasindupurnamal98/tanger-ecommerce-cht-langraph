# Singer E-commerce AI Chatbot

Welcome to the **Singer E-commerce AI Chatbot** project!  
This is a full-stack, session-aware, context-driven virtual assistant for Singer’s online customers—powered by Azure OpenAI, LangGraph, FastAPI, SQL Server, and a beautiful Streamlit frontend.

---

## 🚀 Features

- **Conversational AI:** Natural, friendly, and context-aware chat powered by Azure OpenAI.
- **Session Management:** Remembers your conversation and context for a seamless experience.
- **Order Tracking:** Instantly check your order status, history, and delivery dates.
- **Spare Parts Lookup:** Find and order spare parts for your Singer products.
- **Warranty & Returns:** Get warranty info and return/exchange policies in seconds.
- **Quick Actions:** One-click buttons for common queries (track order, warranty, product info, etc.).
- **Store Locator:** Find Singer showrooms and service centers near you.
- **Personalized Responses:** The bot greets you by name and tailors answers to your needs.
- **Beautiful UI:** Modern, responsive Streamlit interface with chat bubbles, typing indicators, and more.
- **Admin Tools:** View, clear, and manage chat sessions for support and analytics.

---

## 🗂️ Project Structure
TANGER-ECOMMERCE-CHT/ │ ├── backend/ │ ├── .env # Backend environment variables (never commit this!) │ ├── backend.py # Main FastAPI app with LangGraph and OpenAI │ ├── requirements.txt # Backend dependencies │ ├── test_db.py # DB connection test script │ ├── data/ # (Optional) SQL/data files │ └── ... # Other backend scripts │ ├── frontend/ │ └── frontend.py # Streamlit app (UI) │ ├── .gitignore └── README.md

text


---

## ⚡ Quick Start

### 1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/tanger-ecommerce-cht.git
cd tanger-ecommerce-cht
2. Backend Setup
Bash

cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
Configure your .env with Azure OpenAI, SQL Server, etc.
3. Start the Backend
Bash

python backend.py
The API will run at http://127.0.0.1:8000
4. Frontend Setup
Bash

cd ../frontend
pip install streamlit requests
streamlit run frontend.py
The UI will open in your browser.
💡 Usage
Chat naturally: Ask about orders, spare parts, warranty, returns, or anything else.
Use quick actions: Click buttons for instant help.
Session memory: The bot remembers your context and IDs for multi-turn conversations.
Admin endpoints: View or clear sessions at /sessions and /session/{session_id}/history (backend).
🛠️ Tech Stack
Frontend: Streamlit (Python)
Backend: FastAPI, LangGraph, Azure OpenAI, pyodbc
Database: SQL Server (sample schema included)
Session Storage: In-memory (for demo; use Redis/DB for production)
Cloud AI: Azure OpenAI (GPT-4, GPT-4o, etc.)
🎨 Screenshots
Chat UI ScreenshotModern, branded chat interface with quick actions and session info.

🔒 Security & Best Practices
Never commit your .env or secrets!
Use a secure, persistent session store (like Redis) in production.
Add authentication for sensitive features if needed.
🌐 Deployment
Backend: Deploy on Azure, AWS, or any cloud supporting FastAPI.
Frontend: Deploy Streamlit on Streamlit Community Cloud, Azure Web Apps, or Docker.
Database: Use Azure SQL or your preferred managed SQL Server.
🤝 Contributing
Pull requests, issues, and feature suggestions are welcome!
Please open an issue or contact your-email@example.com.

📄 License
MIT License

🙏 Acknowledgements

OpenAI
LangGraph
Streamlit
FastAPI
Built with ❤️ by Pasindu Purnamal