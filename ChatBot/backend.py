import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import MemorySaver
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please create a .env file with your API key.")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    api_key=GOOGLE_API_KEY,
    temperature=0.5, 
    max_tokens=90000,
    streaming=True  # Enable streaming
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], Field(description="List of messages in the chat"), add_messages]
    
def chat_node(state: ChatState):
    if not state['messages']:
        state['messages'] = [HumanMessage(content="Hello, how can I assist you today?")]
    else:
        response = model.invoke(state['messages'])
        state['messages'].append(AIMessage(content=response.content))
    
    return {'messages': state['messages']}

async def stream_chat_response(messages):
    """Simple streaming function that directly streams from the model"""
    full_response = ""
    try:
        # Use the streaming capability of the model directly
        async for chunk in model.astream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                content = chunk.content
                full_response += content
                yield {
                    'partial': True,
                    'chunk': content,
                    'full_response': full_response
                }
        
        # Send final completion signal
        yield {
            'partial': False,
            'full_response': full_response
        }
        
    except Exception as e:
        yield {
            'error': True,
            'message': str(e)
        }

checkpointer = MemorySaver()
    
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer, name="ChatBot")
