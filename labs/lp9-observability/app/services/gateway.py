"""Service 1 of 3: the API gateway (cloud role "rag-pipeline.api-gateway").

GET /ask?q=...&scenario=...  -> calls the orchestrator.
No custom spans here at all: Flask and requests are auto-instrumented, so you still get
a SERVER span (requests table) and a CLIENT span (dependencies table), and the
`traceparent` header is added to the outgoing call for you (context propagation).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from telemetry import flush_telemetry, setup_telemetry  # noqa: E402

log = setup_telemetry()           # MUST run before Flask is imported

import requests  # noqa: E402
from flask import Flask, jsonify, request  # noqa: E402
from opentelemetry import trace  # noqa: E402

app = Flask(__name__)
ORCHESTRATOR = os.environ.get("ORCHESTRATOR_URL", "http://127.0.0.1:5002")


@app.get("/ask")
def ask():
    q = request.args.get("q", "How do I reset my password?")
    scenario = request.args.get("scenario", "normal")
    trace_id = format(trace.get_current_span().get_span_context().trace_id, "032x")
    log.info("Gateway received question (scenario=%s)", scenario)
    r = requests.post(f"{ORCHESTRATOR}/process", json={"q": q, "scenario": scenario}, timeout=30)
    body = r.json()
    body["trace_id"] = trace_id   # = operation_Id in Application Insights
    return jsonify(body), r.status_code


@app.post("/flush")
def flush():
    flush_telemetry()
    return "flushed"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5001")))
