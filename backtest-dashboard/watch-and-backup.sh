#!/bin/bash
# File change watcher for backtest-dashboard
# Backs up automatically when files change

REPO_DIR="/home/openclaw/.openclaw/workspace/backtest-dashboard"
LOG_FILE="$REPO_DIR/.backup.log"
PID_FILE="$REPO_DIR/.watcher.pid"
HEARTBEAT_FILE="$REPO_DIR/.watcher.heartbeat"

cd "$REPO_DIR" || exit 1

# Check if already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "$(date): Watcher already running (PID: $OLD_PID)" >> "$LOG_FILE"
        exit 0
    else
        echo "$(date): Stale PID file found, starting new watcher" >> "$LOG_FILE"
    fi
fi

# Store PID
echo $$ > "$PID_FILE"

echo "$(date): File watcher started (PID: $$)" >> "$LOG_FILE"

# Initial hash of tracked files
get_hash() {
    git status --porcelain 2>/dev/null | md5sum
}

LAST_HASH=$(get_hash)

# Cleanup on exit
trap 'echo "$(date): Watcher stopped" >> "$LOG_FILE"; rm -f "$PID_FILE" "$HEARTBEAT_FILE"; exit 0' INT TERM EXIT

while true; do
    # Update heartbeat
    date +%s > "$HEARTBEAT_FILE"
    
    sleep 30  # Check every 30 seconds
    
    CURRENT_HASH=$(get_hash)
    
    if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
        echo "$(date): Changes detected, backing up..." >> "$LOG_FILE"
        
        git add .
        
        # Only commit if there are staged changes
        if ! git diff --cached --quiet; then
            CHANGED=$(git diff --cached --name-only | head -3 | tr '\n' ', ')
            git commit -m "Auto-backup: Changes in $CHANGED" --quiet
            
            if git push origin main --quiet; then
                echo "$(date): Backup successful" >> "$LOG_FILE"
            else
                echo "$(date): Backup failed" >> "$LOG_FILE"
            fi
        fi
        
        LAST_HASH=$(get_hash)
    fi
done
