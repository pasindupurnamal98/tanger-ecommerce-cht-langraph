import os
import re
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import openai
import pyodbc
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# SQL Server connection string
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('SQL_SERVER')};"
    f"DATABASE={os.getenv('SQL_DATABASE')};"
    f"UID={os.getenv('SQL_USER')};"
    f"PWD={os.getenv('SQL_PASSWORD')}"
)

app = FastAPI()

# In-memory session store
session_store = {}

# --- State Schema using Pydantic BaseModel ---
class ChatState(BaseModel):
    session_id: str
    user_message: str
    response: str = ""  # Default to empty string
    intent: str = ""    # Default to empty string
    user_id: str = ""   # Default to empty string

# --- LangGraph Nodes ---
def intent_node(state: ChatState) -> ChatState:
    print(f"[LangGraph] Entering intent_node with user_message: '{state.user_message}'")
    user_message = state.user_message.strip().lower()
    print(f"[LangGraph] Processed message: '{user_message}'")
    
    # Check for greeting
    if user_message in ["hi", "hello", "hey"]:
        print("[LangGraph] Detected greeting")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent="greeting",
            user_id=state.user_id,
            response=state.response
        )
    
    # Check for user ID
    match = re.match(r'usr\d+', user_message, re.IGNORECASE)
    if match:
        print("[LangGraph] Detected user ID")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent="user_id",
            user_id=match.group().upper(),
            response=state.response
        )
    
    # Check for order-related keywords
    if any(word in user_message for word in ["order", "orders", "delivery", "status"]):
        print("[LangGraph] Detected order query")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent="order_query",
            user_id=state.user_id,
            response=state.response
        )
    
    # Check for spare parts query
    if any(word in user_message for word in ["spare", "part", "parts"]) or re.search(r'prd\d+', user_message, re.IGNORECASE):
        print("[LangGraph] Detected spare part query")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent="spare_part_query",
            user_id=state.user_id,
            response=state.response
        )
    
    # Default to general
    print("[LangGraph] Detected general intent")
    return ChatState(
        session_id=state.session_id,
        user_message=state.user_message,
        intent="general",
        user_id=state.user_id,
        response=state.response
    )

def greeting_node(state: ChatState) -> ChatState:
    print("[LangGraph] Entering greeting_node")
    return ChatState(
        session_id=state.session_id,
        user_message=state.user_message,
        intent=state.intent,
        user_id=state.user_id,
        response="Hello! Please provide your user ID (e.g., USR001) to continue."
    )

def user_id_node(state: ChatState) -> ChatState:
    print(f"[LangGraph] Entering user_id_node with user_id: {state.user_message.upper()}")
    user_id = state.user_message.upper()
    # Save user_id in session store
    session_store[state.session_id] = user_id
    return ChatState(
        session_id=state.session_id,
        user_message=state.user_message,
        intent=state.intent,
        user_id=user_id,
        response=f"Thank you! Your user ID {user_id} has been saved. How can I assist you today?"
    )

