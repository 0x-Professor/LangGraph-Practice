from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
from langchain_core.messages import HumanMessage
from backend import chatbot, ChatState
import uvicorn

app = FastAPI(title="ChatBot API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    content: str
    role: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str

# In-memory session storage (in production, use Redis or database)
active_sessions = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Prepare the user message
        user_message = HumanMessage(content=request.message)
        
        # Get or create session state
        if session_id not in active_sessions:
            initial_state = ChatState(messages=[])
        else:
            initial_state = active_sessions[session_id]
        
        # Add user message to state
        initial_state['messages'].append(user_message)
        
        # Invoke the chatbot
        result = chatbot.invoke(initial_state, config={"configurable": {"thread_id": session_id}})
        
        # Store updated state
        active_sessions[session_id] = result
        
        # Get the AI response (last message should be AI response)
        ai_response = result['messages'][-1].content if result['messages'] else "I'm sorry, I couldn't process your request."
        
        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    if session_id not in active_sessions:
        return {"messages": [], "status": "no_session_found"}
    
    messages = []
    for msg in active_sessions[session_id]['messages']:
        messages.append({
            "content": msg.content,
            "role": "user" if hasattr(msg, 'type') and msg.type == "human" else "assistant"
        })
    
    return {"messages": messages, "status": "success"}

@app.delete("/chat/session/{session_id}")
async def clear_session(session_id: str):
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"status": "session_cleared"}
    return {"status": "session_not_found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ChatBot API"}

def main():
    print("Hello from chatbot!")


if __name__ == "__main__":
    main()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
