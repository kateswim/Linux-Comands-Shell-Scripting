#!/usr/bin/env python3
"""
Hands-on Lab: Improving Performance of Slow Queries in MySQL
Exercises: EXPLAIN, Indexing, UNION ALL, Selective Queries
"""

import mysql.connector
from mysql.connector import Error
import time

# ---------- Configuration ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",  # Update if needed
    "database": "employees"
}

# ---------- Helper Functions ----------

def get_connection():
    """Get MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Connection error: {e}")
        return None

def run_query_with_timing(cursor, query, description):
    """Execute a query and measure execution time."""
    print(f"\n{'='*70}")
    print(f"Query: {description}")
    print(f"{'='*70}")
    print(query)
    print()
    
    start_time = time.time()
    cursor.execute(query)
    elapsed = time.time() - start_time
    
    rows = cursor.fetchall()
    
    print(f"✅ Executed in {elapsed:.4f} seconds")
    print(f"📊 Rows returned: {len(rows)}")
    if rows and len(rows) <= 10:
        for row in rows:
            print(f"   {row}")
    elif rows:
        print(f"   (showing first 10 of {len(rows)} rows)")
        for row in rows[:10]:
            print(f"   {row}")
    
    return elapsed

def explain_query(cursor, query, description):
    """Run EXPLAIN on a query to check performance."""
    print(f"\n{'='*70}")
    print(f"EXPLAIN ANALYSIS: {description}")
    print(f"{'='*70}")
    print(query)
    print()
    
    explain_query = f"EXPLAIN {query}"
    cursor.execute(explain_query)
    
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    # Print header
    print(" | ".join(f"{col:15}" for col in columns))
    print("-" * (len(columns) * 18))
    
    # Print rows
    for row in rows:
        print(" | ".join(f"{str(val):15}" for val in row))
    
    print("\n📌 Key points to look for:")
    print("   - 'key': Which index is used (NULL = no index)")
    print("   - 'rows': Estimated rows examined")
    print("   - 'Extra': Using index, Using where, etc.")

# ---------- Lab Exercises ----------

def exercise_1_basic_query():
    """Exercise 1: Run a basic query without optimization."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    query = """
    SELECT emp_no, first_name, last_name, hire_date 
    FROM employees 
    WHERE last_name = 'Bauer';
    """
    
    explain_query(cursor, query, "Find employees with last name 'Bauer' (before index)")
    
    cursor.close()
    conn.close()

def exercise_2_add_index():
    """Exercise 2: Create an index to improve performance."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Check if index already exists
    cursor.execute("""
    SELECT 1 FROM INFORMATION_SCHEMA.STATISTICS 
    WHERE TABLE_SCHEMA='employees' AND TABLE_NAME='employees' 
    AND INDEX_NAME='idx_last_name'
    """)
    
    if cursor.fetchone():
        print("\n✅ Index idx_last_name already exists.")
    else:
        print("\n🔧 Creating index on last_name column...")
        cursor.execute("ALTER TABLE employees ADD INDEX idx_last_name (last_name);")
        conn.commit()
        print("✅ Index created successfully.")
    
    # Now re-run EXPLAIN to see the improvement
    query = """
    SELECT emp_no, first_name, last_name, hire_date 
    FROM employees 
    WHERE last_name = 'Bauer';
    """
    
    explain_query(cursor, query, "Find employees with last name 'Bauer' (after index)")
    
    cursor.close()
    conn.close()

