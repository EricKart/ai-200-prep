"""model-server: a stand-in for a local model runtime (it listens where Ollama would, on 11434).

POST /generate {"prompt": "..."} -> {"model": "tiny-echo", "output": "..."}
It doesn't run a real model: it counts words and echoes the prompt backwards, which is enough to prove the
main container reached its sidecar over localhost.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._send(200, {"model": "tiny-echo", "status": "ready"})

    def do_POST(self):
        if self.path != "/generate":
            return self._send(404, {"error": "not found"})
        prompt = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}").get("prompt", "")
        self._send(200, {"model": "tiny-echo", "output": f"{len(prompt.split())} words; backwards: {prompt[::-1]}"})

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"model-server {fmt % args}", flush=True)


if __name__ == "__main__":
    print("model-server listening on 0.0.0.0:11434", flush=True)
    ThreadingHTTPServer(("0.0.0.0", 11434), Handler).serve_forever()
