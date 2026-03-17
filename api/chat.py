import json
import os
import urllib.request
import urllib.error
from datetime import datetime
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
        body_bytes = self.rfile.read(length)

        try:
            body = json.loads(body_bytes)
        except Exception:
            self.send_response(400)
            self._headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": {"message": "Body JSON invalido"}}).encode())
            return

        today = datetime.utcnow().strftime("%d/%m/%Y")

        if "messages" in body and body["messages"]:
            last = body["messages"][-1]
            if last.get("role") == "user":
                last["content"] = f"[Fecha actual: {today}]\n\n{last['content']}"

        body["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]
        body["max_tokens"] = 1024

        payload = json.dumps(body).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "web-search-2025-03-05"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=55) as resp:
                result = resp.read()

            data = json.loads(result)
            text_content = ""
            if "content" in data:
                for block in data["content"]:
                    if block.get("type") == "text":
                        text_content += block.get("text", "")

            simplified = {"content": [{"type": "text", "text": text_content}]}
            self.send_response(200)
            self._headers()
            self.end_headers()
            self.wfile.write(json.dumps(simplified).encode())

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
