from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import MemorySaver
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    api_key="AIzaSyAG7aFAc0BT2Fjz2l93Q7xsniYtGbIDAjE", 
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

async def chat_node_stream(state: ChatState):
    """Streaming version of chat_node"""
    if not state['messages']:
        yield {'messages': [HumanMessage(content="Hello, how can I assist you today?")]}
        return
    
    # Stream the response
    full_response = ""
    async for chunk in model.astream(state['messages']):
        if hasattr(chunk, 'content') and chunk.content:
            full_response += chunk.content
            # Create a temporary state update with partial response
            temp_messages = state['messages'] + [AIMessage(content=full_response)]
            yield {
                'messages': temp_messages,
                'partial': True,
                'chunk': chunk.content
            }
    
    # Final complete response
    state['messages'].append(AIMessage(content=full_response))
    yield {'messages': state['messages'], 'partial': False}

checkpointer = MemorySaver()
    
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)
chatbot = graph.compile(checkpointer=checkpointer, name="ChatBot")

# Create streaming version
streaming_graph = StateGraph(ChatState)
streaming_graph.add_node('chat_node_stream', chat_node_stream)
streaming_graph.add_edge(START, 'chat_node_stream')
streaming_graph.add_edge('chat_node_stream', END)
streaming_chatbot = streaming_graph.compile(checkpointer=checkpointer, name="StreamingChatBot")
