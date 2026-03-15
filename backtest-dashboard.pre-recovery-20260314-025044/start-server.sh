#!/usr/bin/env bash
# Simple server starter for backtest-dashboard
PORT=8080
if pgrep -f "python3 -m http.server $PORT" > /dev/null; then
  echo "Dashboard server already running on $PORT"
  exit 0
fi

cd "$(dirname "$0")"
nohup python3 -m http.server $PORT >/dev/null 2>&1 &
echo "Started dashboard server on http://localhost:$PORT"