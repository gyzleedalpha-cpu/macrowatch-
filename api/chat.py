import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._headers()
        self.end_headers()

    def do_POST(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            self.send_response(500)
            self._headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": "API key no configurada en Vercel"}}).encode())
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                result = resp.read()
            self.send_response(200)
            self._headers()
            self.end_headers()
            self.wfile.write(result)

        except urllib.error.HTTPError as e:
            error_body = e.read()
            self.send_response(e.code)
            self._headers()
            self.end_headers()
            self.wfile.write(error_body)

        except Exception as e:
            self.send_response(500)
            self._headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": str(e)}}).encode())

    def _headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json")

    def log_message(self, format, *args):
        pass
