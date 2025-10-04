#!/bin/bash

echo "🚀 Starting NASA Exoplanet Prediction Frontend..."

cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🌐 Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
echo "Make sure your FastAPI backend is running on: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm start
