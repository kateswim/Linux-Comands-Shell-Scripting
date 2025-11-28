# Step-by-Step Explanation of sqlbackup.sh

## Why `.sh` Extension?

The `.sh` extension stands for **"shell script"**. It tells the operating system and developers that this is a shell script file that should be executed by a shell interpreter (like `sh` or `bash`).

**Why use `.sh`?**
- **Standard convention**: Everyone knows it's a shell script
- **Auto-detection**: Some editors automatically enable syntax highlighting
- **Clarity**: Makes it obvious how to run the file
- **System integration**: Helps with file associations and permissions

---

## Line-by-Line Explanation

### **Line 1: `#!/bin/sh`**
```sh
#!/bin/sh
```
- **What it does**: This is called a "shebang" or "hashbang"
- **Purpose**: Tells the system which program should execute this script
- **`/bin/sh`**: Points to the shell interpreter (sh = shell)
- **Why needed**: When you run `./sqlbackup.sh`, the system knows to use `/bin/sh` to run it

---

### **Line 2: Comment**
```sh
# The above line tells the interpreter this code needs to be run as a shell script.
```
- **What it does**: Just a comment (ignored by the computer)
- **Purpose**: Explains what the shebang does (for humans reading the code)

---

### **Line 4-5: Database Variable**
```sh
# Set the database name to a variable. 
DATABASE='world'
```
- **Line 4**: Comment explaining what we're doing
- **Line 5**: Creates a variable named `DATABASE` and sets it to `'world'`
- **Why use a variable**: Makes it easy to change the database name in one place
- **Usage**: Later we'll use `$DATABASE` to reference this value

---

### **Line 7-8: User Message**
```sh
# This will be printed on to the screen. In the case of cron job, it will be printed to the logs.
echo "Pulling Database: This may take a few minutes"
```
- **Line 7**: Comment explaining the purpose
- **Line 8**: `echo` command prints text to the screen
- **Purpose**: Informs the user that the backup process has started
- **Cron jobs**: If run automatically, this message goes to log files

---

### **Line 10-14: Backup Folder Location**
```sh
# Set the folder where the database backup will be stored
# For macOS, use a directory in your home folder or current directory
backupfolder="$HOME/backups"
# Alternative: use current directory
# backupfolder="$(pwd)/backups"
```
- **Line 10-11**: Comments explaining the purpose
- **Line 12**: Sets `backupfolder` variable to `$HOME/backups`
  - `$HOME` = your home directory (e.g., `/Users/katehoncharova`)
  - Full path becomes: `/Users/katehoncharova/backups`
- **Line 13-14**: Commented alternative - uses current directory instead
  - `$(pwd)` = "print working directory" (gets current folder)

---

### **Line 16-17: Create Backup Folder**
```sh
# Create backup folder if it doesn't exist
mkdir -p "$backupfolder"
```
- **Line 16**: Comment
- **Line 17**: Creates the backup directory
  - `mkdir` = make directory command
  - `-p` = "parents" flag - creates parent directories if needed, and doesn't error if folder already exists
  - `"$backupfolder"` = uses the variable we defined (with quotes for safety)

---

### **Line 19-20: Retention Period**
```sh
# Number of days to store the backup 
keep_day=30
```
- **Line 19**: Comment
- **Line 20**: Sets how long to keep backups (30 days)
- **Purpose**: Used later to delete old backups automatically

---

### **Line 22-23: File Names with Timestamps**
```sh
sqlfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).sql
zipfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).gz
```
- **Line 22**: Creates filename for SQL backup
  - `$backupfolder/` = directory path
  - `all-database-` = prefix
  - `$(date +%d-%m-%Y_%H-%M-%S)` = current date/time in format: `27-11-2024_21-30-45`
  - `.sql` = file extension
  - **Example result**: `/Users/katehoncharova/backups/all-database-27-11-2024_21-30-45.sql`

- **Line 23**: Creates filename for compressed backup
  - Same as above but with `.gz` extension (gzip compressed)
  - **Example result**: `/Users/katehoncharova/backups/all-database-27-11-2024_21-30-45.gz`

---

