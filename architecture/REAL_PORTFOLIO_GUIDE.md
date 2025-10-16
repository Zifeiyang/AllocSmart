# Real Portfolio Data Guide

This guide explains how to display your real portfolio data in the dashboard.

## Option 1: Use the Dashboard Button (Easiest)

1. Go to the dashboard
2. If you see "No holdings found", click the "Load My Real Portfolio" button
3. This will attempt to load your real portfolio data from all available sources
4. Your real portfolio data should now be displayed

## Option 2: Run the Show Real Portfolio Script

1. Open a terminal in the project root directory
2. Run the show real portfolio script with your username:
   ```bash
   ./show_real_portfolio.sh <your_username>
   ```
3. This will retrieve your real portfolio data and save it to a JSON file
4. Go to the dashboard and click the "Load My Real Portfolio" button
5. Your real portfolio data should now be displayed

## Option 3: Check and Fix the Database

If you're still having issues, you can check and fix the database directly:

1. Run the retrieve_real_portfolio.py script to see your actual portfolio data:
   ```bash
   cd backend
   python retrieve_real_portfolio.py <your_username>
   ```
2. This will show you exactly what's in the database for your portfolio
3. If there are issues with your portfolio data, you can fix them using the debug_portfolio.py script:
   ```bash
   python debug_portfolio.py <your_username>
   ```
4. Go to the dashboard and click the "Load My Real Portfolio" button
5. Your real portfolio data should now be displayed

## Understanding Your Portfolio Data

The portfolio data consists of:

1. **Initial Cash**: The amount of cash you started with
2. **Initial Holdings**: The stocks you initially added to your portfolio
3. **Current Holdings**: The current state of your portfolio, including any transactions

If you initialized your portfolio through the portfolio-init page, your data should be stored in the database. The "Load My Real Portfolio" button will retrieve this data and display it on the dashboard.

## Troubleshooting

If you're still having issues:

1. Check the browser console for any error messages
2. Try clearing your browser cache and local storage
3. Make sure the backend server is running
4. Try restarting both the frontend and backend servers
5. Check the database directly to see if your portfolio data exists

## Contact Support

If you continue to experience issues, please contact support with the following information:
- Your username
- Steps you've taken to fix the issue
- Any error messages you've encountered
- Screenshots of the dashboard showing the issue
