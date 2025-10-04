#!/bin/bash

echo "???? Starting NASA Exoplanet Predictor App..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "Port $1 is already in use"
        return 1
    else
        echo "Port $1 is available"
        return 0
    fi
}

# Kill any existing processes on our ports
echo "???? Cleaning up existing processes..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
pkill -f "react-scripts.*3000" 2>/dev/null || true
pkill -f "vite.*5173" 2>/dev/null || true

# Wait a moment
sleep 2

# Start backend (FastAPI)
echo "???? Starting FastAPI Backend on port 8000..."
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo "??? Backend started successfully (PID: $BACKEND_PID)"
else
    echo "??? Backend failed to start"
    exit 1
fi

# Start frontend (React)
echo "???? Starting React Frontend on port 3000..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "??? Application Started Successfully!"
echo ""
echo "???? Frontend: http://localhost:3000"
echo "???? Backend API: http://localhost:8000"
echo "???? API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "???? Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "??? Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
