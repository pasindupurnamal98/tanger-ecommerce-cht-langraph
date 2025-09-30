###session management
import os
import re
import uuid
from typing import Dict, List
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

# Session storage (in production, use Redis or database)
sessions: Dict[str, List[Dict]] = {}

# --- Session Management Functions ---
def get_or_create_session(session_id: str = None) -> str:
    """Get existing session or create new one"""
    if not session_id:
        session_id = str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = []
    return session_id

def add_to_session(session_id: str, role: str, content: str):
    """Add message to session history"""
    if session_id in sessions:
        sessions[session_id].append({"role": role, "content": content})
        # Keep only last 20 messages to prevent memory issues
        if len(sessions[session_id]) > 20:
            sessions[session_id] = sessions[session_id][-20:]

def get_session_context(session_id: str) -> str:
    """Get conversation context from session"""
    if session_id not in sessions:
        return ""
    
    context_messages = []
    for msg in sessions[session_id][-10:]:  # Last 10 messages for context
        context_messages.append(f"{msg['role']}: {msg['content']}")
    
    return "\n".join(context_messages)

def extract_user_id_from_context(text: str) -> str:
    """Extract user ID from text (current message or context)"""
    match = re.search(r'USR\d+', text, re.IGNORECASE)
    return match.group() if match else None

def extract_product_id_from_context(text: str) -> str:
    """Extract product ID from text (current message or context)"""
    match = re.search(r'PRD\d+', text, re.IGNORECASE)
    return match.group() if match else None

# --- Updated State Schema ---
class ChatState(BaseModel):
    user_message: str
    response: str = ""
    intent: str = ""
    session_context: str = ""
    session_id: str = ""
    extracted_user_id: str = ""
    extracted_product_id: str = ""

# --- Updated LangGraph Nodes ---
def intent_node(state: ChatState):
    print(f"[LangGraph] Entering intent_node with user_message: {state.user_message}")
    user_message = state.user_message
    session_context = state.session_context
    
    # Create enhanced prompt with context
    prompt = f"""
    Previous conversation context:
    {session_context}
    
    Current user message: "{user_message}"
    
    Classify the user's intent from this message considering the conversation context.
    
    Rules:
    - If user asks about "orders", "my orders", "other orders", "order status" and a user ID (USR###) was mentioned in context, classify as "order_query"
    - If user asks about "spare parts", "parts", "components" and a product ID (PRD###) was mentioned in context, classify as "spare_part_query"
    - If user provides a user ID (USR###) and asks about orders, classify as "order_query"
    - If user provides a product ID (PRD###) and asks about parts, classify as "spare_part_query"
    - For general questions, greetings, or other topics, classify as "general"
    
    Options: order_query, spare_part_query, general
    Respond with only the intent keyword.
    """
    
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    intent = response.choices[0].message.content.strip().lower()
    print(f"[LangGraph] Detected intent: {intent}")
    
    # Extract IDs from current message and context
    combined_text = f"{session_context} {user_message}"
    extracted_user_id = extract_user_id_from_context(combined_text)
    extracted_product_id = extract_product_id_from_context(combined_text)
    
    return {
        "user_message": user_message,
        "intent": intent,
        "response": state.response,
        "session_context": session_context,
        "session_id": state.session_id,
        "extracted_user_id": extracted_user_id or "",
        "extracted_product_id": extracted_product_id or ""
    }

