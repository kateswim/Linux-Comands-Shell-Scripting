# Shell Scripts and Python - Complete Guide

## What is a Shell Script?

A **shell script** (`.sh` file) is a text file containing commands that would normally be typed in a terminal. It's like a recipe that tells the computer what commands to run in sequence.

### Why Use Shell Scripts?

1. **Direct System Access**: Can run system commands directly (`mysqldump`, `gzip`, `find`)
2. **No Dependencies**: Doesn't need Python libraries - uses OS tools
3. **Fast**: Minimal overhead, executes quickly
4. **Standard Tool**: Industry standard for automation
5. **Cron Compatible**: Easy to schedule with cron jobs

### Example Shell Script:
```bash
#!/bin/sh
# This is a shell script
echo "Hello World"
mysqldump world > backup.sql
gzip backup.sql
```

---

## Why Run Shell Scripts from Python?

### You might want to do this because:

1. **Python has better error handling** - Can catch and handle errors better
2. **Python has better logic** - Can add conditions, loops, user input
3. **Python can process results** - Can read output, parse data, make decisions
4. **Python can schedule** - Can use Python schedulers (like `schedule` library)
5. **Python can integrate** - Can combine with other Python code

### Example: Why not just use terminal?

**Terminal (manual):**
```bash
$ ./sqlbackup.sh
# You have to manually check if it worked
# You have to manually list backups
# You have to manually delete old ones
```

**Python (automated):**
```python
# Run backup
run_shell_script("sqlbackup.sh")

# Check if it worked
if success:
    # List backups
    show_backups()
    # Delete old ones automatically
    delete_old_backups()
```

---

## How Python Runs Shell Scripts

### Method 1: Using `subprocess.run()` (Recommended)

```python
import subprocess

# Run a shell script
result = subprocess.run(
    ["./sqlbackup.sh"],      # Command to run
    capture_output=True,      # Capture output
    text=True                 # Return text (not bytes)
)

print(result.stdout)  # Print output
print(result.returncode)  # 0 = success, non-zero = error
```

**What happens:**
1. Python calls the operating system
2. OS finds the shell script
3. OS runs it using `/bin/sh` (from the `#!/bin/sh` line)
4. Python captures the output
5. Python returns the result

### Method 2: Using `os.system()` (Simple but less control)

```python
import os

# Run shell script
exit_code = os.system("./sqlbackup.sh")
# Returns 0 if successful
```

### Method 3: Using `subprocess.Popen()` (Advanced)

```python
import subprocess

# Run script and get real-time output
process = subprocess.Popen(
    ["./sqlbackup.sh"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Read output line by line
for line in process.stdout:
    print(line)
```

---

## Complete Example: Running Shell Script from Python

```python
#!/usr/bin/env python3
import subprocess
from pathlib import Path

def run_backup_script():
    """Run the sqlbackup.sh shell script from Python"""
    
    script_path = Path("sqlbackup.sh")
    
    # Make sure it's executable
    os.chmod(script_path, 0o755)
    
    # Run it
    result = subprocess.run(
        [str(script_path)],
        capture_output=True,
        text=True
    )
    
    # Check results
    if result.returncode == 0:
        print("Backup successful!")
        print(result.stdout)
        return True
    else:
        print("Backup failed!")
        print(result.stderr)
        return False

# Run it
run_backup_script()
```

---

## What Happens When Python Runs a Shell Script?

```
┌─────────────┐
│   Python    │
│   Script    │
└──────┬──────┘
       │ subprocess.run(["./sqlbackup.sh"])
       │
       ▼
┌─────────────┐
│  Operating  │
│   System    │
└──────┬──────┘
       │ Finds sqlbackup.sh
       │ Reads #!/bin/sh
       │
       ▼
┌─────────────┐
│  /bin/sh    │
│  Interpreter│
└──────┬──────┘
       │ Executes commands in script
       │ (mysqldump, gzip, etc.)
       │
       ▼
┌─────────────┐
│   MySQL     │
│  Database   │
└─────────────┘
```

---

## Key Concepts

### 1. **Shell Script is NOT Python Code**
- Shell scripts use shell syntax (`bash`/`sh`)
- Python uses Python syntax
- They are different languages!

### 2. **Python Executes Shell Scripts**
- Python doesn't "understand" shell scripts
- Python asks the OS to run them
- OS uses shell interpreter to execute

### 3. **Why Both Work Together**
- Shell scripts: Great for system commands
- Python: Great for logic and error handling
- Together: Best of both worlds!

---

## Real-World Use Cases

### 1. **Automated Backups with Python Logic**
```python
def automated_backup():
    # Run shell script
    success = run_shell_script("sqlbackup.sh")
    
    if success:
        # Python logic: Check backup size
        backups = list_backups()
        total_size = sum(b.size for b in backups)
        
        if total_size > 10_000_000_000:  # 10GB
            # Python logic: Delete oldest
            delete_oldest_backup()
        
        # Python logic: Send notification
        send_email("Backup completed!")
```

### 2. **Scheduled Backups**
```python
import schedule
import time

def backup_job():
    run_shell_script("sqlbackup.sh")

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(backup_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. **Backup with User Interface**
```python
def backup_with_ui():
    print("Starting backup...")
    result = run_shell_script("sqlbackup.sh")
    
    if result:
        backups = list_backups()
        print(f"Backup complete! Total backups: {len(backups)}")
    else:
        print("Backup failed! Check errors above.")
```

---

## Comparison: Terminal vs Python

| Task | Terminal | Python |
|------|----------|--------|
| **Run script** | `./sqlbackup.sh` | `subprocess.run(["./sqlbackup.sh"])` |
| **Check result** | Manual check | `if result.returncode == 0:` |
| **Process output** | Manual | `result.stdout` |
| **Error handling** | Basic | Try/except blocks |
| **Automation** | Cron jobs | Python schedulers |
| **Logic** | Limited | Full Python power |

---

## Summary

### What is a Shell Script?
- A file with terminal commands
- Executed by shell interpreter (`/bin/sh`)
- Great for system operations

### Why Run from Python?
- Better error handling
- More logic and control
- Can process results
- Can integrate with other Python code

### How Does It Work?
1. Python calls `subprocess.run()`
2. OS finds and executes the shell script
3. Shell interpreter runs the commands
4. Python captures and processes the output

### When to Use What?
- **Shell script alone**: Simple, one-time tasks
- **Python + Shell script**: Complex logic, automation, error handling
- **Python only**: When you don't need system commands

---

## Your Backup Automation Script

I've created `backup_automation.py` that:
1. ✅ Runs your shell script from Python
2. ✅ Lists all backups
3. ✅ Deletes all backups (with confirmation)
4. ✅ Deletes old backups automatically
5. ✅ Shows you how it all works

**Try it:**
```bash
python3 backup_automation.py
```

Or run specific commands:
```bash
python3 backup_automation.py backup    # Run backup
python3 backup_automation.py list      # List backups
python3 backup_automation.py cleanup   # Delete old backups
```

