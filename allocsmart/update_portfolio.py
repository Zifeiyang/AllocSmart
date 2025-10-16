#!/usr/bin/env python3
"""
Update Portfolio Script
This script directly updates the portfolio data in the database
"""

import sys
import json
import logging
import sqlite3
import os
import datetime
import argparse

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

def update_portfolio(username, initial_cash, initial_holdings):
    """Update the portfolio data for a user."""
    logger.info(f"Updating portfolio for user: {username}")
    logger.info(f"Initial cash: {initial_cash}")
    logger.info(f"Initial holdings: {initial_holdings}")
    
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
        
        # Get column names
        column_names = [col[1] for col in portfolio_columns]
        
        # Prepare the update data
        now = datetime.datetime.now().isoformat()
        
        if portfolio:
            logger.info(f"Found existing portfolio: {portfolio}")
            
            # Update the portfolio
            update_parts = []
            values = []
            
            # Update initial_cash if available
            if "initial_cash" in column_names:
                update_parts.append("initial_cash = ?")
                values.append(initial_cash)
            
            # Update initial_holdings_json if available
            if "initial_holdings_json" in column_names:
                update_parts.append("initial_holdings_json = ?")
                values.append(json.dumps(initial_holdings))
            
            # Update updated_at if available
            if "updated_at" in column_names:
                update_parts.append("updated_at = ?")
                values.append(now)
            
            # Add user_id to values
            values.append(user_id)
            
            # Build and execute the query
            query = f"UPDATE {portfolio_table} SET {', '.join(update_parts)} WHERE user_id = ?"
            logger.info(f"Update query: {query}")
            logger.info(f"Update values: {values}")
            
            cursor.execute(query, values)
            conn.commit()
            
            # Verify the portfolio was updated
            cursor.execute(f"SELECT * FROM {portfolio_table} WHERE user_id = ?", (user_id,))
            updated_portfolio = cursor.fetchone()
            
            if not updated_portfolio:
                logger.error("Failed to update portfolio")
                return False
            
            logger.info(f"Portfolio updated successfully: {updated_portfolio}")
        else:
            logger.info("No existing portfolio found, creating a new one")
            
            # Create a new portfolio
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
        
        return True
    except Exception as e:
        logger.error(f"Error updating portfolio: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def parse_holdings(holdings_str):
    """Parse holdings string into a dictionary."""
    if not holdings_str:
        return {}
    
    try:
        # Try to parse as JSON
        return json.loads(holdings_str)
    except json.JSONDecodeError:
        # Try to parse as comma-separated list of ticker:quantity pairs
        holdings = {}
        pairs = holdings_str.split(',')
        for pair in pairs:
            if ':' in pair:
                ticker, quantity = pair.split(':')
                try:
                    holdings[ticker.strip().upper()] = float(quantity.strip())
                except ValueError:
                    logger.warning(f"Invalid quantity for {ticker}: {quantity}")
        return holdings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update portfolio data in the database')
    parser.add_argument('username', help='Username of the user')
    parser.add_argument('initial_cash', type=float, help='Initial cash amount')
    parser.add_argument('--holdings', help='Initial holdings as JSON string or comma-separated list of ticker:quantity pairs')
    
    args = parser.parse_args()
    
    # Parse holdings
    initial_holdings = parse_holdings(args.holdings)
    
    # Update portfolio
    success = update_portfolio(args.username, args.initial_cash, initial_holdings)
    
    if success:
        print(f"Portfolio updated successfully for user {args.username}")
        sys.exit(0)
    else:
        print(f"Failed to update portfolio for user {args.username}")
        sys.exit(1)
