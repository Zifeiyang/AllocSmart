# Portfolio Initialization Troubleshooting Guide

If you're experiencing issues with portfolio initialization or the dashboard not displaying your portfolio data correctly, follow these steps to resolve the problem.

## Quick Fix: Force Refresh

1. On the dashboard, click the "Refresh Portfolio" button in the top-right corner.
2. This will attempt to fetch your portfolio data using multiple fallback methods.

## Common Issues and Solutions

### Issue: Dashboard shows "No holdings found" even after initializing portfolio

**Solution 1: Force Refresh**
- Click the "Refresh Portfolio" button on the dashboard.

**Solution 2: Clear Browser Cache**
1. Open your browser's developer tools (F12 or right-click and select "Inspect")
2. Go to the "Application" tab
3. Select "Local Storage" on the left
4. Clear any items related to portfolio data
5. Refresh the page

**Solution 3: Reinitialize Portfolio**
1. Go to the Portfolio Initialization page (/portfolio-init)
2. Enter your initial cash and holdings again
3. Submit the form

### Issue: Portfolio data not persisting after page refresh

This could be due to issues with the backend database or API connectivity.

**Solution: Use Direct Database Fix**

Run the direct database fix script to manually initialize your portfolio:

```bash
cd backend
python direct_db_fix.py <username> <initial_cash> --holdings '{"AAPL":10,"MSFT":5}'
```

Replace `<username>` with your username, `<initial_cash>` with your initial cash amount, and modify the holdings JSON as needed.

### Issue: API errors when trying to initialize portfolio

If you're seeing API errors, try using the direct web API:

1. Make a POST request to `/api/web/portfolio/init` with the following JSON body:
```json
{
  "username": "your_username",
  "initial_cash": 10000,
  "initial_holdings": {
    "AAPL": 10,
    "MSFT": 5
  }
}
```

2. You can use tools like Postman or curl to make this request.

## Running All Services

For the best experience, run all services using the provided script:

```bash
./run_dashboard.sh
```

This will start:
- Backend Flask server
- Web API server
- Frontend development server

## Manual Database Fix

If all else fails, you can directly modify the database:

1. Locate the SQLite database file (usually `backend/app.db` or `backend/instance/app.db`)
2. Use a SQLite browser tool to open the database
3. Find the `user_portfolio` table
4. Add or modify your portfolio entry with your user ID, initial cash, and holdings JSON

## Contact Support

If you continue to experience issues, please contact support with the following information:
- Your username
- Steps you've taken to initialize your portfolio
- Any error messages you've encountered
- Screenshots of the dashboard showing the issue