def db_node(state: ChatState):
    print(f"[LangGraph] Entering db_node with intent: {state.intent}")
    intent = state.intent
    user_message = state.user_message
    session_context = state.session_context
    extracted_user_id = state.extracted_user_id
    extracted_product_id = state.extracted_product_id
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        if intent == "order_query":
            if extracted_user_id:
                print(f"[LangGraph] Using extracted user ID: {extracted_user_id}")
                cursor.execute("""
                    SELECT O.OrderID, O.Status, O.DeliveryDate, U.Name
                    FROM Orders O
                    JOIN Users U ON O.UserID = U.UserID
                    WHERE O.UserID = ?
                """, extracted_user_id)
                orders = cursor.fetchall()
                conn.close()
                
                if not orders:
                    print("[LangGraph] No orders found for user.")
                    return {
                        "response": f"No orders found for user ID {extracted_user_id}.",
                        "intent": intent,
                        "user_message": user_message,
                        "session_context": session_context,
                        "session_id": state.session_id,
                        "extracted_user_id": extracted_user_id,
                        "extracted_product_id": extracted_product_id
                    }
                
                user_name = orders[0].Name
                result = f"Customer: {user_name}\n" + "\n".join(
                    [f"Order {o.OrderID}: {o.Status}, Delivery: {o.DeliveryDate}" for o in orders]
                )
                print(f"[LangGraph] Orders found: {result}")
                return {
                    "response": result,
                    "intent": intent,
                    "user_message": user_message,
                    "session_context": session_context,
                    "session_id": state.session_id,
                    "extracted_user_id": extracted_user_id,
                    "extracted_product_id": extracted_product_id
                }
            else:
                conn.close()
                print("[LangGraph] No user ID found in message or context.")
                return {
                    "response": "Please provide your user ID (e.g., USR001) to check your orders.",
                    "intent": intent,
                    "user_message": user_message,
                    "session_context": session_context,
                    "session_id": state.session_id,
                    "extracted_user_id": extracted_user_id,
                    "extracted_product_id": extracted_product_id
                }
                
        elif intent == "spare_part_query":
            if extracted_product_id:
                print(f"[LangGraph] Using extracted product ID: {extracted_product_id}")
                cursor.execute("""
                    SELECT P.Name AS ProductName, S.PartName, S.Stock, S.Price
                    FROM SpareParts S
                    JOIN Products P ON S.ProductID = P.ProductID
                    WHERE S.ProductID = ?
                """, extracted_product_id)
                parts = cursor.fetchall()
                conn.close()
                
                if not parts:
                    print("[LangGraph] No spare parts found for product.")
                    return {
                        "response": f"No spare parts found for product ID {extracted_product_id}.",
                        "intent": intent,
                        "user_message": user_message,
                        "session_context": session_context,
                        "session_id": state.session_id,
                        "extracted_user_id": extracted_user_id,
                        "extracted_product_id": extracted_product_id
                    }
                
                product_name = parts[0].ProductName
                result = f"Product: {product_name}\n" + "\n".join(
                    [f"{p.PartName}: {p.Stock} in stock, Rs.{p.Price}" for p in parts]
                )
                print(f"[LangGraph] Spare parts found: {result}")
                return {
                    "response": result,
                    "intent": intent,
                    "user_message": user_message,
                    "session_context": session_context,
                    "session_id": state.session_id,
                    "extracted_user_id": extracted_user_id,
                    "extracted_product_id": extracted_product_id
                }
            else:
                conn.close()
                print("[LangGraph] No product ID found in message or context.")
                return {
                    "response": "Please provide a product ID (e.g., PRD001) to check spare parts.",
                    "intent": intent,
                    "user_message": user_message,
                    "session_context": session_context,
                    "session_id": state.session_id,
                    "extracted_user_id": extracted_user_id,
                    "extracted_product_id": extracted_product_id
                }
        else:
            conn.close()
            print("[LangGraph] Intent not handled by db_node, passing to LLM.")
            return {
                "response": "",
                "intent": intent,
                "user_message": user_message,
                "session_context": session_context,
                "session_id": state.session_id,
                "extracted_user_id": extracted_user_id,
                "extracted_product_id": extracted_product_id
            }
            
    except Exception as e:
        print(f"[LangGraph] Database error: {e}")
        return {
            "response": f"Database error: {e}",
            "intent": intent,
            "user_message": user_message,
            "session_context": session_context,
            "session_id": state.session_id,
            "extracted_user_id": extracted_user_id,
            "extracted_product_id": extracted_product_id
        }

