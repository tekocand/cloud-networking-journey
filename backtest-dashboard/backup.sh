#!/bin/bash
# Auto-backup script for backtest-dashboard

REPO_DIR="/home/openclaw/.openclaw/workspace/backtest-dashboard"
LOG_FILE="/home/openclaw/.openclaw/workspace/backtest-dashboard/.backup.log"

# Ensure git uses the token for HTTPS
export GIT_CONFIG_GLOBAL="/home/openclaw/.openclaw/workspace/backtest-dashboard/.gitconfig"

cd "$REPO_DIR" || exit 1

# Check if there are changes to commit
if git diff --quiet && git diff --staged --quiet; then
    echo "$(date): No changes to backup" >> "$LOG_FILE"
    exit 0
fi

# Add all changes
git add .

# Commit with timestamp
COMMIT_MSG="Auto-backup: $(date '+%Y-%m-%d %H:%M')"
git commit -m "$COMMIT_MSG"

# Push to GitHub
if git push origin main; then
    echo "$(date): Backup successful" >> "$LOG_FILE"
else
    echo "$(date): Backup failed" >> "$LOG_FILE"
    exit 1
fi
