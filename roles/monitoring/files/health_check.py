#!/usr/bin/env python3
import argparse
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


def check_running(interface):
    try:
        subprocess.check_output(f"ip link show {interface} up", shell=True, stderr=subprocess.DEVNULL)
        return True
    except:
        return False


class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        interface = self.server.interface
        running = check_running(interface)
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


def get_args():
    parser = argparse.ArgumentParser(description="wireguard health check")
    parser.add_argument("--port", default=80, type=int, help="server port")
    parser.add_argument("--interface", default="wg0", help="wireguard network interface")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    
    server = HTTPServer(('', args.port), CustomRequestHandler)
    server.interface = args.interface
    server.serve_forever()


if __name__ == "__main__":
    main()
