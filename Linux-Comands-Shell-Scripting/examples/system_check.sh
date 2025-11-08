#!/bin/bash
# Example: System health check
# Why Bash? - Easy access to system commands like 'df', 'free', 'uptime'

# Check disk space
echo "=== Disk Usage ==="
df -h

# Check memory
echo -e "\n=== Memory Usage ==="
free -h 2>/dev/null || vm_stat

# Check uptime
echo -e "\n=== System Uptime ==="
uptime

