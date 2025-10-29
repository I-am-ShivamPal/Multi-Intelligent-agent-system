#!/usr/bin/env python3
"""Simple HTTP endpoints for MCP integration."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from core.mcp_bridge import mcp_bridge

class MCPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''<!DOCTYPE html>
<html><head><title>MCP Endpoints</title></head>
<body>
<h1>MCP Integration Endpoints</h1>
<ul>
<li><a href="/mcp_outbox">GET /mcp_outbox</a> - Get messages from bus</li>
<li><a href="/health">GET /health</a> - Health check</li>
<li>POST /mcp_inbox - Send messages to bus</li>
</ul>
</body></html>'''
            self.wfile.write(html.encode())
            
        elif self.path == '/mcp_outbox':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            messages = mcp_bridge.get_outbox_messages()
            self.wfile.write(json.dumps(messages).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/mcp_inbox':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                message = json.loads(post_data.decode())
                mcp_bridge.add_inbox_message(message)
                mcp_bridge.process_mcp_inbox()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "received"}).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def start_mcp_server(port=8080):
    """Start MCP endpoint server."""
    server = HTTPServer(('localhost', port), MCPHandler)
    print(f"🌐 MCP Endpoints running on http://localhost:{port}")
    print("  GET  /mcp_outbox - Get messages from bus")
    print("  POST /mcp_inbox  - Send messages to bus")
    print("  GET  /health     - Health check")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 MCP server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_mcp_server()