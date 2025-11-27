#!/usr/bin/env python3
"""
Script to execute flights.sql PostgreSQL dump file.
This script handles \connect commands and COPY FROM stdin statements.
"""

import psycopg2
import re
import sys
from pathlib import Path

# ---------- Connection settings ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",  # Connect to default database first
    "user": "postgres",
    "password": "your_password_here"  # Update this!
}

def execute_sql_file(sql_file_path):
    """
    Execute a PostgreSQL dump file that may contain \connect commands.
    """
    sql_file = Path(sql_file_path)
    if not sql_file.exists():
        print(f"Error: File {sql_file_path} not found!")
        return False
    
    print(f"Reading SQL file: {sql_file_path}")
    
    # Read the entire file
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by \connect commands to handle database switches
    parts = re.split(r'\\connect\s+(\w+)', content)
    
    current_db = DB_CONFIG['dbname']
    conn = None
    
    try:
        # First part (before any \connect)
        if parts[0].strip():
            conn = psycopg2.connect(**DB_CONFIG)
            conn.autocommit = True  # Required for CREATE DATABASE
            print(f"Connected to database: {current_db}")
            execute_sql_statements(conn, parts[0])
        
        # Process remaining parts (alternating between \connect dbname and SQL)
        for i in range(1, len(parts), 2):
            if i < len(parts) - 1:
                new_db = parts[i]
                sql_block = parts[i + 1]
                
                if conn:
                    conn.close()
                
                # Update connection to new database
                db_config = DB_CONFIG.copy()
                db_config['dbname'] = new_db
                conn = psycopg2.connect(**db_config)
                conn.autocommit = True
                current_db = new_db
                print(f"Connected to database: {current_db}")
                
                if sql_block.strip():
                    execute_sql_statements(conn, sql_block)
        
        print("\nSQL file executed successfully!")
        return True
        
    except psycopg2.Error as e:
        print(f"\nDatabase error: {e}")
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

def execute_sql_statements(conn, sql_content):
    """
    Execute SQL statements, handling COPY FROM stdin commands.
    """
    cursor = conn.cursor()
    
    # Split by COPY ... FROM stdin; and handle separately
    # This is a simplified approach - for production, you'd want more robust parsing
    copy_pattern = r'(COPY\s+[^;]+FROM\s+stdin;.*?\n\\.\n)'
    
    parts = re.split(copy_pattern, sql_content, flags=re.DOTALL | re.IGNORECASE)
    
    for part in parts:
        if not part.strip():
            continue
        
        # Check if this is a COPY FROM stdin block
        if re.match(r'COPY\s+[^;]+FROM\s+stdin;', part, re.IGNORECASE):
            # Extract COPY command and data
            lines = part.split('\n')
            copy_command = lines[0]
            
            # Find the data lines (between COPY command and \.)
            data_lines = []
            in_data = False
            for line in lines[1:]:
                if line.strip() == '\\.':
                    break
                if in_data or line.strip():
                    data_lines.append(line)
                    in_data = True
            
            # Execute COPY command with data
            try:
                # Use copy_expert for COPY FROM stdin
                data_str = '\n'.join(data_lines)
                cursor.copy_expert(copy_command, open_from_string(data_str))
                conn.commit()
            except Exception as e:
                print(f"Warning: Error executing COPY command: {e}")
                # Try alternative approach - might need to parse differently
        else:
            # Regular SQL statements
            # Split by semicolons but be careful with functions/procedures
            statements = split_sql_statements(part)
            
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                        conn.commit()
                    except psycopg2.Error as e:
                        # Some statements might fail (e.g., IF NOT EXISTS)
                        if "already exists" not in str(e).lower():
                            print(f"Warning: {e}")
                        conn.rollback()
    
    cursor.close()

def split_sql_statements(sql_text):
    """
    Split SQL text into individual statements, handling functions/procedures.
    """
    statements = []
    current = ""
    in_function = False
    dollar_quote = None
    
    for line in sql_text.split('\n'):
        # Check for dollar quoting (used in functions)
        if re.search(r'\$[^$]*\$', line):
            if dollar_quote is None:
                # Find the dollar quote tag
                match = re.search(r'(\$[^$]*\$)', line)
                if match:
                    dollar_quote = match.group(1)
            else:
                # Check if we're closing the dollar quote
                if dollar_quote in line:
                    dollar_quote = None
        
        current += line + '\n'
        
        # If we're not in a dollar-quoted block and see a semicolon, it's end of statement
        if dollar_quote is None and line.strip().endswith(';'):
            statements.append(current)
            current = ""
    
    if current.strip():
        statements.append(current)
    
    return statements

def open_from_string(data_string):
    """Create a file-like object from a string for copy_expert."""
    from io import StringIO
    return StringIO(data_string)

if __name__ == "__main__":
    # Update password before running!
    if DB_CONFIG["password"] == "your_password_here":
        print("WARNING: Please update the password in DB_CONFIG before running!")
        print("   Edit this file and set DB_CONFIG['password'] to your PostgreSQL password.")
        sys.exit(1)
    
    sql_file = Path(__file__).parent / "flights.sql"
    
    if len(sys.argv) > 1:
        sql_file = Path(sys.argv[1])
    
    success = execute_sql_file(sql_file)
    sys.exit(0 if success else 1)

