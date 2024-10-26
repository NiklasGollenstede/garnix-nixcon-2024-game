import os
import random
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from cowsay import cowsay

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"200 OK")

        elif path.startswith("/add/"):
            try:
                _, _, a, b = path.split("/")
                result = int(a) + int(b)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(result).encode())
            except ValueError:
                self.send_error(400, "Invalid numbers")

        elif path.startswith("/mult/"):
            try:
                _, _, a, b = path.split("/")
                result = int(a) * int(b)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(result).encode())
            except ValueError:
                self.send_error(400, "Invalid numbers")

        elif path.startswith("/cowsay/"):
            message = path[len("/cowsay/"):]
            response = cowsay(message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())

        elif path == "/uuid":
            random_uuid = str(uuid.uuid4())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(random_uuid.encode())

        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), SimpleServer)
    print(f"Server running on port {port}")
    server.serve_forever()