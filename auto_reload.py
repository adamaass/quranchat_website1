#!/usr/bin/env python3
import http.server
import socketserver
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server
        
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(('.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg')):
            print(f"File changed: {event.src_path}")
            print("Server is running. Refresh your browser to see changes.")

def start_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Auto-reload is active. Changes will be detected automatically.")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()

def main():
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Set up file watching
    event_handler = ReloadHandler(None)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nServer stopped.")
    
    observer.join()

if __name__ == "__main__":
    main() 