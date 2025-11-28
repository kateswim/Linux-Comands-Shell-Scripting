#!/usr/bin/env python3
"""
Automated MySQL Backup Script
This Python script can:
1. Run shell scripts from Python
2. Automate database backups
3. Delete old backups
4. Schedule backups (with cron or Python scheduler)
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

# Configuration
BACKUP_SCRIPT = Path(__file__).parent / "sqlbackup.sh"
BACKUP_FOLDER = Path.home() / "backups"

def run_shell_script(script_path):
    """
    Run a shell script from Python using subprocess
    
    This demonstrates how Python can execute shell scripts (.sh files)
    """
    script_path = Path(script_path)
    
    if not script_path.exists():
        print(f"Error: Script {script_path} not found!")
        return False
    
    # Make sure script is executable
    os.chmod(script_path, 0o755)  # rwxr-xr-x permissions
    
    try:
        print(f"Running shell script: {script_path}")
        print("-" * 60)
        
        # Run the shell script
        # subprocess.run() executes the shell script
        result = subprocess.run(
            [str(script_path)],  # Command to run
            capture_output=True,  # Capture output
            text=True,            # Return text (not bytes)
            check=False          # Don't raise exception on error
        )
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print(f"\nScript executed successfully!")
            return True
        else:
            print(f"\nScript failed with exit code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"Error running script: {e}")
        return False

def list_backups():
    """List all backup files"""
    if not BACKUP_FOLDER.exists():
        print(f"Backup folder {BACKUP_FOLDER} does not exist.")
        return []
    
    backups = list(BACKUP_FOLDER.glob("*.gz"))
    backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return backups

def show_backups():
    """Display all backup files"""
    backups = list_backups()
    
    if not backups:
        print("No backups found.")
        return
    
    print(f"\nFound {len(backups)} backup(s):")
    print("-" * 60)
    for i, backup in enumerate(backups, 1):
        size = backup.stat().st_size / (1024 * 1024)  # Size in MB
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name}")
        print(f"   Size: {size:.2f} MB")
        print(f"   Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

def delete_all_backups():
    """Delete all backup files"""
    backups = list_backups()
    
    if not backups:
        print("No backups to delete.")
        return True
    
    print(f"WARNING: This will delete {len(backups)} backup file(s)!")
    response = input("Are you sure? (yes/no): ")
    
    if response.lower() == 'yes':
        deleted = 0
        for backup in backups:
            try:
                backup.unlink()  # Delete file
                print(f"Deleted: {backup.name}")
                deleted += 1
            except Exception as e:
                print(f"Error deleting {backup.name}: {e}")
        
        print(f"\nDeleted {deleted} backup file(s).")
        return True
    else:
        print("Cancelled.")
        return False

def delete_old_backups(days=30):
    """Delete backups older than specified days"""
    backups = list_backups()
    
    if not backups:
        print("No backups found.")
        return
    
    cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
    deleted = 0
    
    for backup in backups:
        if backup.stat().st_mtime < cutoff_time:
            try:
                backup.unlink()
                print(f"Deleted old backup: {backup.name}")
                deleted += 1
            except Exception as e:
                print(f"Error deleting {backup.name}: {e}")
    
    if deleted > 0:
        print(f"\nDeleted {deleted} old backup(s).")
    else:
        print("No old backups to delete.")

def main():
    """Main menu"""
    print("=" * 60)
    print("MySQL Backup Automation Script")
    print("=" * 60)
    print("\nThis script demonstrates:")
    print("1. How Python can run shell scripts (.sh files)")
    print("2. How to automate database backups")
    print("3. How to manage backup files from Python")
    print("\nOptions:")
    print("1. Run backup script (execute sqlbackup.sh)")
    print("2. List all backups")
    print("3. Delete all backups")
    print("4. Delete old backups (older than 30 days)")
    print("5. Run backup and show results")
    print("0. Exit")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "1":
        run_shell_script(BACKUP_SCRIPT)
    elif choice == "2":
        show_backups()
    elif choice == "3":
        delete_all_backups()
    elif choice == "4":
        delete_old_backups(30)
    elif choice == "5":
        print("\nRunning backup...")
        if run_shell_script(BACKUP_SCRIPT):
            print("\n" + "=" * 60)
            show_backups()
    elif choice == "0":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    # You can also run the backup directly from command line
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "backup":
            run_shell_script(BACKUP_SCRIPT)
        elif command == "list":
            show_backups()
        elif command == "delete-all":
            delete_all_backups()
        elif command == "cleanup":
            delete_old_backups(30)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: backup, list, delete-all, cleanup")
    else:
        # Interactive mode
        while True:
            main()
            print("\n" + "=" * 60)
            continue_choice = input("Continue? (yes/no): ")
            if continue_choice.lower() != 'yes':
                break

