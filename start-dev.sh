#!/bin/bash

# ZNPHI Measles Chatbot - Development Startup Script
# This script starts both the backend API and frontend dev server

echo "🚀 Starting ZNPHI Measles Chatbot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
echo "  - Installing Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "    Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
cd ..

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "  - Installing Node.js dependencies..."
    npm install
fi

echo ""
echo "✅ Dependencies installed!"
echo ""

# Start backend in background
echo "🔧 Starting Backend API (port 8000)..."
cd backend
source venv/bin/activate
python znphi_api.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "   Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend running (PID: $BACKEND_PID)"
else
    echo "❌ Backend failed to start. Check backend.log for errors."
    exit 1
fi

echo ""
echo "🎨 Starting Frontend Dev Server (port 5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ ZNPHI Measles Chatbot is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Frontend:      http://localhost:5173"
echo "🔧 Backend API:   http://localhost:8000"
echo "📚 API Docs:      http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: Already streaming above"
echo ""
echo "⏹️  To stop: Press Ctrl+C"
echo ""

# Trap Ctrl+C to clean up processes
trap "echo ''; echo '⏹️  Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Stopped!'; exit" INT

# Wait for processes
wait
