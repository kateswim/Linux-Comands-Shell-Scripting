# Shell Scripts (.sh) - Why and How to Use Them

## Why Use Shell Scripts (.sh)?

Shell scripts are used for several important reasons:

### 1. **System-Level Operations**
- Direct access to system commands (`mysqldump`, `pg_dump`, `gzip`, `find`)
- No need for Python libraries - uses native OS tools
- Faster execution for simple tasks

### 2. **Automation & Scheduling**
- Perfect for **cron jobs** (scheduled tasks)
- Can run automatically without user interaction
- Lightweight - minimal overhead

### 3. **Database Administration**
- Standard tool for database backups
- Works with any database (MySQL, PostgreSQL, etc.)
- Easy to integrate into backup systems

### 4. **Cross-Platform Compatibility**
- Works on Linux, macOS, and Unix systems
- Can be easily modified for different environments

## How to Run Shell Scripts

### Method 1: Make it Executable and Run Directly
```bash
# Make the script executable (one time only)
chmod +x sqlbackup.sh

# Run it
./sqlbackup.sh
```

### Method 2: Run with Shell Interpreter
```bash
# Run with sh
sh sqlbackup.sh

# Or with bash (if script uses bash features)
bash sqlbackup.sh
```

### Method 3: Run from Any Directory
```bash
# Use full path
/path/to/your/script/sqlbackup.sh

# Or navigate to directory first
cd /path/to/your/script
./sqlbackup.sh
```

## Your Backup Scripts

### MySQL Backup (`sqlbackup.sh`)
- **Location**: `MYSQL/sqlbackup.sh`
- **Database**: `world` (change if needed)
- **Backup Location**: `~/backups/`
- **Usage**:
  ```bash
  cd MYSQL
  ./sqlbackup.sh
  ```

### PostgreSQL Backup (`pgbackup.sh`)
- **Location**: `PostgreSQL/pgbackup.sh`
- **Database**: `demo` (change if needed)
- **Backup Location**: `~/backups/`
- **Usage**:
  ```bash
  cd PostgreSQL
  ./pgbackup.sh
  ```

## Customizing the Scripts

### Change Database Name
Edit the `DATABASE` variable:
```sh
DATABASE='your_database_name'
```

### Change Backup Location
Edit the `backupfolder` variable:
```sh
backupfolder="$HOME/my_backups"  # Home directory
# OR
backupfolder="$(pwd)/backups"     # Current directory
```

### Add Authentication
For MySQL:
```sh
mysqldump -u root -p$PASSWORD $DATABASE > $sqlfile
```

For PostgreSQL:
```sh
pg_dump -U username -W $DATABASE > $sqlfile
```

## Scheduling with Cron (Advanced)

To run backups automatically every day at 2 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 2 * * * /path/to/your/script/sqlbackup.sh >> /path/to/logs/backup.log 2>&1
```

## Troubleshooting

### "Permission denied" Error
```bash
chmod +x sqlbackup.sh
```

### "Command not found" Error
- Make sure MySQL/PostgreSQL tools are installed
- Check if they're in your PATH: `which mysqldump` or `which pg_dump`

### Script Not Found
- Use full path or navigate to script directory first
- Check file name (no typos)

## Shell Script vs Python Script

| Feature | Shell Script (.sh) | Python Script (.py) |
|---------|-------------------|---------------------|
| **Best For** | System tasks, backups | Complex logic, data processing |
| **Speed** | Faster for simple tasks | Slower startup |
| **Dependencies** | None (uses OS tools) | Requires Python + libraries |
| **Readability** | Less readable | More readable |
| **Error Handling** | Basic | Advanced |
| **Database Access** | Command-line tools | Libraries (psycopg2, mysql-connector) |

## Example: Running Your Backup Script

```bash
# Navigate to MySQL directory
cd "/Users/katehoncharova/Documents/GitHub/DataEngineering/Relational Database Administration/MYSQL"

# Run the backup script
./sqlbackup.sh

# Check the backup was created
ls -lh ~/backups/
```

The backup will be:
- Compressed (`.gz` format)
- Named with timestamp: `all-database-DD-MM-YYYY_HH-MM-SS.gz`
- Stored in `~/backups/` folder
- Old backups (>30 days) automatically deleted

