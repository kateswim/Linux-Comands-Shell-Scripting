#!/usr/bin/env python3
"""
Script to download, extract, and import the employees database into MySQL.
Lab: Improving Performance of Slow Queries in MySQL
"""

import subprocess
import sys
import os
from pathlib import Path
import urllib.request
import zipfile

# ---------- Configuration ----------
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # Update if needed
DB_NAME = "employees"

DOWNLOAD_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/datasets/employeesdb.zip"
ZIP_FILE = "employeesdb.zip"
EXTRACT_DIR = "employeesdb"
SQL_FILE = f"{EXTRACT_DIR}/employees.sql"

# ---------- Functions ----------

def download_database(url, filename):
    """Download the employees database zip file."""
    if Path(filename).exists():
        print(f"✅ {filename} already exists, skipping download.")
        return True
    
    print(f"📥 Downloading database from {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def extract_database(zip_file, extract_to):
    """Extract the zip file."""
    if Path(extract_to).exists():
        print(f"✅ {extract_to} already exists, skipping extraction.")
        return True
    
    print(f"📦 Extracting {zip_file}...")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall()
        print(f"✅ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

def create_database(host, port, user, password):
    """Create the employees database if it doesn't exist."""
    print(f"🗄️  Creating database '{DB_NAME}' if it doesn't exist...")
    
    cmd = [
        'mysql',
        '-h', host,
        '-P', port,
        '-u', user,
        '-e', f'CREATE DATABASE IF NOT EXISTS {DB_NAME};'
    ]
    
    env = os.environ.copy()
    if password:
        env['MYSQL_PWD'] = password
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Database '{DB_NAME}' is ready.")
            return True
        else:
            print(f"❌ Error creating database: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Error: mysql command not found!")
        print("   Please install MySQL client: brew install mysql")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def import_sql_file(sql_file, host, port, user, password, db_name):
    """Import the SQL file into MySQL."""
    if not Path(sql_file).exists():
        print(f"❌ Error: {sql_file} not found!")
        return False
    
    print(f"⏳ Importing {sql_file} into database '{db_name}'...")
    print("   This may take 1-2 minutes...")
    
    cmd = [
        'mysql',
        '-h', host,
        '-P', port,
        '-u', user,
        db_name
    ]
    
    env = os.environ.copy()
    if password:
        env['MYSQL_PWD'] = password
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdin=f, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database imported successfully!")
            if result.stdout:
                print("Output:")
                print(result.stdout[:500])  # Print first 500 chars
            return True
        else:
            print(f"❌ Import error: {result.stderr[:500]}")
            return False
    except FileNotFoundError:
        print("❌ Error: mysql command not found!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_import(host, port, user, password, db_name):
    """Verify the database was imported correctly."""
    print(f"\n✔️  Verifying import...")
    
    cmd = [
        'mysql',
        '-h', host,
        '-P', port,
        '-u', user,
        db_name,
        '-e', 'SHOW TABLES;'
    ]
    
    env = os.environ.copy()
    if password:
        env['MYSQL_PWD'] = password
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print("Tables in employees database:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Verification error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ---------- Main ----------

if __name__ == "__main__":
    print("=" * 70)
    print("Employees Database Setup - Hands-on Lab")
    print("=" * 70)
    
    # Check if password needs updating
    if not MYSQL_PASSWORD and len(sys.argv) > 1 and sys.argv[1] != "--help":
        MYSQL_PASSWORD = sys.argv[1]
        print(f"Using provided password.")
    
    print(f"\nConfiguration:")
    print(f"  Host: {MYSQL_HOST}")
    print(f"  Port: {MYSQL_PORT}")
    print(f"  User: {MYSQL_USER}")
    print(f"  Database: {DB_NAME}")
    print()
    
    # Step 1: Download
    if not download_database(DOWNLOAD_URL, ZIP_FILE):
        sys.exit(1)
    
    # Step 2: Extract
    if not extract_database(ZIP_FILE, EXTRACT_DIR):
        sys.exit(1)
    
    # Step 3: Create database
    if not create_database(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD):
        sys.exit(1)
    
    # Step 4: Import
    if not import_sql_file(SQL_FILE, MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, DB_NAME):
        sys.exit(1)
    
    # Step 5: Verify
    if not verify_import(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, DB_NAME):
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"1. Connect to MySQL: mysql -h {MYSQL_HOST} -u {MYSQL_USER} {DB_NAME}")
    print(f"2. Run lab exercises: python3 employees_lab_exercises.py")
    print()
    
    sys.exit(0)
