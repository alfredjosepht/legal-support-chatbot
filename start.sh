#!/bin/bash
# Quick start script for Legal Support Chatbot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Starting Legal Support Chatbot..."
echo ""

# Kill any existing processes
echo "Cleaning up old processes..."
pkill -f "uvicorn app:app" || true
pkill -f "npm start" || true
sleep 2

# Start backend in background
echo "Starting backend on port 8000..."
cd "$SCRIPT_DIR"
python -m uvicorn app:app --reload --port 8000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "  ✓ Backend PID: $BACKEND_PID"

# Start frontend in background
echo "Starting frontend on port 3001..."
cd "$SCRIPT_DIR/frontend"
PORT=3001 npm start > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  ✓ Frontend PID: $FRONTEND_PID"

sleep 5

# Check if services are running
echo ""
echo "Verifying services..."

if curl -s http://localhost:8000/ | grep -q "Backend running"; then
    echo "  ✅ Backend running on http://localhost:8000"
else
    echo "  ❌ Backend failed to start. Check /tmp/backend.log"
fi

if curl -s http://localhost:3001/ | grep -q "DOCTYPE"; then
    echo "  ✅ Frontend running on http://localhost:3001"
else
    echo "  ⏳ Frontend still loading... (this is normal)"
fi

echo ""
echo "🎉 Legal Support Chatbot is starting!"
echo "   Open your browser: http://localhost:3001"
echo ""
echo "Logs:"
echo "  Backend: tail -f /tmp/backend.log"
echo "  Frontend: tail -f /tmp/frontend.log"
echo ""
echo "To stop: pkill -f 'uvicorn app:app' && pkill -f 'npm start'"
