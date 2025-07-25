import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

app = FastAPI()

# --- State Schema ---
class ChatState(BaseModel):
    user_message: str
    response: str = None

# --- LangGraph Nodes ---
def pass_through_node(state: ChatState):
    return {"user_message": state.user_message}

def llm_node(state: ChatState):
    user_message = state.user_message
    response = openai.chat.completions.create(
        model=openai_deployment,  # For Azure, this is your deployment name
        messages=[{"role": "user", "content": user_message}]
    )
    return {"response": response.choices[0].message.content}

# --- LangGraph Workflow ---
graph = StateGraph(ChatState)
graph.add_node("input", pass_through_node)
graph.add_node("llm", llm_node)
graph.add_edge("input", "llm")
graph.add_edge("llm", END)
graph.set_entry_point("input")
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
    uvicorn.run("simpl_backend:app", host="127.0.0.1", port=8000, reload=True)