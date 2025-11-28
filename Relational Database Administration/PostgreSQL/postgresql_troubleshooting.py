#!/usr/bin/env python3
"""
PostgreSQL Troubleshooting Script
This script automates common troubleshooting tasks for PostgreSQL database administration:
- Check and modify configuration parameters
- Enable error logging
- Test server performance
- Diagnose connection issues
- View server logs
"""

import psycopg2
from psycopg2 import Error
import time
import subprocess
import os
import re
from pathlib import Path

# ---------- Connection settings ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "demo",  # flights database
    "user": "katehoncharova",
    "password": ""
}

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",  # Connect to postgres database for config changes
    "user": "katehoncharova",
    "password": ""
}

def get_connection(db_config=None):
    """Get PostgreSQL database connection"""
    if db_config is None:
        db_config = DB_CONFIG
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# ---------- Configuration Functions ----------

def show_config_parameter(parameter_name, db_config=None):
    """Show the current value of a configuration parameter"""
    conn = get_connection(db_config)
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(f"SHOW {parameter_name};")
                value = cur.fetchone()[0]
                print(f"{parameter_name}: {value}")
                return value
        except Error as e:
            print(f"Error showing parameter {parameter_name}: {e}")
            return None
        finally:
            conn.close()
    return None

def check_logging_collector():
    """Check if logging collector is enabled"""
    print("\n" + "=" * 60)
    print("Checking logging_collector status...")
    print("=" * 60)
    return show_config_parameter("logging_collector", POSTGRES_CONFIG)

def check_max_connections():
    """Check current max_connections setting"""
    print("\n" + "=" * 60)
    print("Checking max_connections...")
    print("=" * 60)
    return show_config_parameter("max_connections", POSTGRES_CONFIG)

def check_shared_buffers():
    """Check current shared_buffers setting"""
    print("\n" + "=" * 60)
    print("Checking shared_buffers...")
    print("=" * 60)
    return show_config_parameter("shared_buffers", POSTGRES_CONFIG)

def check_work_mem():
    """Check current work_mem setting"""
    print("\n" + "=" * 60)
    print("Checking work_mem...")
    print("=" * 60)
    return show_config_parameter("work_mem", POSTGRES_CONFIG)

def check_maintenance_work_mem():
    """Check current maintenance_work_mem setting"""
    print("\n" + "=" * 60)
    print("Checking maintenance_work_mem...")
    print("=" * 60)
    return show_config_parameter("maintenance_work_mem", POSTGRES_CONFIG)

def check_log_directory():
    """Check where PostgreSQL logs are stored"""
    print("\n" + "=" * 60)
    print("Checking log_directory...")
    print("=" * 60)
    return show_config_parameter("log_directory", POSTGRES_CONFIG)

def find_postgresql_conf():
    """Try to find postgresql.conf file location"""
    # Common locations for postgresql.conf
    possible_paths = [
        Path("/usr/local/var/postgres/postgresql.conf"),  # macOS Homebrew default
        Path("/opt/homebrew/var/postgres/postgresql.conf"),  # macOS Homebrew Apple Silicon
        Path("/var/lib/postgresql/data/postgresql.conf"),  # Linux default
        Path(os.path.expanduser("~/.postgresql/postgresql.conf")),  # User config
    ]
    
    # Try to get from PostgreSQL
    conn = get_connection(POSTGRES_CONFIG)
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SHOW config_file;")
                config_file = cur.fetchone()[0]
                if config_file and Path(config_file).exists():
                    return Path(config_file)
        except:
            pass
        finally:
            conn.close()
    
    # Check common locations
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def modify_postgresql_conf(parameter, new_value, conf_path=None):
    """
    Modify a parameter in postgresql.conf file
    
    Args:
        parameter: Name of the parameter (e.g., 'max_connections')
        new_value: New value to set (e.g., '100' or '128MB')
        conf_path: Path to postgresql.conf (if None, will try to find it)
    
    Returns:
        True if successful, False otherwise
    """
    if conf_path is None:
        conf_path = find_postgresql_conf()
    
    if conf_path is None or not conf_path.exists():
        print(f"Error: Could not find postgresql.conf file")
        print("Please provide the path to postgresql.conf manually")
        return False
    
    try:
        # Read the file
        with open(conf_path, 'r') as f:
            lines = f.readlines()
        
        # Pattern to match the parameter (with or without comment)
        # Matches: parameter = value or # parameter = value
        pattern = re.compile(r'^(\s*#?\s*)' + re.escape(parameter) + r'\s*=\s*.*$', re.IGNORECASE)
        
        modified = False
        new_lines = []
        
        for line in lines:
            if pattern.match(line):
                # Found the parameter, replace it
                indent = re.match(r'^(\s*)', line).group(1)
                new_line = f"{indent}{parameter} = {new_value}\n"
                new_lines.append(new_line)
                modified = True
                print(f"Modified: {parameter} = {new_value}")
            else:
                new_lines.append(line)
        
        if not modified:
            # Parameter not found, add it at the end
            new_lines.append(f"\n# Modified by troubleshooting script\n")
            new_lines.append(f"{parameter} = {new_value}\n")
            print(f"Added: {parameter} = {new_value}")
        
        # Write the file back
        with open(conf_path, 'w') as f:
            f.writelines(new_lines)
        
        print(f"Successfully modified {conf_path}")
        print("WARNING: PostgreSQL server must be restarted for changes to take effect!")
        return True
        
    except Exception as e:
        print(f"Error modifying postgresql.conf: {e}")
        return False

