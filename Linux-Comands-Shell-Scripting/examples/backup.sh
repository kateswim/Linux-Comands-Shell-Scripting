#!/bin/bash
# Example: Automatic backup script
# Why Bash? - Easy to use system commands like 'tar', 'date', 'find'

# Create backup with timestamp
BACKUP_DIR="/tmp/backups"
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz" /path/to/files
echo "Backup completed!"

