from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import asyncio
from langchain_core.messages import HumanMessage
from backend import chatbot, streaming_chatbot, ChatState
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

@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint that returns responses word by word"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        async def generate_stream():
            try:
                # Prepare the user message
                user_message = HumanMessage(content=request.message)
                
                # Get or create session state
                if session_id not in active_sessions:
                    initial_state = ChatState(messages=[])
                else:
                    initial_state = active_sessions[session_id].copy()
                
                # Add user message to state
                initial_state['messages'].append(user_message)
                
                # Send initial response with session info
                yield f"data: {json.dumps({'type': 'session_start', 'session_id': session_id})}\n\n"
                
                # Stream the response
                full_response = ""
                async for chunk in streaming_chatbot.astream(initial_state, config={"configurable": {"thread_id": session_id}}):
                    if 'chunk' in chunk and chunk.get('partial', False):
                        # Send each chunk as it arrives
                        chunk_data = {
                            'type': 'chunk',
                            'content': chunk['chunk'],
                            'session_id': session_id
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                        full_response += chunk['chunk']
                        
                        # Small delay for smooth streaming effect
                        await asyncio.sleep(0.01)
                    
                    elif not chunk.get('partial', True):
                        # Final message - store the complete state
                        active_sessions[session_id] = chunk
                        
                        # Send completion signal
                        completion_data = {
                            'type': 'complete',
                            'full_response': full_response,
                            'session_id': session_id
                        }
                        yield f"data: {json.dumps(completion_data)}\n\n"
                        break
                
            except Exception as e:
                error_data = {
                    'type': 'error',
                    'error': str(e),
                    'session_id': session_id
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing streaming chat: {str(e)}")

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