def enable_logging_collector(conf_path=None):
    """Enable logging_collector in postgresql.conf"""
    print("\n" + "=" * 60)
    print("Enabling logging_collector...")
    print("=" * 60)
    return modify_postgresql_conf("logging_collector", "on", conf_path)

def set_max_connections(value, conf_path=None):
    """Set max_connections in postgresql.conf"""
    print("\n" + "=" * 60)
    print(f"Setting max_connections to {value}...")
    print("=" * 60)
    return modify_postgresql_conf("max_connections", str(value), conf_path)

def set_shared_buffers(value, conf_path=None):
    """Set shared_buffers in postgresql.conf"""
    print("\n" + "=" * 60)
    print(f"Setting shared_buffers to {value}...")
    print("=" * 60)
    return modify_postgresql_conf("shared_buffers", value, conf_path)

def set_work_mem(value, conf_path=None):
    """Set work_mem in postgresql.conf"""
    print("\n" + "=" * 60)
    print(f"Setting work_mem to {value}...")
    print("=" * 60)
    return modify_postgresql_conf("work_mem", value, conf_path)

def set_maintenance_work_mem(value, conf_path=None):
    """Set maintenance_work_mem in postgresql.conf"""
    print("\n" + "=" * 60)
    print(f"Setting maintenance_work_mem to {value}...")
    print("=" * 60)
    return modify_postgresql_conf("maintenance_work_mem", value, conf_path)

def apply_lab_fixes(conf_path=None):
    """
    Apply all the fixes from the lab:
    - max_connections: 4 -> 100
    - shared_buffers: 128kB -> 128MB
    - work_mem: 64kB -> 4MB
    - maintenance_work_mem: 1MB -> 64MB
    """
    print("\n" + "=" * 60)
    print("Applying Lab Configuration Fixes")
    print("=" * 60)
    
    results = []
    results.append(set_max_connections(100, conf_path))
    results.append(set_shared_buffers("128MB", conf_path))
    results.append(set_work_mem("4MB", conf_path))
    results.append(set_maintenance_work_mem("64MB", conf_path))
    
    if all(results):
        print("\nAll configuration changes applied successfully!")
        print("Please restart PostgreSQL server for changes to take effect.")
        return True
    else:
        print("\nSome configuration changes failed. Please check the errors above.")
        return False

# ---------- Performance Testing Functions ----------

def test_simple_query():
    """Test performance of a simple query"""
    print("\n" + "=" * 60)
    print("Testing simple query performance...")
    print("=" * 60)
    sql = "SELECT * FROM bookings.aircrafts_data;"
    conn = get_connection()
    if conn:
        try:
            start_time = time.time()
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            print(f"Query executed in {elapsed_time:.2f} ms")
            print(f"Rows returned: {len(rows)}")
            return elapsed_time
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    return None

def test_complex_update():
    """Test performance of a complex UPDATE query"""
    print("\n" + "=" * 60)
    print("Testing complex UPDATE query performance...")
    print("=" * 60)
    print("This may take a while...")
    sql = """
    UPDATE bookings.boarding_passes 
    SET ticket_no = ticket_no, 
        flight_id = flight_id, 
        boarding_no = boarding_no, 
        seat_no = seat_no;
    """
    conn = get_connection()
    if conn:
        try:
            start_time = time.time()
            with conn.cursor() as cur:
                cur.execute(sql)
                conn.commit()
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            print(f"UPDATE query executed in {elapsed_time:.2f} ms ({elapsed_time/1000:.2f} seconds)")
            return elapsed_time
        except Error as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    return None

# ---------- Connection Testing Functions ----------