def db_node(state: ChatState) -> ChatState:
    print(f"[LangGraph] Entering db_node with intent: {state.intent}, user_id: {state.user_id}, user_message: {state.user_message}")
    intent = state.intent
    user_message = state.user_message
    user_id = state.user_id or session_store.get(state.session_id, "")
    
    try:
        if intent == "order_query":
            if user_id:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("SELECT OrderID, Status, DeliveryDate FROM Orders WHERE UserID = ?", user_id)
                orders = cursor.fetchall()
                conn.close()
                
                if not orders:
                    print("[LangGraph] No orders found for user.")
                    return ChatState(
                        session_id=state.session_id,
                        user_message=state.user_message,
                        intent=state.intent,
                        user_id=user_id,
                        response="No orders found for your account."
                    )
                
                result = "\n".join([f"Order {o.OrderID}: {o.Status}, Delivery: {o.DeliveryDate}" for o in orders])
                print(f"[LangGraph] Orders found: {result}")
                return ChatState(
                    session_id=state.session_id,
                    user_message=state.user_message,
                    intent=state.intent,
                    user_id=user_id,
                    response=result
                )
            else:
                print("[LangGraph] No user ID found in session.")
                return ChatState(
                    session_id=state.session_id,
                    user_message=state.user_message,
                    intent=state.intent,
                    user_id=user_id,
                    response="Please provide your user ID (e.g., USR001) first."
                )
                
        elif intent == "spare_part_query":
            match = re.search(r'PRD\d+', user_message, re.IGNORECASE)
            if match:
                product_id = match.group().upper()
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("SELECT PartName, Stock, Price FROM SpareParts WHERE ProductID = ?", product_id)
                parts = cursor.fetchall()
                conn.close()
                
                if not parts:
                    print("[LangGraph] No spare parts found for product.")
                    return ChatState(
                        session_id=state.session_id,
                        user_message=state.user_message,
                        intent=state.intent,
                        user_id=user_id,
                        response="No spare parts found for this product."
                    )
                
                result = "\n".join([f"{p.PartName}: {p.Stock} in stock, Rs.{p.Price}" for p in parts])
                print(f"[LangGraph] Spare parts found: {result}")
                return ChatState(
                    session_id=state.session_id,
                    user_message=state.user_message,
                    intent=state.intent,
                    user_id=user_id,
                    response=result
                )
            else:
                print("[LangGraph] No product ID found in message.")
                return ChatState(
                    session_id=state.session_id,
                    user_message=state.user_message,
                    intent=state.intent,
                    user_id=user_id,
                    response="Please provide a product ID (e.g., PRD001)."
                )
        else:
            # For any other intent, pass to LLM - use special marker
            print("[LangGraph] Intent not handled by db_node, passing to LLM.")
            return ChatState(
                session_id=state.session_id,
                user_message=state.user_message,
                intent=state.intent,
                user_id=user_id,
                response="__PASS_TO_LLM__"  # Special marker instead of empty string
            )
    except Exception as e:
        print(f"[LangGraph] Database error: {e}")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent=state.intent,
            user_id=user_id,
            response=f"Database error: {e}"
        )

def llm_node(state: ChatState) -> ChatState:
    print(f"[LangGraph] Entering llm_node with user_message: {state.user_message}")
    user_message = state.user_message
    
    try:
        response = openai.chat.completions.create(
            model=openai_deployment,
            messages=[{"role": "user", "content": user_message}]
        )
        result = response.choices[0].message.content
        print(f"[LangGraph] LLM response: {result}")
        
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent=state.intent,
            user_id=state.user_id,
            response=result
        )
    except Exception as e:
        print(f"[LangGraph] LLM error: {e}")
        return ChatState(
            session_id=state.session_id,
            user_message=state.user_message,
            intent=state.intent,
            user_id=state.user_id,
            response=f"I'm sorry, I encountered an error processing your request: {e}"
        )

# --- LangGraph Workflow ---
graph = StateGraph(ChatState)

# Add nodes
graph.add_node("intent", intent_node)
graph.add_node("greeting", greeting_node)
graph.add_node("user_id", user_id_node)
graph.add_node("db", db_node)
graph.add_node("llm", llm_node)

# Set entry point
graph.set_entry_point("intent")

# Add conditional edges from intent node
graph.add_conditional_edges(
    "intent",
    lambda state: state.intent,
    {
        "greeting": "greeting",
        "user_id": "user_id",
        "order_query": "db",
        "spare_part_query": "db",
        "general": "llm"
    }
)

# Add conditional edge from db node
graph.add_conditional_edges(
    "db",
    lambda state: "llm" if state.response == "__PASS_TO_LLM__" else END
)

# Add edges to END
graph.add_edge("greeting", END)
graph.add_edge("user_id", END)
graph.add_edge("llm", END)

# Compile the workflow
workflow = graph.compile()

# --- FastAPI Endpoint ---
class ChatRequest(BaseModel):
    user_message: str
    session_id: Optional[str] = None

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # Generate a new session_id if not provided
    session_id = request.session_id or str(uuid.uuid4())
    # Get user_id from session store if available
    user_id = session_store.get(session_id, "")
    
    try:
        initial_state = ChatState(
            session_id=session_id,
            user_message=request.user_message,
            user_id=user_id,
            response="",
            intent=""
        )
        
        result = workflow.invoke(initial_state)
        print(f"[LangGraph] Final response: {result.response}")
        return {"response": result.response, "session_id": session_id}
    except Exception as e:
        print(f"[LangGraph] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Customer Service Chatbot API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("✅ Starting FastAPI server at http://127.0.0.1:8000 ...")
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)