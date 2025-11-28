#!/bin/sh
# The above line tells the interpreter this code needs to be run as a shell script.

# Set the database name to a variable. 
DATABASE='world'

# This will be printed on to the screen. In the case of cron job, it will be printed to the logs.
echo "Pulling Database: This may take a few minutes"

# Set the folder where the database backup will be stored
# For macOS, use a directory in your home folder or current directory
backupfolder="$HOME/backups"
# Alternative: use current directory
# backupfolder="$(pwd)/backups"

# Create backup folder if it doesn't exist
mkdir -p "$backupfolder"

# Number of days to store the backup 
keep_day=30

sqlfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).sql
zipfile=$backupfolder/all-database-$(date +%d-%m-%Y_%H-%M-%S).gz

# Create a backup
# Note: Add -u for username and -p for password if needed
# Example: mysqldump -u root -p$PASSWORD $DATABASE > $sqlfile

if mysqldump $DATABASE > $sqlfile ; then
   echo 'Sql dump created'
    # Compress backup 
    if gzip -c $sqlfile > $zipfile; then
        echo 'The backup was successfully compressed'
    else
        echo 'Error compressing backup! Backup was not created!' 
        exit 1
    fi
    rm $sqlfile 
else
   echo 'mysqldump returned non-zero code. No backup was created!' 
   exit 1
fi

# Delete old backups 
find $backupfolder -name "*.gz" -mtime +$keep_day -delete

echo "Backup completed successfully!"

