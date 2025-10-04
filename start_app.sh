#!/bin/bash

echo "🚀 Starting NASA Exoplanet Prediction System..."
echo "Team AstroVenture 🇵🇰🇦🇿"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "🌐 Starting backend server..."
python3 app.py &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 3

echo "🎨 Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ NASA Exoplanet Prediction System is running!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait

# Cleanup
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
echo "🛑 Servers stopped."