### **Line 25-29: Create Database Backup**
```sh
# Create a backup
# Note: Add -u for username and -p for password if needed
# Example: mysqldump -u root -p$PASSWORD $DATABASE > $sqlfile

if mysqldump $DATABASE > $sqlfile ; then
```
- **Line 25-27**: Comments with instructions for adding authentication
- **Line 29**: **IF statement** that runs `mysqldump`
  - `mysqldump` = MySQL command to export database
  - `$DATABASE` = uses our variable (becomes `world`)
  - `>` = redirects output to a file
  - `$sqlfile` = the filename we created
  - `; then` = if command succeeds, execute what follows

**What happens**: Creates a SQL file with all database data

---

### **Line 30: Success Message**
```sh
   echo 'Sql dump created'
```
- Prints confirmation that SQL file was created
- Only runs if `mysqldump` succeeded (because of `if...then`)

---

### **Line 31-37: Compress the Backup**
```sh
    # Compress backup 
    if gzip -c $sqlfile > $zipfile; then
        echo 'The backup was successfully compressed'
    else
        echo 'Error compressing backup! Backup was not created!' 
        exit 1
    fi
```
- **Line 31**: Comment
- **Line 32**: **IF statement** to compress the file
  - `gzip` = compression tool
  - `-c` = write output to stdout (so we can redirect it)
  - `$sqlfile` = input file (the SQL backup)
  - `>` = redirect to file
  - `$zipfile` = output file (compressed version)
- **Line 33**: Success message if compression works
- **Line 34-36**: **ELSE block** - runs if compression fails
  - Prints error message
  - `exit 1` = stops script with error code 1

---

### **Line 38: Delete Original SQL File**
```sh
    rm $sqlfile 
```
- `rm` = remove/delete command
- `$sqlfile` = the uncompressed SQL file
- **Why**: We only need the compressed version, saves disk space

---

### **Line 39-42: Handle Backup Failure**
```sh
else
   echo 'mysqldump returned non-zero code. No backup was created!' 
   exit 1
fi
```
- **Line 39**: **ELSE** - runs if `mysqldump` failed (from line 29)
- **Line 40**: Error message explaining backup failed
- **Line 41**: `exit 1` = stops script with error code
- **Line 42**: `fi` = closes the IF statement from line 29

---

### **Line 44-45: Delete Old Backups**
```sh
# Delete old backups 
find $backupfolder -name "*.gz" -mtime +$keep_day -delete
```
- **Line 44**: Comment
- **Line 45**: Finds and deletes old backup files
  - `find` = search for files command
  - `$backupfolder` = where to search
  - `-name "*.gz"` = only files ending in `.gz`
  - `-mtime +$keep_day` = files older than 30 days (modified time)
  - `-delete` = delete those files
- **Purpose**: Prevents backup folder from growing too large

---

### **Line 47: Final Success Message**
```sh
echo "Backup completed successfully!"
```
- Prints final confirmation
- Only shows if everything worked correctly

---

## Why the File with Dot at End (`sqlbackup.sh.`)?

The file `sqlbackup.sh.` (with a dot at the end) was likely created by accident. Here's why:

### **Possible Reasons:**
1. **Typo**: Someone typed an extra dot when saving
2. **File system quirk**: Some systems add dots to hidden files
3. **Editor issue**: Some editors add dots to temporary files
4. **Copy/paste error**: Extra character got included

### **Why It's a Problem:**
- **Confusing**: Two files with almost the same name
- **Wrong file might run**: If you type `sqlbackup.sh.` by mistake
- **Not standard**: Shell scripts should end with `.sh`, not `.sh.`

### **Solution:**
- **Delete the old file** (`sqlbackup.sh.`)
- **Use the correct file** (`sqlbackup.sh`)

---

## Summary: Why Shell Scripts (.sh)?

1. **Direct system access**: Can run system commands directly
2. **No dependencies**: Doesn't need Python or other languages
3. **Fast execution**: Minimal overhead
4. **Standard tool**: Industry standard for automation
5. **Cron compatible**: Easy to schedule with cron jobs
6. **Cross-platform**: Works on Linux, macOS, Unix

---

## How the Script Works (Flow):

```
1. Set variables (database name, folder, etc.)
2. Create backup folder if needed
3. Generate filenames with timestamps
4. Run mysqldump → creates SQL file
5. Compress SQL file → creates .gz file
6. Delete uncompressed SQL file
7. Delete backups older than 30 days
8. Print success message
```

If any step fails, the script stops and prints an error message.

