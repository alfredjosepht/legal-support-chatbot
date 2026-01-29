#!/bin/bash
# Setup script for Legal Support Chatbot

echo "🚀 Setting up Legal Support Chatbot..."
echo ""

# Check Python
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  Found: $PYTHON_VERSION"

# Check Node
echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 14+"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "  Found: $NODE_VERSION"

echo ""
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Backend installation failed"
    exit 1
fi

echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Frontend installation failed"
    exit 1
fi
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the system:"
echo ""
echo "Terminal 1 - Backend:"
echo "  python -m uvicorn app:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend && PORT=3001 npm start"
echo ""
echo "Then open: http://localhost:3001"
echo ""
