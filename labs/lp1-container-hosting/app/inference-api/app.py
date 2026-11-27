"""inference-api: the lab's main container. Standard library only, so ACR builds take seconds.

GET  /         -> version, host name and where it looks for the model server
GET  /health   -> 200 "ok"
POST /predict  -> sends {"text": ...} to the model server and returns its answer

Port: --port, else the PORT variable, else 5000. Binds to 0.0.0.0 (binding to localhost is a classic
"container starts but every request fails" bug).
"""
import argparse
import json
import os
import socket
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "v1")
MODEL_URL = os.environ.get("MODEL_URL", "http://localhost:11434/generate")


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        if self.path == "/":
            return self._send(200, {"app": "inference-api", "version": VERSION,
                                    "host": socket.gethostname(), "model_url": MODEL_URL})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/predict":
            return self._send(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        try:
            text = json.loads(self.rfile.read(length) or b"{}").get("text", "")
        except json.JSONDecodeError:
            return self._send(400, {"error": "send JSON like {\"text\": \"hello\"}"})
        req = urllib.request.Request(MODEL_URL, data=json.dumps({"prompt": text}).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                answer = json.loads(r.read())
        except (urllib.error.URLError, OSError) as e:
            return self._send(503, {"error": f"model server unreachable at {MODEL_URL}", "detail": str(e)})
        self._send(200, {"version": VERSION, "model": answer.get("model"), "output": answer.get("output")})

    def log_message(self, fmt, *args):  # one line per request on stdout, so `az webapp log tail` shows it
        print(f"inference-api {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", "5000")))
    port = p.parse_args().port
    print(f"inference-api {VERSION} listening on 0.0.0.0:{port}, model server at {MODEL_URL}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
