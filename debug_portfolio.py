#!/usr/bin/env python3
"""
Debug Portfolio Script
This script directly checks and fixes portfolio data in the database
"""

import sys
import json
import logging
import sqlite3
import os
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_db_path():
    """Find the database file by searching common locations."""
    possible_paths = [
        'app.db',
        'instance/app.db',
        'instance/allocsmart.db',
        'backend/app.db',
        'backend/instance/app.db',
        'backend/instance/allocsmart.db',
        '../app.db',
        '../instance/app.db',
        '../instance/allocsmart.db'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found database at {path}")
            return path
    
    logger.error("Could not find database file")
    return None

def debug_portfolio(username):
    """Debug portfolio data for a user."""
    logger.info(f"Debugging portfolio for user: {username}")
    
    # Find the database
    db_path = find_db_path()
    if not db_path:
        logger.error("Database not found. Cannot proceed.")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check database schema
        logger.info("Checking database schema...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"Tables in database: {[t[0] for t in tables]}")
        
        # Find user table
        user_table = None
        for table_candidate in ['user', 'users', 'User']:
            if (table_candidate,) in tables:
                user_table = table_candidate
                logger.info(f"Found user table: {user_table}")
                break
        
        if not user_table:
            logger.error("User table not found")
            return False
        
        # Check user table schema
        cursor.execute(f"PRAGMA table_info({user_table})")
        user_columns = cursor.fetchall()
        logger.info(f"User table columns: {[col[1] for col in user_columns]}")
        
        # Find user
        username_column = None
        for col in user_columns:
            if col[1].lower() in ['username', 'name']:
                username_column = col[1]
                break
        
        if not username_column:
            logger.error("Could not find username column in user table")
            return False
        
        logger.info(f"Using username column: {username_column}")
        cursor.execute(f"SELECT * FROM {user_table} WHERE {username_column} = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            logger.error(f"User '{username}' not found in database")
            return False
        
        user_id = user[0]  # Assuming ID is the first column
        logger.info(f"Found user: {username} (ID: {user_id})")
        
        # Find portfolio table
        portfolio_table = None
        for table_candidate in ['user_portfolio', 'UserPortfolio', 'portfolio']:
            if (table_candidate,) in tables:
                portfolio_table = table_candidate
                logger.info(f"Found portfolio table: {portfolio_table}")
                break
        
        if not portfolio_table:
            logger.error("Portfolio table not found")
            return False
        
        # Check portfolio table schema
        cursor.execute(f"PRAGMA table_info({portfolio_table})")
        portfolio_columns = cursor.fetchall()
        logger.info(f"Portfolio table columns: {[col[1] for col in portfolio_columns]}")
        
        # Check if user has a portfolio
        cursor.execute(f"SELECT * FROM {portfolio_table} WHERE user_id = ?", (user_id,))
        portfolio = cursor.fetchone()
        
        if not portfolio:
            logger.error(f"No portfolio found for user {username}")
            logger.info("Creating a new portfolio with sample data...")
            
            # Create a new portfolio with sample data
            now = datetime.datetime.now().isoformat()
            initial_cash = 10000.0
            initial_holdings = {"AAPL": 10, "MSFT": 5, "GOOGL": 2}
            
            # Build the insert query based on available columns
            column_names = [col[1] for col in portfolio_columns]
            query_parts = []
            values = []
            
            # Always include user_id
            query_parts.append("user_id")
            values.append(user_id)
            
            # Add initial_cash if available
            if "initial_cash" in column_names:
                query_parts.append("initial_cash")
                values.append(initial_cash)
            
            # Add initial_holdings_json if available
            if "initial_holdings_json" in column_names:
                query_parts.append("initial_holdings_json")
                values.append(json.dumps(initial_holdings))
            
            # Add updated_at if available
            if "updated_at" in column_names:
                query_parts.append("updated_at")
                values.append(now)
            
            # Build and execute the query
            placeholders = ", ".join(["?" for _ in query_parts])
            query = f"INSERT INTO {portfolio_table} ({', '.join(query_parts)}) VALUES ({placeholders})"
            logger.info(f"Insert query: {query}")
            logger.info(f"Insert values: {values}")
            
            cursor.execute(query, values)
            conn.commit()
            
            # Verify the portfolio was created
            cursor.execute(f"SELECT * FROM {portfolio_table} WHERE user_id = ?", (user_id,))
            portfolio = cursor.fetchone()
            
            if not portfolio:
                logger.error("Failed to create portfolio")
                return False
            
            logger.info(f"Portfolio created successfully: {portfolio}")
        else:
            logger.info(f"Found existing portfolio: {portfolio}")
            
            # Check if portfolio has holdings
            holdings_column = None
            for col in portfolio_columns:
                if col[1].lower() in ['initial_holdings_json', 'holdings_json', 'holdings']:
                    holdings_column = col[1]
                    break
            
            if not holdings_column:
                logger.error("Could not find holdings column in portfolio table")
                return False
            
            # Get the index of the holdings column
            holdings_index = [i for i, col in enumerate(portfolio_columns) if col[1] == holdings_column][0]
            
            # Check if holdings are empty or invalid
            holdings_json = portfolio[holdings_index]
            try:
                holdings = json.loads(holdings_json) if holdings_json else {}
                logger.info(f"Current holdings: {holdings}")
                
                if not holdings:
                    logger.info("Holdings are empty, updating with sample data...")
                    sample_holdings = {"AAPL": 10, "MSFT": 5, "GOOGL": 2}
                    
                    # Update holdings
                    cursor.execute(
                        f"UPDATE {portfolio_table} SET {holdings_column} = ? WHERE user_id = ?",
                        (json.dumps(sample_holdings), user_id)
                    )
                    conn.commit()
                    
                    logger.info("Holdings updated successfully")
            except json.JSONDecodeError:
                logger.error(f"Invalid holdings JSON: {holdings_json}")
                logger.info("Updating with valid sample data...")
                
                sample_holdings = {"AAPL": 10, "MSFT": 5, "GOOGL": 2}
                
                # Update holdings
                cursor.execute(
                    f"UPDATE {portfolio_table} SET {holdings_column} = ? WHERE user_id = ?",
                    (json.dumps(sample_holdings), user_id)
                )
                conn.commit()
                
                logger.info("Holdings updated successfully")
        
        # Final verification
        cursor.execute(f"SELECT * FROM {portfolio_table} WHERE user_id = ?", (user_id,))
        updated_portfolio = cursor.fetchone()
        logger.info(f"Final portfolio state: {updated_portfolio}")
        
        return True
    except Exception as e:
        logger.error(f"Error debugging portfolio: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_portfolio.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    success = debug_portfolio(username)
    
    if success:
        print(f"Portfolio debugging completed successfully for user {username}")
        print("Now refresh your dashboard to see the changes")
        sys.exit(0)
    else:
        print(f"Failed to debug portfolio for user {username}")
        sys.exit(1)
