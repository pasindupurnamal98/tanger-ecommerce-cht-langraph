import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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

# --- State Schema ---
class ChatState(BaseModel):
    user_message: str
    response: str = None
    intent: str = None

# --- LangGraph Nodes ---
def intent_node(state: ChatState):
    user_message = state.user_message
    prompt = f"""Classify the user's intent from this message: "{user_message}"
Options: order_query, spare_part_query, general
Respond with only the intent keyword."""
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    intent = response.choices[0].message.content.strip()
    return {"user_message": user_message, "intent": intent}

def db_node(state: ChatState):
    intent = state.intent
    user_message = state.user_message
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        if intent == "order_query":
            match = re.search(r'USR\d+', user_message)
            if match:
                user_id = match.group()
                cursor.execute("SELECT OrderID, Status, DeliveryDate FROM Orders WHERE UserID = ?", user_id)
                orders = cursor.fetchall()
                conn.close()
                if not orders:
                    return {"response": "No orders found for your account."}
                return {"response": "\n".join([f"Order {o.OrderID}: {o.Status}, Delivery: {o.DeliveryDate}" for o in orders])}
            else:
                conn.close()
                return {"response": "Please provide your user ID (e.g., USR001)."}
        elif intent == "spare_part_query":
            match = re.search(r'PRD\d+', user_message)
            if match:
                product_id = match.group()
                cursor.execute("SELECT PartName, Stock, Price FROM SpareParts WHERE ProductID = ?", product_id)
                parts = cursor.fetchall()
                conn.close()
                if not parts:
                    return {"response": "No spare parts found for this product."}
                return {"response": "\n".join([f"{p.PartName}: {p.Stock} in stock, Rs.{p.Price}" for p in parts])}
            else:
                conn.close()
                return {"response": "Please provide a product ID (e.g., PRD001)."}
        else:
            conn.close()
            return {"response": None}
    except Exception as e:
        return {"response": f"Database error: {e}"}

def llm_node(state: ChatState):
    user_message = state.user_message
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": user_message}]
    )
    return {"response": response.choices[0].message.content}

# --- LangGraph Workflow ---


graph = StateGraph(ChatState)
graph.add_node("intent", intent_node)
graph.add_node("db", db_node)
graph.add_node("llm", llm_node)
graph.add_edge("intent", "db")
graph.add_conditional_edges(
    "db",
    lambda state: "llm" if state.response is None else END
)
graph.add_edge("llm", END)
graph.set_entry_point("intent")
workflow = graph.compile()

# --- FastAPI Endpoint ---
class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        result = workflow.invoke({"user_message": request.user_message})
        return {"response": result["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("✅ Starting FastAPI server at http://127.0.0.1:8000 ...")
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)