# LP9 · M1: Instrument an app with OpenTelemetry

> **Learning path 9:** Observe and troubleshoot apps on Azure · **Skill area 4:** Secure, monitor and troubleshoot solutions · about 79 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-9/instrument-app-opentelemetry)

OpenTelemetry gives every request a trace that follows it across services. You'll learn the concepts, add the Azure Monitor Distro, create custom spans, configure sampling and logs, and read traces in Application Insights.

**In this lesson**

1. [Explore OpenTelemetry and its role in observability](#explore-opentelemetry-and-its-role-in-observability)
2. [Add the OpenTelemetry SDK to an application](#add-the-opentelemetry-sdk-to-an-application)
3. [Configure spans and traces](#configure-spans-and-traces)
4. [Export telemetry to Azure Monitor](#export-telemetry-to-azure-monitor)
5. [Debug distributed flows with trace data](#debug-distributed-flows-with-trace-data)

## Explore OpenTelemetry and its role in observability

📘 Microsoft Learn: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

**Metrics** tell you something changed, **traces** tell you where, **logs** tell you why. A trace is one request's journey; each step is a **span** with timing and labels. A `traceparent` header carries the trace ID from service to service so the steps join up.

**Key facts**

- Three pillars: **distributed tracing** (path and timing of a request), **metrics** (aggregates: counts, error rates, percentiles), **logs** (detailed timestamped events).
- **OpenTelemetry**: vendor-neutral, open-source framework under the **CNCF**. Components: **APIs**, **SDKs** (batching, sampling, resource detection), **instrumentation libraries** (automatic capture), **exporters**. Instrument once, export anywhere (Azure Monitor, Jaeger, Prometheus, Grafana).
- **Azure Monitor OpenTelemetry Distro** bundles the SDK, Azure Monitor exporter, common instrumentation and Azure resource detectors.
- A **trace** = tree of **spans**. Span: trace ID (shared), span ID, parent span ID (none for the root), name, start/end, **attributes**, status.
- **Context propagation** uses **W3C TraceContext**: header `traceparent: 00-<32-hex trace ID>-<16-hex parent span ID>-01` (version, trace ID, parent span ID, flags; 01 = sampled).
- Mapping to Application Insights: SERVER and **CONSUMER** spans → **Request**; CLIENT, **INTERNAL** and PRODUCER → **Dependency**; trace ID → **operation_Id**; span attributes → **customDimensions**.

| OpenTelemetry | Application Insights |
|---|---|
| Server / Consumer span | Request (requests table) |
| Client / Internal / Producer span | Dependency (dependencies table) |
| Trace ID | operation_Id |
| Span attributes | customDimensions |

> [!WARNING]
> **Exam traps**
>
> - CONSUMER spans are Requests; INTERNAL spans are Dependencies.
> - traceparent's 2nd field is the trace ID; 3rd is the parent span ID.

## Add the OpenTelemetry SDK to an application

📘 Microsoft Learn: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

`pip install azure-monitor-opentelemetry`, call `configure_azure_monitor()` once at startup, and HTTP calls, web requests, PostgreSQL queries, Azure SDK calls and Python logs are captured automatically. Give each service a **service.name** so it shows up as its own box on the Application Map.

**Key facts**

- **Autoinstrumentation**: no code changes (App Service, Functions, VMs); quick but limited control. **Manual (SDK)**: custom spans, attributes, sampling; preferred for AI-specific operations. The **Azure Monitor OpenTelemetry Distro** is the recommended SDK approach.
- Install `azure-monitor-opentelemetry`; call `configure_azure_monitor()` **once at startup**; it sets up tracer, meter and logger providers.
- Automatic Python collection: **requests**, **urllib/urllib3** (client spans), **Flask/Django/FastAPI** (server spans), **psycopg2** (PostgreSQL dependencies), **Azure SDK** calls, and the standard **logging** module.
- Connection string (ingestion endpoint + instrumentation key): **APPLICATIONINSIGHTS_CONNECTION_STRING** environment variable (recommended for production) or passed in code (least recommended). If both are set, **code takes priority**.
- **Cloud role name** = `service.namespace` + `service.name` (falls back to service.name alone); `service.instance.id` distinguishes instances. Without distinct names all services appear as one Application Map node.
- Env vars: `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES="service.namespace=rag-pipeline,service.instance.id=…"`.

> [!WARNING]
> **Exam traps**
>
> - Connection string set in code overrides the environment variable.
> - Same service.name for every service = one node on the Application Map.

## Configure spans and traces

📘 Microsoft Learn: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

Automatic capture can't see your own steps (assemble prompt, score results). Wrap them in **custom spans**, add **attributes** like the model name or token count, choose the right **span kind**, and nest spans so the trace looks like a tree of your pipeline.

**Key facts**

- `tracer = trace.get_tracer("name")` after configure_azure_monitor() (no extra registration in Python). `with tracer.start_as_current_span("GenerateEmbedding") as span:` starts and ends the span automatically.
- **Resource attributes** describe the service (set once); **span attributes** describe one operation (`span.set_attribute("embedding.model", …)`; string, number or boolean) → customDimensions.
- Name attributes with namespaced keys (`search.result_count`, `llm.token_count`), not generic ones like value or data.
- Span kinds: SERVER (requests), CLIENT (dependencies), **INTERNAL** (dependencies; **default**), PRODUCER (dependencies), CONSUMER (requests). Set with `kind=SpanKind.CLIENT`.
- Exceptions escaping the with block are recorded and set the status to error. If you catch them, call `span.record_exception()` and `span.set_status(Status(StatusCode.ERROR, …))`.
- Nesting: start a span inside another with block; the SDK sets the parent automatically (context variables). The end-to-end transaction view shows a waterfall.

> [!WARNING]
> **Exam traps**
>
> - Default span kind is INTERNAL.
> - Caught exceptions aren't recorded unless you record them.

## Export telemetry to Azure Monitor

📘 Microsoft Learn: [Export telemetry to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/5-export-telemetry-azure-monitor)

The Distro sends telemetry **straight** to Application Insights. **Sampling** keeps costs down by sending a share of traces (metrics are never sampled). If the network drops, telemetry is **cached locally** and retried for up to 48 hours. Check it's arriving with Live Metrics or a quick KQL query.

**Key facts**

- Default **direct export** to the ingestion endpoint (no intermediary); the alternative **OpenTelemetry Collector** adds central sampling, transformation and multi-backend routing.
- Tables: requests (SERVER, CONSUMER), dependencies (CLIENT, INTERNAL, PRODUCER), **traces** (log records), **exceptions**, **customMetrics**.
- Sampling: **fixed-percentage** (`sampling_ratio` 0.0–1.0) or **rate-limited** (`traces_per_second`). Env vars: `OTEL_TRACES_SAMPLER=microsoft.fixed_percentage` / `microsoft.rate_limited` with `OTEL_TRACES_SAMPLER_ARG`. For sampling, **environment variables take precedence** over code. Default sampler: **RateLimitedSampler**. Start around **5% (0.05)**.
- Sampling applies to traces only; **metrics are never sampled**; logs of unsampled traces are dropped by default.
- Offline storage: cached locally and retried for up to **48 hours**; default under the temp directory; override with `storage_directory`; `disable_offline_storage=True` not recommended.
- Verify: Overview pane, **Live Metrics** (near real time; enabled by default), or KQL on requests.

> [!WARNING]
> **Exam traps**
>
> - Sampling: env vars beat code. Connection string: code beats env vars.
> - Logs go to the traces table, not requests.

## Debug distributed flows with trace data

📘 Microsoft Learn: [Debug distributed flows with trace data](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/6-debug-distributed-flows-trace-data)

Start with the **Application Map** to see which service is slow or failing, open the **end-to-end transaction** waterfall to see which step ate the time, and use **KQL** to ask precise questions, joining tables on **operation_Id**.

**Key facts**

- **Application Map**: a node per cloud role (service.name), edges for calls; average response time, request count, failure rate. Select nodes or edges to drill in.
- **End-to-end transaction details**: waterfall of all spans in one trace, from the Performance pane, Failures pane or Application Map; selecting a span shows attributes and exceptions.
- KQL tables: requests, dependencies, traces, exceptions; all share **operation_Id** (= trace ID).
- Examples: `requests | where duration > 3000 | summarize count(), avg(duration) by cloud_RoleName`; `requests | join kind=inner (dependencies) on operation_Id`; `extend tokenCount = toint(customDimensions["embedding.token_count"])`.
- AI patterns: **embedding timeouts** (long or failed spans; check embedding.model), **vector search cold starts** (slow clusters after inactivity; check search.result_count), **LLM rate limiting** (429s or long retries; llm.prompt_tokens/response_tokens), **context window overflow** (llm.prompt_tokens near the limit).
- Proactive: alerts on operation latency, **workbooks** for dashboards, correlate traces with custom metrics.

> [!WARNING]
> **Exam traps**
>
> - Join requests and dependencies on operation_Id.
> - Custom attributes live in customDimensions; cast with toint()/tostring().

## Check yourself

- **Practice questions:** [lp9m1 on GitHub](../../practice/lp9m1.md), or [on the site](https://aryantripathi.dev/ai-200/lp-9/instrument-app-opentelemetry) with hints and saved progress
- **Cheat sheet:** [Learning path 9](../cheatsheets/lp9.md)
- **Microsoft Learn exercise:** [Instrument an app with the OpenTelemetry SDK](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/7-exercise-instrument-app-opentelemetry)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
