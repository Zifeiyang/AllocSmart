#!/bin/bash

# Run the dashboard with all necessary services

# Start the backend server
echo "Starting backend server..."
cd backend
FLASK_APP=app.py flask run &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Wait for the backend to start
sleep 2

# Start the web API server
echo "Starting web API server..."
python web_portfolio_init.py &
WEB_API_PID=$!
echo "Web API server started with PID: $WEB_API_PID"

# Wait for the web API to start
sleep 2

# Start the frontend server
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

echo ""
echo "All services started!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:5000"
echo "Web API: http://localhost:5001"
echo ""
echo "If you encounter issues with portfolio initialization, try the following:"
echo "1. Use the direct portfolio initialization page: http://localhost:5173/direct_portfolio_init.html"
echo "2. Run the direct database fix script: cd backend && python direct_db_fix.py <username> <initial_cash>"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to clean up on exit
cleanup() {
    echo "Stopping all services..."
    kill $BACKEND_PID $WEB_API_PID $FRONTEND_PID
    echo "All services stopped"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup INT

# Keep the script running
wait
