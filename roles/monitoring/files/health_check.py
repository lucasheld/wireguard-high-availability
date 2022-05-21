#!/usr/bin/env python3
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

INTERFACE_NAME = "wg0"
PORT = 80


def check_running():
    try:
        subprocess.check_output(f"ip link show {INTERFACE_NAME} up", shell=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False


class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        running = check_running()
        if running:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"healthy")
        else:
            self.send_response(503)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"unhealthy")


server = HTTPServer(('', PORT), CustomRequestHandler)
server.serve_forever()
