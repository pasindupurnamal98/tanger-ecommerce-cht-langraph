import os
import re
import uuid
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import json

# Load environment variables
load_dotenv()

app = FastAPI()

# In-memory session store
session_store = {}

def process_chat_message(user_message: str, session_id: str) -> str:
    """Simple chat processing function"""
    print(f"Processing: '{user_message}' for session: {session_id}")
    
    user_message_lower = user_message.strip().lower()
    
    # Simple intent detection
    if user_message_lower in ["hi", "hello", "hey"]:
        return "Hello! Welcome to our customer service. Please provide your user ID (e.g., USR001) to continue."
    
    elif user_message_lower.startswith("usr"):
        user_id = user_message.upper()
        session_store[session_id] = user_id
        return f"Thank you! Your user ID {user_id} has been saved. How can I assist you today?"
    
    elif "order" in user_message_lower:
        user_id = session_store.get(session_id)
        if user_id:
            return f"Here are your orders for {user_id}: Order ORD001: Shipped, Delivery: 2025-01-30"
        else:
            return "Please provide your user ID first."
    
    else:
        return f"I understand you said: '{user_message}'. How can I help you further?"

@app.post("/chat")
async def chat_endpoint(request: dict):
    """Chat endpoint using plain dict instead of Pydantic"""
    try:
        # Extract data from request
        user_message = request.get("user_message", "")
        session_id = request.get("session_id") or str(uuid.uuid4())
        
        if not user_message:
            raise HTTPException(status_code=400, detail="user_message is required")
        
        # Process the message
        response = process_chat_message(user_message, session_id)
        
        # Return plain dict
        return {
            "response": response,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Simple Chatbot API is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("✅ Starting simple FastAPI server...")
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)