def friendly_llm_node(state: ChatState):
    print(f"[LangGraph] Entering friendly_llm_node with db result: {state.response}")
    
    # Enhanced prompt with context awareness
    prompt = f"""
    You are Singer Assistant, a helpful virtual assistant for Singer e-commerce customers.
    
    Previous conversation context:
    {state.session_context}
    
    Current database result to rephrase: {state.response}
    User's original message: {state.user_message}
    
    Rephrase the database result in a friendly, helpful way for the customer. 
    Consider the conversation context to make your response more natural and personalized.
    If this is a follow-up question, acknowledge the continuation of the conversation.
    
    Never mention OpenAI or that you are an AI language model. Always respond as Singer Assistant.
    """
    
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    print(f"[LangGraph] Friendly LLM response: {result}")
    
    return {
        "response": result,
        "intent": state.intent,
        "user_message": state.user_message,
        "session_context": state.session_context,
        "session_id": state.session_id,
        "extracted_user_id": state.extracted_user_id,
        "extracted_product_id": state.extracted_product_id
    }

def llm_node(state: ChatState):
    print(f"[LangGraph] Entering llm_node with user_message: {state.user_message}")
    user_message = state.user_message
    session_context = state.session_context
    
    # Enhanced system message with context
    system_message = {
        "role": "system",
        "content": (
            "You are Singer Assistant, a helpful virtual assistant for Singer e-commerce customers. "
            "You help with orders, spare parts, warranties, returns, product information, store locations, and delivery information. "
            "Never mention OpenAI or that you are an AI language model. "
            "Always answer as Singer Assistant. "
            "Use the conversation context to provide more personalized and relevant responses."
        )
    }
    
    # Include context in the conversation
    messages = [system_message]
    if session_context:
        messages.append({
            "role": "user", 
            "content": f"Previous conversation context:\n{session_context}\n\nCurrent question: {user_message}"
        })
    else:
        messages.append({"role": "user", "content": user_message})
    
    response = openai.chat.completions.create(
        model=openai_deployment,
        messages=messages
    )
    result = response.choices[0].message.content
    print(f"[LangGraph] LLM response: {result}")
    
    return {
        "response": result,
        "intent": state.intent,
        "user_message": user_message,
        "session_context": session_context,
        "session_id": state.session_id,
        "extracted_user_id": state.extracted_user_id,
        "extracted_product_id": state.extracted_product_id
    }

# --- LangGraph Workflow ---
graph = StateGraph(ChatState)
graph.add_node("intent", intent_node)
graph.add_node("db", db_node)
graph.add_node("friendly_llm", friendly_llm_node)
graph.add_node("llm", llm_node)

graph.add_edge("intent", "db")
graph.add_conditional_edges(
    "db",
    lambda state: "llm" if not state.response else "friendly_llm"
)
graph.add_edge("friendly_llm", END)
graph.add_edge("llm", END)
graph.set_entry_point("intent")

workflow = graph.compile()

# --- Updated FastAPI Models ---
class ChatRequest(BaseModel):
    user_message: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# --- Updated FastAPI Endpoint ---
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Get or create session
        session_id = get_or_create_session(request.session_id)
        print(f"[Session] Using session ID: {session_id}")
        
        # Get conversation context
        session_context = get_session_context(session_id)
        print(f"[Session] Context length: {len(session_context)} characters")
        
        # Add user message to session
        add_to_session(session_id, "user", request.user_message)
        
        # Create initial state with context
        initial_state = {
            "user_message": request.user_message,
            "intent": "",
            "response": "",
            "session_context": session_context,
            "session_id": session_id,
            "extracted_user_id": "",
            "extracted_product_id": ""
        }
        
        # Run the workflow
        result = workflow.invoke(initial_state)
        
        # Add assistant response to session
        add_to_session(session_id, "assistant", result["response"])
        
        print(f"[LangGraph] Final response: {result['response']}")
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id
        )
        
    except Exception as e:
        print(f"[LangGraph] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Additional Endpoints for Session Management ---
@app.get("/session/{session_id}/history")
def get_session_history(session_id: str):
    """Get conversation history for a session"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"session_id": session_id, "history": sessions[session_id]}

@app.delete("/session/{session_id}")
def clear_session(session_id: str):
    """Clear a specific session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/sessions")
def list_sessions():
    """List all active sessions"""
    return {
        "active_sessions": list(sessions.keys()),
        "total_sessions": len(sessions)
    }

if __name__ == "__main__":
    import uvicorn
    print("✅ Starting FastAPI server with session management at http://127.0.0.1:8000 ...")
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)