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
    response: str = ""
    intent: str = ""

# --- LangGraph Nodes ---
def intent_node(state: ChatState):
    print(f"[LangGraph] Entering intent_node with user_message: {state.user_message}")
    user_message = state.user_message
    prompt = f"""Classify the user's intent from this message: "{user_message}"
Options: order_query, spare_part_query, general
Respond with only the intent keyword."""
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    intent = response.choices[0].message.content.strip()
    print(f"[LangGraph] Detected intent: {intent}")
    return {
        "user_message": user_message,
        "intent": intent,
        "response": state.response
    }

def db_node(state: ChatState):
    print(f"[LangGraph] Entering db_node with intent: {state.intent}, user_message: {state.user_message}")
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
                    print("[LangGraph] No orders found for user.")
                    return {
                        "response": "No orders found for your account.",
                        "intent": intent,
                        "user_message": user_message
                    }
                result = "\n".join([f"Order {o.OrderID}: {o.Status}, Delivery: {o.DeliveryDate}" for o in orders])
                print(f"[LangGraph] Orders found: {result}")
                return {
                    "response": result,
                    "intent": intent,
                    "user_message": user_message
                }
            else:
                conn.close()
                print("[LangGraph] No user ID found in message.")
                return {
                    "response": "Please provide your user ID (e.g., USR001).",
                    "intent": intent,
                    "user_message": user_message
                }
        elif intent == "spare_part_query":
            match = re.search(r'PRD\d+', user_message)
            if match:
                product_id = match.group()
                cursor.execute("SELECT PartName, Stock, Price FROM SpareParts WHERE ProductID = ?", product_id)
                parts = cursor.fetchall()
                conn.close()
                if not parts:
                    print("[LangGraph] No spare parts found for product.")
                    return {
                        "response": "No spare parts found for this product.",
                        "intent": intent,
                        "user_message": user_message
                    }
                result = "\n".join([f"{p.PartName}: {p.Stock} in stock, Rs.{p.Price}" for p in parts])
                print(f"[LangGraph] Spare parts found: {result}")
                return {
                    "response": result,
                    "intent": intent,
                    "user_message": user_message
                }
            else:
                conn.close()
                print("[LangGraph] No product ID found in message.")
                return {
                    "response": "Please provide a product ID (e.g., PRD001).",
                    "intent": intent,
                    "user_message": user_message
                }
        else:
            conn.close()
            print("[LangGraph] Intent not handled by db_node, passing to LLM.")
            return {
                "response": "",
                "intent": intent,
                "user_message": user_message
            }
    except Exception as e:
        print(f"[LangGraph] Database error: {e}")
        return {
            "response": f"Database error: {e}",
            "intent": intent,
            "user_message": user_message
        }

def llm_node(state: ChatState):
    print(f"[LangGraph] Entering llm_node with user_message: {state.user_message}")
    user_message = state.user_message
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": user_message}]
    )
    result = response.choices[0].message.content
    print(f"[LangGraph] LLM response: {result}")
    return {
        "response": result,
        "intent": state.intent,
        "user_message": user_message
    }

# --- LangGraph Workflow ---
graph = StateGraph(ChatState)
graph.add_node("intent", intent_node)
graph.add_node("db", db_node)
graph.add_node("llm", llm_node)
graph.add_edge("intent", "db")
graph.add_conditional_edges(
    "db",
    lambda state: "llm" if not state.response else END
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
        result = workflow.invoke({"user_message": request.user_message, "intent": "", "response": ""})
        print(f"[LangGraph] Final response: {result['response']}")
        return {"response": result["response"]}
    except Exception as e:
        print(f"[LangGraph] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("✅ Starting FastAPI server at http://127.0.0.1:8000 ...")
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)