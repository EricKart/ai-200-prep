"""Service 2 of 3: the RAG orchestrator (cloud role "rag-pipeline.llm-orchestrator").

This is where the CUSTOM instrumentation lives (LP9 Module 1, unit 4):
  tracer = trace.get_tracer(...)                       one tracer per component
  with tracer.start_as_current_span("Name") as span:   a timed operation (ends automatically)
  span.set_attribute("embedding.model", ...)           -> customDimensions in Application Insights
  kind=SpanKind.CLIENT                                 -> dependencies table, type "InProc"/HTTP
  span.record_exception(ex) + span.set_status(ERROR)   -> exceptions table + failed span
Nested `with` blocks become parent -> child spans automatically.

Request flow for POST /process:
  [SERVER span from Flask] POST /process
     ├─ GenerateEmbedding     (INTERNAL)
     ├─ SearchVectorIndex     (INTERNAL)  slow "cold start" after 20 s of no searches
     ├─ AssemblePrompt        (INTERNAL)  fails if the prompt is bigger than the context window
     └─ CallLlm               (CLIENT)
           └─ POST /v1/chat   (auto: requests library -> llm-service)
"""
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from telemetry import flush_telemetry, setup_telemetry  # noqa: E402

log = setup_telemetry()

import requests  # noqa: E402
from flask import Flask, jsonify, request  # noqa: E402
from opentelemetry import metrics, trace  # noqa: E402
from opentelemetry.trace import SpanKind, Status, StatusCode  # noqa: E402

app = Flask(__name__)
tracer = trace.get_tracer("llm-orchestrator")
meter = metrics.get_meter("llm-orchestrator")
docs_counter = meter.create_counter("documents_retrieved", description="Documents returned by vector search")

LLM_URL = os.environ.get("LLM_URL", "http://127.0.0.1:5003")
CONTEXT_WINDOW = 128_000
last_search = 0.0


class ContextWindowExceededError(Exception):
    pass


@app.post("/process")
def process():
    global last_search
    data = request.get_json()
    query, scenario = data["q"], data.get("scenario", "normal")
    # The header that carried the trace across the service boundary (W3C TraceContext):
    log.info("traceparent received: %s", request.headers.get("traceparent"))

    # ---- 1. Embedding ---------------------------------------------------------
    with tracer.start_as_current_span("GenerateEmbedding") as span:
        tokens = len(query.split()) * 4
        span.set_attribute("embedding.model", "text-embedding-3-small")
        span.set_attribute("embedding.token_count", tokens)
        time.sleep(random.uniform(0.08, 0.2))
        span.set_attribute("embedding.dimensions", 1536)

    # ---- 2. Vector search (cold start after idle) --------------------------------
    with tracer.start_as_current_span("SearchVectorIndex") as span:
        cold = time.monotonic() - last_search > 20
        span.set_attribute("search.index_name", "product-docs")
        span.set_attribute("search.top_k", 5)
        span.set_attribute("search.cold_start", cold)
        time.sleep(3.5 if cold else random.uniform(0.05, 0.2))
        results = random.randint(3, 5)
        span.set_attribute("search.result_count", results)
        span.set_attribute("search.similarity_threshold", 0.78)
        last_search = time.monotonic()
        docs_counter.add(results, {"index": "product-docs"})

    # ---- 3. Prompt assembly (context window overflow) ----------------------------
    with tracer.start_as_current_span("AssemblePrompt") as span:
        prompt_tokens = 150_000 if scenario == "overflow" else random.randint(900, 2500)
        span.set_attribute("llm.prompt_tokens", prompt_tokens)
        try:
            if prompt_tokens > CONTEXT_WINDOW:
                raise ContextWindowExceededError(f"Prompt has {prompt_tokens} tokens; limit is {CONTEXT_WINDOW}")
            span.set_status(Status(StatusCode.OK))
        except ContextWindowExceededError as ex:
            span.record_exception(ex)
            span.set_status(Status(StatusCode.ERROR, "Prompt exceeds context window"))
            log.error("Context window overflow: %s", ex)
            return jsonify(error=str(ex)), 500

    # ---- 4. LLM call (CLIENT span wrapping a real HTTP call) ---------------------
    with tracer.start_as_current_span("CallLlm", kind=SpanKind.CLIENT) as span:
        span.set_attribute("llm.provider", "azure-openai")
        span.set_attribute("llm.model", "gpt-4o-mini")
        payload = {"q": query, "scenario": scenario, "request_id": random.random()}
        r = requests.post(f"{LLM_URL}/v1/chat", json=payload, timeout=30)
        if r.status_code == 429:
            span.set_attribute("llm.retry_after_429", True)
            log.warning("LLM returned 429, retrying after Retry-After")
            time.sleep(float(r.headers.get("Retry-After", "1")))
            r = requests.post(f"{LLM_URL}/v1/chat", json=payload, timeout=30)
        answer = r.json()
        span.set_attribute("llm.response_tokens", answer["usage"]["completion_tokens"])

    log.info("Answered query with %d documents", results)
    return jsonify(answer=answer["answer"], documents=results, scenario=scenario)


@app.post("/flush")
def flush():
    flush_telemetry()
    return "flushed"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5002")))
