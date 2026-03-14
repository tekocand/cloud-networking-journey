#!/usr/bin/env python3
"""
Trading Journal Server - Serves static files and API endpoints
"""

import json
import os
import mimetypes
from http.server import HTTPServer, SimpleHTTPRequestHandler

DATA_DIR = 'data'

class JournalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialize with the current directory as the root
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        # API endpoints
        if self.path.startswith('/api/'):
            endpoint = self.path[5:]  # Remove '/api/'
            filepath = os.path.join(DATA_DIR, f'{endpoint}.json')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            default = '[]' if endpoint in ['trades', 'vision', 'casestudies', 'watchlist'] else '{}'
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(default.encode())
            return
        
        # Static files
        if self.path == '/':
            self.path = '/index.html'
        
        # Get the file path
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.path.lstrip('/'))
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File not found')
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            endpoint = self.path[5:]
            filepath = os.path.join(DATA_DIR, f'{endpoint}.json')
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                # Validate JSON
                json.loads(post_data.decode())
                
                # Save to file
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(post_data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8080):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(('0.0.0.0', port), JournalHandler)
    print(f"🌙 Trading Journal Server running at http://0.0.0.0:{port}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print(f"💾 Data directory: {os.path.join(os.getcwd(), DATA_DIR)}")
    print("")
    print("Available endpoints:")
    print(f"  GET/POST  http://localhost:{port}/api/trades")
    print(f"  GET/POST  http://localhost:{port}/api/journal")
    print(f"  GET/POST  http://localhost:{port}/api/habits")
    print(f"  GET/POST  http://localhost:{port}/api/goals")
    print(f"  GET/POST  http://localhost:{port}/api/vision")
    print(f"  GET/POST  http://localhost:{port}/api/casestudies")
    print(f"  GET/POST  http://localhost:{port}/api/watchlist")
    print(f"  GET/POST  http://localhost:{port}/api/weekly")
    print("")
    print("Press Ctrl+C to stop")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
