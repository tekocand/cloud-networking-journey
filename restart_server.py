#!/usr/bin/env python3
"""
Restart both HTTP server and Trade API server
"""

import subprocess
import time
import socket
import os
import sys

def is_port_in_use(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('0.0.0.0', port))
        sock.close()
        return result == 0
    except:
        return False

def kill_port(port):
    try:
        subprocess.run(['fuser', '-k', f'{port}/tcp'], capture_output=True)
    except:
        try:
            subprocess.run(['pkill', '-f', f'http.server {port}'], capture_output=True)
        except:
            pass

# Kill existing servers
print("Stopping existing servers...")
kill_port(8080)
kill_port(8081)
time.sleep(1)

# Start HTTP server for static files
print("Starting HTTP server on port 8080...")
subprocess.Popen(
    [sys.executable, '-m', 'http.server', '8080', '--bind', '0.0.0.0'],
    cwd='/home/openclaw/.openclaw/workspace/backtest-dashboard',
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Start Trade API server
print("Starting Trade API server on port 8081...")
subprocess.Popen(
    [sys.executable, 'trade_server.py'],
    cwd='/home/openclaw/.openclaw/workspace/backtest-dashboard',
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(2)

# Verify
http_ok = is_port_in_use(8080)
api_ok = is_port_in_use(8081)

if http_ok and api_ok:
    print("✅ Both servers running!")
    print("   Dashboard: http://0.0.0.0:8080")
    print("   Trade API: http://0.0.0.0:8081")
else:
    if not http_ok:
        print("❌ HTTP server failed to start")
    if not api_ok:
        print("❌ Trade API server failed to start")
