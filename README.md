#  Singer E-commerce AI Chatbot

## Project Overview

The **Singer E-commerce AI Chatbot** is an intelligent, interactive assistant designed to revolutionize the online shopping experience for Singer customers. Leveraging the power of AI and a robust technical stack, this chatbot provides instant, 24/7 support for a wide range of customer needs, aiming to enhance customer satisfaction and streamline support operations.

### Problem Solved

Traditional customer support often involves long wait times, limited availability, and repetitive queries that consume valuable human agent time. This chatbot addresses these challenges by:

*   **Providing Instant Support:** Customers can get immediate answers to their questions, regardless of time or day.
*   **Automating Routine Tasks:** Common inquiries (e.g., product information, order status) are handled automatically, freeing up human agents for more complex issues.
*   **Enhancing User Experience:** A conversational and context-aware interface makes interactions natural and efficient.
*   **Increasing Sales Opportunities:** Proactive engagement and easy access to product/promotion information can drive sales.

## 🚀 Key Features

*   **Conversational AI:** Powered by Azure OpenAI and LangGraph, the chatbot offers friendly, context-aware, and human-like interactions.
*   **Session Management:** Maintains conversation context across multiple turns, providing a seamless user experience.
*   **Product Information:** Instantly provides details, specifications, and pricing for a wide range of products including electrical appliances, furniture, and kitchen items.
*   **Order Tracking:** Allows customers to check the real-time status and delivery details of their orders.
*   **Warranty Management:** Enables users to verify warranty periods and coverage for their purchased products.
*   **Spare Parts Lookup:** Helps customers find and order specific spare parts for their Singer products.
*   **Store Information:** Provides locations, contact details, and operating hours for Singer showrooms and service centers.
*   **Returns & Exchanges:** Guides users through the process of returning or exchanging products.
*   **Promotions & Offers:** Informs customers about current deals, discounts, and special offers.
*   **Personalized Responses:** The chatbot can greet users by name and tailor responses based on past interactions or user profiles.
*   **User-Friendly Interface:** A modern Streamlit interface with intuitive chat bubbles, typing indicators, and quick action buttons.
*   **Admin Tools:** Backend endpoints for viewing, clearing, and managing chat sessions.

## 🛠️ Technical Overview

This project is built with a modern, scalable, and secure technology stack:

*   **Frontend:**
    *   **Streamlit:** Used for building the interactive and user-friendly chat interface. Streamlit's simplicity allows for rapid development and deployment of data applications.

*   **Backend:**
    *   **LangGraph:** Manages complex conversational flows, state, and multi-step interactions, ensuring the chatbot can handle intricate user queries.
    *   **Azure OpenAI:** Provides advanced natural language understanding (NLU) and natural language generation (NLG) capabilities, enabling human-like responses and intelligent conversation.
    *   **FastAPI:** A high-performance web framework for building the backend APIs that connect the chatbot to the database and other services.
    *   **pyodbc:** Python driver for connecting to SQL Server databases.

*   **Database:**
    *   **SQL Server:** Stores all essential business data, including product catalogs, customer orders, warranty information, spare parts inventory, and store details. A sample schema is included for easy setup.

*   **Session Storage:**
    *   **In-memory (for demo):** For demonstration purposes, session state is managed in-memory. For production environments, a persistent store like Redis or a dedicated database is recommended.

*   **Cloud AI:**
    *   **Azure OpenAI:** Leverages powerful models like GPT-4, GPT-4o, etc., for advanced AI capabilities.
      
## 🖼️ Demo Snapshot

![Singer Assistant Demo](/img.png)

*Modern, branded chat interface with quick actions and session info.*

## 📁 Project Structure

```
TANGER-ECOMMERCE-CHT/
├── backend/
│   ├── .env                 # Environment variables (sensitive, not committed)
│   ├── backend.py           # Main FastAPI application with LangGraph and OpenAI integration
│   ├── requirements.txt     # Python dependencies for the backend
│   ├── simpl_backend.py     # (Optional) Simplified backend script for testing/development
│   └── test_db.py           # Script to test database connectivity
├── data/
│   ├── 10_smp.pdf           # Sample document (e.g., for RAG or information extraction)
│   ├── setup_database.sql   # SQL script to create database schema and insert sample data
│   ├── singer_categories.txt# List of product categories extracted from Singer website
│   └── updated.sql          # (Optional) Updated SQL scripts
├── frontend/
│   └── frontend.py          # Streamlit application for the user interface
├── Singer_Assistant.mp4     # Video demonstration of the chatbot
├── .gitignore               # Specifies intentionally untracked files to ignore
└── README.md                # Project README file
```

