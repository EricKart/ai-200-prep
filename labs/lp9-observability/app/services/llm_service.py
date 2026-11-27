"""Service 3 of 3: a fake LLM API (cloud role "rag-pipeline.llm-service").

It behaves like a real model endpoint on a bad day, depending on the `scenario` sent:
  normal      -> answers in 0.3-0.7 s
  slow-llm    -> answers in about 5.5 s        (latency bottleneck)
  rate-limit  -> first call gets HTTP 429      (token rate limiting), the retry succeeds
No custom code for telemetry: Flask auto-instrumentation records every call.
"""
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from telemetry import flush_telemetry, setup_telemetry  # noqa: E402

log = setup_telemetry()

from flask import Flask, jsonify, request  # noqa: E402

app = Flask(__name__)
seen_rate_limit = set()


@app.post("/v1/chat")
def chat():
    data = request.get_json()
    scenario = data.get("scenario", "normal")
    if scenario == "rate-limit" and data["request_id"] not in seen_rate_limit:
        seen_rate_limit.add(data["request_id"])
        log.warning("Token rate limit hit, returning 429")
        return jsonify(error="Too Many Requests: token rate limit exceeded"), 429, {"Retry-After": "1"}
    time.sleep(5.5 if scenario == "slow-llm" else random.uniform(0.3, 0.7))
    return jsonify(answer="Open Settings > Security > Reset password.",
                   usage={"completion_tokens": random.randint(40, 120)})


@app.post("/flush")
def flush():
    flush_telemetry()
    return "flushed"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5003")))
