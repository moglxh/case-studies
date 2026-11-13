import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ip = sys.argv[1]
mode = sys.argv[2]   # "legit" or "lookalike"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "unknown")
        if mode == "legit":
            self.send_page(200, f"NovaBot official site (served for {host})")
        elif self.path == "/":
            # the "parked domain" behaviour: bounce the visitor onward
            self.send_response(302)
            self.send_header("Location", "/verify")
            self.end_headers()
        elif self.path == "/verify":
            self.send_page(200, f"LAB DEMO: lookalike 'Security Check' page (served for {host}). "
                                "In the real campaign a fake verification prompt appears here. "
                                "This lab shows nothing to run.")
        else:
            self.send_page(404, "not found")

    def send_page(self, code, text):
        body = (text + "\n").encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[{mode}] {self.requestline} Host={self.headers.get('Host')}")

HTTPServer((ip, 8080), Handler).serve_forever()