## 🚀 Getting Started

Follow these steps to set up and run the Singer E-commerce AI Chatbot locally.

### Prerequisites

*   Python 3.8+
*   SQL Server instance (local or cloud-based)
*   Azure OpenAI Service subscription with deployed models (GPT-4, GPT-4o, etc.)

### 1. Clone the Repository

```bash
git clone https://github.com/pasindupurnamal98/tanger-ecommerce-cht-langraph.git
cd tanger-ecommerce-cht-langraph
```

### 2. Database Setup

1.  **Create Database:** Create a new database in your SQL Server instance (e.g., `SingerEcommerceDB`).
2.  **Run SQL Script:** Execute the `data/setup_database.sql` script against your newly created database. This script will create all necessary tables and populate them with sample data.

### 3. Backend Setup

1.  **Navigate to Backend Directory:**
    ```bash
    cd backend
    ```
2.  **Create Environment File:** Create a `.env` file in the `backend/` directory with your database connection string and Azure OpenAI credentials. Replace placeholders with your actual values:
    ```
    DATABASE_CONNECTION_STRING="DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server_name;DATABASE=SingerEcommerceDB;UID=your_username;PWD=your_password"
    AZURE_OPENAI_API_KEY="your_azure_openai_api_key"
    AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
    AZURE_OPENAI_API_VERSION="2024-02-15-preview" # Or your specific API version
    AZURE_OPENAI_DEPLOYMENT_NAME="your_deployment_name" # e.g., gpt-4o-deployment
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Backend Server:**
    ```bash
    uvicorn backend:app --reload --port 8000
    ```
    The backend API will be accessible at `http://localhost:8000`.

### 4. Frontend Setup

1.  **Open a New Terminal and Navigate to Frontend Directory:**
    ```bash
    cd frontend
    ```
2.  **Run Streamlit Application:**
    ```bash
    streamlit run frontend.py
    ```
    The Streamlit chatbot interface will open in your web browser, usually at `http://localhost:8501`.

    

## 💡 Usage

*   **Chat Naturally:** Interact with the chatbot by asking questions about products, orders, warranties, spare parts, store locations, or any other customer service inquiry.
*   **Use Quick Actions:** Click on the quick reply buttons for common queries to get instant responses.
*   **Session Memory:** The chatbot remembers your conversation context, allowing for multi-turn interactions.
*   **Admin Endpoints (Backend):**
    *   View active sessions: `http://localhost:8000/sessions`
    *   View session history: `http://localhost:8000/session/{session_id}/history`
    *   Clear sessions: (Implement as needed, typically via a POST request to a specific endpoint)

## 🔒 Security & Best Practices

*   **Environment Variables:** Never commit sensitive information like API keys or database credentials directly into your repository. Use `.env` files and ensure they are listed in `.gitignore`.
*   **Persistent Session Storage:** For production deployments, replace in-memory session management with a robust, persistent store like Redis or a dedicated database table.
*   **Authentication:** Implement proper authentication and authorization mechanisms for sensitive features or admin functionalities.

## 🌐 Deployment

*   **Backend:** The FastAPI backend can be deployed on cloud platforms such as Azure App Service, AWS EC2, Google Cloud Run, or any environment supporting Python web applications.
*   **Frontend:** The Streamlit application can be deployed on Streamlit Community Cloud, Azure Web Apps, or containerized using Docker.
*   **Database:** Utilize managed SQL Server services like Azure SQL Database for production-grade reliability and scalability.

## 🤝 Contributing

Contributions, issues, and feature suggestions are highly welcome! Feel free to fork the repository, create pull requests, or open issues to discuss improvements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

*   [OpenAI](https://openai.com/)
*   [LangGraph](https://langchain.github.io/langgraph/)
*   [Streamlit](https://streamlit.io/)
*   [FastAPI](https://fastapi.tiangolo.com/)

Built with ❤️ by [Pasindu]


