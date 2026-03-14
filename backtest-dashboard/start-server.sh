#!/bin/bash
# Auto-start script for Trading Journal Dashboard

PIDFILE="/tmp/journal-server.pid"
PORT=8080

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Journal server already running (PID: $PID)"
        exit 0
    else
        rm -f "$PIDFILE"
    fi
fi

# Check if port is in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Port $PORT is already in use"
    exit 0
fi

# Start the server
cd /home/openclaw/.openclaw/workspace/backtest-dashboard
nohup python3 server.py > server.log 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PIDFILE"
echo "Journal server started on port $PORT (PID: $SERVER_PID)"