def test_connections(max_connections_to_test=5):
    """Test how many connections can be established"""
    print("\n" + "=" * 60)
    print(f"Testing connection limits (attempting {max_connections_to_test} connections)...")
    print("=" * 60)
    
    connections = []
    successful = 0
    failed = 0
    
    for i in range(max_connections_to_test):
        conn = get_connection()
        if conn:
            connections.append(conn)
            successful += 1
            print(f"Connection {i+1}: SUCCESS")
        else:
            failed += 1
            print(f"Connection {i+1}: FAILED")
    
    print(f"\nResults: {successful} successful, {failed} failed")
    
    # Close all connections
    for conn in connections:
        try:
            conn.close()
        except:
            pass
    
    return successful, failed

# ---------- Log Viewing Functions ----------

def get_log_directory_path():
    """Get the path to PostgreSQL log directory"""
    log_dir = check_log_directory()
    if log_dir:
        # log_directory is usually relative to data directory
        # On macOS with Homebrew, it's often in /usr/local/var/postgres or similar
        # This is a simplified approach - you may need to adjust based on your setup
        return log_dir
    return None

def view_recent_logs(log_file_path=None, lines=50):
    """View recent log entries"""
    print("\n" + "=" * 60)
    print("Viewing recent log entries...")
    print("=" * 60)
    
    if log_file_path and Path(log_file_path).exists():
        try:
            with open(log_file_path, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                print(f"\nLast {len(recent_lines)} lines from {log_file_path}:")
                print("-" * 60)
                for line in recent_lines:
                    print(line.rstrip())
        except Exception as e:
            print(f"Error reading log file: {e}")
    else:
        print("Log file path not provided or file does not exist.")
        print("To view logs manually:")
        print("1. Find your PostgreSQL data directory")
        print("2. Navigate to the 'log' subdirectory")
        print("3. Open the most recent postgresql-YYYY-MM-DD-*.log file")

# ---------- Configuration Recommendations ----------

def print_configuration_recommendations():
    """Print recommendations for optimal PostgreSQL configuration"""
    print("\n" + "=" * 60)
    print("PostgreSQL Configuration Recommendations")
    print("=" * 60)
    print("""
For optimal performance, consider these settings in postgresql.conf:

1. max_connections: 100 (or higher based on your needs)
   - Current default: 100
   - Allows more concurrent connections

2. shared_buffers: 128MB - 256MB (or 25% of RAM for dedicated servers)
   - Current default: 128MB
   - Memory used for caching data

3. work_mem: 4MB - 16MB
   - Current default: 4MB
   - Memory for sorting and hash operations

4. maintenance_work_mem: 64MB - 256MB
   - Current default: 64MB
   - Memory for maintenance operations (VACUUM, CREATE INDEX, etc.)

5. logging_collector: on
   - Enables logging to files
   - Useful for troubleshooting

Note: Changes to postgresql.conf require a server restart to take effect.
    """)

# ---------- Main Troubleshooting Workflow ----------

def run_troubleshooting_suite():
    """Run a complete troubleshooting suite"""
    print("=" * 60)
    print("PostgreSQL Troubleshooting Suite")
    print("=" * 60)
    
    # Check current configuration
    print("\n[STEP 1] Checking Current Configuration")
    print("-" * 60)
    max_conn = check_max_connections()
    shared_buf = check_shared_buffers()
    work_m = check_work_mem()
    maint_work_m = check_maintenance_work_mem()
    logging = check_logging_collector()
    
    # Test performance
    print("\n[STEP 2] Testing Query Performance")
    print("-" * 60)
    simple_time = test_simple_query()
    complex_time = test_complex_update()
    
    # Test connections
    print("\n[STEP 3] Testing Connection Limits")
    print("-" * 60)
    successful, failed = test_connections(5)
    
    # Print recommendations
    print_configuration_recommendations()
    
    # Summary
    print("\n" + "=" * 60)
    print("Troubleshooting Summary")
    print("=" * 60)
    print(f"Max Connections: {max_conn}")
    print(f"Shared Buffers: {shared_buf}")
    print(f"Work Memory: {work_m}")
    print(f"Maintenance Work Memory: {maint_work_m}")
    print(f"Logging Collector: {logging}")
    print(f"\nSimple Query Time: {simple_time:.2f} ms" if simple_time else "Simple Query: FAILED")
    print(f"Complex Update Time: {complex_time:.2f} ms ({complex_time/1000:.2f} seconds)" if complex_time else "Complex Update: FAILED")
    print(f"Connection Test: {successful} successful, {failed} failed")
    
    if failed > 0:
        print("\nWARNING: Some connections failed. Check max_connections setting.")
    if complex_time and complex_time > 30000:  # More than 30 seconds
        print("\nWARNING: Complex query took a long time. Consider optimizing configuration.")

def run_lab_workflow():
    """
    Run the complete lab workflow as described in the instructions:
    Exercise 2: Enable error logging
    Exercise 3: Test performance
    Exercise 4: Troubleshoot and fix issues
    Exercise 5: Verify fixes
    """
    print("=" * 60)
    print("PostgreSQL Troubleshooting Lab Workflow")
    print("=" * 60)
    
    # Exercise 2: Enable Error Logging
    print("\n" + "=" * 60)
    print("EXERCISE 2: Enable Error Logging")
    print("=" * 60)
    print("\n[Task A] Checking logging_collector status...")
    current_logging = check_logging_collector()
    
    if current_logging != "on":
        print("\n[Task A] Enabling logging_collector...")
        conf_path = find_postgresql_conf()
        if conf_path:
            enable_logging_collector(conf_path)
            print("\nNOTE: You must restart PostgreSQL for this change to take effect.")
        else:
            print("Could not find postgresql.conf. Please enable logging manually.")
    else:
        print("Logging collector is already enabled.")
    
    print("\n[Task B] Checking log directory...")
    log_dir = check_log_directory()
    
    # Exercise 3: Test Performance
    print("\n" + "=" * 60)
    print("EXERCISE 3: Test Server Performance")
    print("=" * 60)
    print("\n[Task B] Testing query performance...")
    simple_time = test_simple_query()
    complex_time = test_complex_update()
    
    print("\n[Task B] Testing connection limits...")
    successful, failed = test_connections(5)
    
    if failed > 0:
        print("\n" + "=" * 60)
        print("EXERCISE 4: Troubleshoot Connection Issues")
        print("=" * 60)
        print("\n[Task A] Diagnosing issue...")
        print("Some connections failed. This is likely due to max_connections being too low.")
        current_max = check_max_connections()
        
        print("\n[Task B] Applying fixes...")
        conf_path = find_postgresql_conf()
        if conf_path:
            print("\nApplying recommended configuration fixes:")
            apply_lab_fixes(conf_path)
            print("\nNOTE: You must restart PostgreSQL for these changes to take effect.")
        else:
            print("Could not find postgresql.conf. Please apply fixes manually.")
    else:
        print("All connections succeeded. No issues detected.")
    
    # Exercise 5: Verify fixes (after restart)
    print("\n" + "=" * 60)
    print("EXERCISE 5: Verify Fixes (After Restart)")
    print("=" * 60)
    print("\nAfter restarting PostgreSQL, run this script again with 'performance' command")
    print("to verify that the fixes improved performance.")
    
    print("\n" + "=" * 60)
    print("Lab Workflow Complete")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart PostgreSQL server")
    print("2. Run: python3 postgresql_troubleshooting.py performance")
    print("3. Run: python3 postgresql_troubleshooting.py connections")
    print("4. Compare results with previous run")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "config":
            check_max_connections()
            check_shared_buffers()
            check_work_mem()
            check_maintenance_work_mem()
            check_logging_collector()
        elif command == "performance":
            test_simple_query()
            test_complex_update()
        elif command == "connections":
            test_connections(5)
        elif command == "logs":
            if len(sys.argv) > 2:
                view_recent_logs(sys.argv[2])
            else:
                view_recent_logs()
        elif command == "all":
            run_troubleshooting_suite()
        elif command == "enable-logging":
            if len(sys.argv) > 2:
                enable_logging_collector(sys.argv[2])
            else:
                enable_logging_collector()
        elif command == "fix-config":
            if len(sys.argv) > 2:
                apply_lab_fixes(sys.argv[2])
            else:
                apply_lab_fixes()
        elif command == "find-conf":
            conf_path = find_postgresql_conf()
            if conf_path:
                print(f"Found postgresql.conf at: {conf_path}")
            else:
                print("Could not find postgresql.conf")
        elif command == "lab":
            run_lab_workflow()
        else:
            print(f"Unknown command: {command}")
            print("\nAvailable commands:")
            print("  config         - Check configuration parameters")
            print("  performance    - Test query performance")
            print("  connections    - Test connection limits")
            print("  logs [path]    - View recent logs")
            print("  enable-logging [path] - Enable logging_collector in postgresql.conf")
            print("  fix-config [path]     - Apply lab configuration fixes")
            print("  find-conf            - Find postgresql.conf location")
            print("  lab                  - Run complete lab workflow")
            print("  all                  - Run complete troubleshooting suite")
    else:
        # Run complete suite by default
        run_troubleshooting_suite()