def exercise_3_selective_columns():
    """Exercise 3: Be SELECTive - only request needed columns."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print("Exercise 3: Being SELECTive with Columns")
    print(f"{'='*70}")
    
    # Bad: SELECT *
    print("\n❌ BAD: SELECT * (retrieves all columns)")
    query_bad = "SELECT * FROM employees WHERE emp_no < 10010 LIMIT 3;"
    run_query_with_timing(cursor, query_bad, "SELECT all columns")
    
    # Good: SELECT specific columns
    print("\n✅ GOOD: SELECT specific columns (emp_no, first_name, last_name)")
    query_good = """
    SELECT emp_no, first_name, last_name 
    FROM employees 
    WHERE emp_no < 10010 
    LIMIT 3;
    """
    run_query_with_timing(cursor, query_good, "SELECT only needed columns")
    
    cursor.close()
    conn.close()

def exercise_4_union_all():
    """Exercise 4: Use UNION ALL for combining result sets."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print("Exercise 4: Using UNION ALL")
    print(f"{'='*70}")
    
    # Example: Combine results from two queries
    query_union_all = """
    SELECT emp_no, first_name, last_name, 'Manager' AS role
    FROM employees 
    WHERE emp_no IN (10001, 10002, 10003)
    UNION ALL
    SELECT emp_no, first_name, last_name, 'Staff' AS role
    FROM employees 
    WHERE emp_no IN (10004, 10005, 10006);
    """
    
    print("\n✅ Using UNION ALL (faster - no duplicate removal)")
    run_query_with_timing(cursor, query_union_all, "UNION ALL example")
    
    cursor.close()
    conn.close()

def exercise_5_filtering_optimization():
    """Exercise 5: Push filters that use indexed columns."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print("Exercise 5: Optimizing Filters")
    print(f"{'='*70}")
    
    # Count employees
    cursor.execute("SELECT COUNT(*) FROM employees;")
    total = cursor.fetchone()[0]
    print(f"\nTotal employees in database: {total}")
    
    # Bad: Filter after retrieval
    print("\n❌ BAD: Retrieve and filter in application")
    query_bad = """
    SELECT emp_no, first_name, last_name 
    FROM employees 
    WHERE birth_date > '1960-01-01';
    """
    print(query_bad)
    cursor.execute(query_bad)
    print(f"✅ Rows matching condition: {len(cursor.fetchall())}")
    
    # Show EXPLAIN to understand index usage
    explain_query(cursor, query_bad, "Filter on birth_date (is there an index?)")
    
    cursor.close()
    conn.close()

def exercise_6_advanced_explain():
    """Exercise 6: Advanced EXPLAIN with JSON format."""
    conn = get_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    print(f"\n{'='*70}")
    print("Exercise 6: Advanced EXPLAIN (JSON Format)")
    print(f"{'='*70}")
    
    query = """
    SELECT e.emp_no, e.first_name, e.last_name, s.salary
    FROM employees e
    JOIN salaries s ON e.emp_no = s.emp_no
    WHERE e.hire_date > '1990-01-01'
    LIMIT 10;
    """
    
    print("\nRunning EXPLAIN FORMAT=JSON...")
    explain_json_query = f"EXPLAIN FORMAT=JSON {query}"
    
    try:
        cursor.execute(explain_json_query)
        result = cursor.fetchone()[0]
        print(result)
        print("\n📌 This shows detailed query execution plan including:")
        print("   - Join type (inner, left, etc.)")
        print("   - Index usage per table")
        print("   - Estimated cost")
    except Error as e:
        print(f"⚠️  JSON format may not be available: {e}")
        # Fallback to standard EXPLAIN
        explain_query(cursor, query, "JOIN query")
    
    cursor.close()
    conn.close()

# ---------- Main ----------

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Hands-on Lab: Query Performance Optimization" + " "*11 + "║")
    print("║" + " "*16 + "Improving Performance of Slow Queries in MySQL" + " "*6 + "║")
    print("╚" + "="*68 + "╝")
    
    exercises = [
        ("Exercise 1: Basic Query (Before Optimization)", exercise_1_basic_query),
        ("Exercise 2: Add Index & Verify Improvement", exercise_2_add_index),
        ("Exercise 3: Be SELECTive with Columns", exercise_3_selective_columns),
        ("Exercise 4: Use UNION ALL for Combining Results", exercise_4_union_all),
        ("Exercise 5: Optimize Filters", exercise_5_filtering_optimization),
        ("Exercise 6: Advanced EXPLAIN Analysis", exercise_6_advanced_explain),
    ]
    
    for i, (title, func) in enumerate(exercises, 1):
        try:
            func()
        except Error as e:
            print(f"\n❌ Exercise {i} error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error in Exercise {i}: {e}")
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*20 + "✅ Lab Complete!" + " "*33 + "║")
    print("╚" + "="*68 + "╝")
    print("\n")
