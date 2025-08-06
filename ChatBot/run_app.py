#!/usr/bin/env python3
"""
Startup script for the ChatBot application
Runs both backend and frontend servers
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    backend_cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    return subprocess.Popen(backend_cmd)

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting frontend server...")
    frontend_cmd = [sys.executable, "-m", "streamlit", "run", "frontend.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
    return subprocess.Popen(frontend_cmd)

def main():
    print("🤖 ChatBot Application Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("backend.py").exists():
        print("❌ Please run this script from the ChatBot directory")
        sys.exit(1)
    
    # Install requirements
    install_requirements()
    
    print("\n🔧 Starting services...")
    
    try:
        # Start backend
        backend_process = start_backend()
        time.sleep(3)  # Give backend time to start
        
        # Start frontend
        frontend_process = start_frontend()
        
        print("\n✅ Both servers are starting up!")
        print("📍 Backend API: http://localhost:8000")
        print("🌐 Frontend UI: http://localhost:8501")
        print("\n💡 Tips:")
        print("- Wait a few seconds for both servers to fully start")
        print("- The frontend will show connection status")
        print("- Press Ctrl+C to stop both servers")
        
        # Wait for both processes
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            backend_process.terminate()
            frontend_process.terminate()
            
            # Wait for graceful shutdown
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
            
            print("✅ Servers stopped successfully!")
    
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()