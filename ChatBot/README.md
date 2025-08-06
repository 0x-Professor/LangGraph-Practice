# 🤖 AI ChatBot - Full Stack Application

A fully functional AI chatbot application built with FastAPI backend, Streamlit frontend, and powered by Google Gemini via LangGraph.

## ✨ Features

### Backend (FastAPI + LangGraph)
- 🧠 **Google Gemini 2.0 Flash Integration** - Advanced AI conversations
- 🔄 **Session Management** - Persistent chat sessions with memory
- 📊 **REST API** - Clean endpoints for chat operations
- 🚀 **Fast Response Times** - Optimized for real-time conversations
- 💾 **Memory Persistence** - Chat history maintained per session

### Frontend (Streamlit)
- 🎨 **Rich UI** - Beautiful, responsive chat interface
- 📱 **Real-time Status** - Backend connection monitoring
- 💬 **Interactive Chat** - Seamless conversation experience
- 📥 **Export/Import** - Save and load chat histories
- 🔧 **Session Controls** - Clear, restart, and manage sessions
- 📊 **Analytics** - Message counts and session information

## 🚀 Quick Start

### Option 1: One-Command Startup (Recommended)
```bash
cd ChatBot
python run_app.py
```

This will:
- Install all required dependencies
- Start the backend server (http://localhost:8000)
- Start the frontend UI (http://localhost:8501)

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Start Backend Server**
```bash
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Start Frontend (in a new terminal)**
```bash
streamlit run frontend.py --server.port 8501
```

## 🔧 Configuration

### Environment Setup
Make sure you have a valid Google API key set in `backend.py`. The current implementation includes the key directly, but for production, use environment variables:

```python
import os
api_key = os.getenv("GOOGLE_API_KEY", "your-default-key")
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
```

### Port Configuration
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8501`
- API Documentation: `http://localhost:8000/docs` (FastAPI auto-generated)

## 📡 API Endpoints

### Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id"
}
```

### Get Chat History
```http
GET /chat/history/{session_id}
```

### Clear Session
```http
DELETE /chat/session/{session_id}
```

### Health Check
```http
GET /health
```

## 🎯 Usage Instructions

1. **Start the Application**
   - Run `python run_app.py` or start servers manually
   - Wait for both servers to fully initialize

2. **Access the Frontend**
   - Open http://localhost:8501 in your browser
   - The interface will show connection status

3. **Start Chatting**
   - Type your message in the chat input
   - Press Enter to send
   - Watch the AI respond in real-time

4. **Use Advanced Features**
   - **Session Management**: Start new sessions or clear current ones
   - **Export Chat**: Download your conversation as JSON
   - **Load History**: Restore previous chat sessions
   - **Status Monitoring**: Check backend connectivity

## 🛠️ Technical Architecture

```
Frontend (Streamlit) ←→ Backend (FastAPI) ←→ LangGraph ←→ Google Gemini
        ↓                    ↓
   Session State         Memory Storage
```

### Components:
- **Frontend**: `frontend.py` - Streamlit-based UI
- **Backend**: `main.py` - FastAPI server with REST endpoints
- **AI Logic**: `backend.py` - LangGraph workflow with Gemini
- **Startup**: `run_app.py` - Automated setup and launch script

## 🔍 Troubleshooting

### Backend Not Connecting
- Check if port 8000 is available
- Verify Google API key is valid
- Look for error messages in terminal

### Frontend Issues
- Ensure backend is running first
- Check if port 8501 is available
- Refresh the browser page

### Dependencies Problems
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📦 Dependencies

### Core Framework
- `fastapi` - Backend API framework
- `streamlit` - Frontend UI framework
- `uvicorn` - ASGI server for FastAPI

### AI/ML Stack
- `langchain-google-genai` - Google Gemini integration
- `langgraph` - Workflow orchestration
- `langchain-core` - Core LangChain functionality

### Utilities
- `requests` - HTTP client for frontend-backend communication
- `pydantic` - Data validation and serialization

## 🚧 Development

### Adding New Features
1. **Backend**: Modify `main.py` for new endpoints
2. **Frontend**: Update `frontend.py` for UI changes
3. **AI Logic**: Extend `backend.py` for new capabilities

### Testing API
Use the auto-generated docs at http://localhost:8000/docs to test endpoints directly.

## 🔐 Security Notes

- The current setup is for development/demo purposes
- In production, use proper API key management
- Consider adding authentication and rate limiting
- Use HTTPS in production environments

## 📄 License

This project is part of the LangGraph-Practice repository and follows the same license terms.

---

**Happy Chatting! 🤖💬**