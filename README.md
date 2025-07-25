
# 🎵 Singer E-commerce AI Chatbot

Welcome to the **Singer E-commerce AI Chatbot** project!  
A full-stack, session-aware, context-driven virtual assistant for Singer’s online customers—powered by Azure OpenAI, LangGraph, FastAPI, SQL Server, and a beautiful Streamlit frontend.

---

## 🚀 Features

- **Conversational AI:** Friendly, context-aware chat powered by Azure OpenAI.
- **Session Management:** Remembers your conversation and context.
- **Order Tracking:** Instantly check your order status and history.
- **Spare Parts Lookup:** Find and order spare parts for your Singer products.
- **Warranty & Returns:** Get warranty info and return/exchange policies.
- **Quick Actions:** One-click buttons for common queries.
- **Store Locator:** Find Singer showrooms and service centers.
- **Personalized Responses:** The bot greets you by name and tailors answers.
- **Beautiful UI:** Modern Streamlit interface with chat bubbles, typing indicators, and more.
- **Admin Tools:** View, clear, and manage chat sessions.

---

## 📁 Project Structure
TANGER-ECOMMERCE-CHT/ ├── backend/ │ ├── .env # Backend environment variables (never commit this!) │ ├── backend.py # Main FastAPI app with LangGraph and OpenAI │ ├── requirements.txt # Backend dependencies │ ├── test_db.py # DB connection test script │ ├── data/ # (Optional) SQL/data files │ └── ... # Other backend scripts ├── frontend/ │ └── frontend.py # Streamlit app (UI) ├── .gitignore └── README.md


---

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


📄 License
MIT License

🙏 Acknowledgements

OpenAI
LangGraph
Streamlit
FastAPI
Built with ❤️ by [Pasindu]