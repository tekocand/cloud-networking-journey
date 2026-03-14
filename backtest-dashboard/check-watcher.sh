#!/bin/bash
# Check watcher status

REPO_DIR="/home/openclaw/.openclaw/workspace/backtest-dashboard"
PID_FILE="$REPO_DIR/.watcher.pid"
HEARTBEAT_FILE="$REPO_DIR/.watcher.heartbeat"
LOG_FILE="$REPO_DIR/.backup.log"

if [ ! -f "$PID_FILE" ]; then
    echo "❌ Watcher not running (no PID file)"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "❌ Watcher not running (PID $PID is dead)"
    rm -f "$PID_FILE" "$HEARTBEAT_FILE"
    exit 1
fi

# Check heartbeat
if [ -f "$HEARTBEAT_FILE" ]; then
    LAST_HEARTBEAT=$(cat "$HEARTBEAT_FILE")
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_HEARTBEAT))
    
    if [ $DIFF -gt 120 ]; then
        echo "⚠️  Watcher running but stale (no heartbeat for ${DIFF}s)"
        exit 1
    else
        echo "✅ Watcher running (PID: $PID, heartbeat: ${DIFF}s ago)"
    fi
else
    echo "⚠️  Watcher running but no heartbeat file"
fi

# Show last backup
echo ""
echo "Last 3 log entries:"
tail -3 "$LOG_FILE"
