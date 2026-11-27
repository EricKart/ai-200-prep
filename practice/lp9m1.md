# Practice: LP9 · M1 Instrument an app with OpenTelemetry

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp9m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-9/instrument-app-opentelemetry)

## 1. `lp9m1-001`

Which observability pillar shows where in a multi-service request the time is spent?

- **A.** Distributed tracing
- **B.** Metrics over time
- **C.** Alert rules
- **D.** Logs of each event

<details><summary>💡 Hint</summary>

Metrics show trends and logs show detail. The pillar that follows one request across services is the third one.

</details>

<details><summary>✅ Answer</summary>

**A.** Distributed tracing

- A: Correct. Traces show the sequence and timing of operations across services.
- B: Metrics show that something changed, in aggregate.
- C: Alerts aren't one of the three pillars.
- D: Logs explain why a specific operation behaved as it did.

Metrics: something changed. Traces: where. Logs: why.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 2. `lp9m1-002`

Which standard does OpenTelemetry use to propagate trace context over HTTP?

- **A.** OAuth 2.0 bearer tokens
- **B.** The AMQP 1.0 protocol
- **C.** The CloudEvents v1.0 schema
- **D.** W3C TraceContext

<details><summary>💡 Hint</summary>

Trace context travels in a header defined by a web standards body.

</details>

<details><summary>✅ Answer</summary>

**D.** W3C TraceContext

- A: OAuth tokens are for authorization.
- B: AMQP is a messaging protocol.
- C: CloudEvents is an event schema.
- D: Correct. The traceparent header carries the trace and parent span IDs.

traceparent: version-traceId-parentSpanId-flags.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 3. `lp9m1-003`

In Application Insights, which field corresponds to the OpenTelemetry trace ID?

- **A.** customDimensions
- **B.** cloud_RoleName
- **C.** operation_Id
- **D.** itemCount

<details><summary>💡 Hint</summary>

Application Insights uses its own name for the ID that ties a whole request together.

</details>

<details><summary>✅ Answer</summary>

**C.** operation_Id

- A: customDimensions holds span attributes.
- B: cloud_RoleName identifies the service.
- C: Correct. operation_Id links all telemetry in one distributed trace.
- D: itemCount relates to sampling counts, not trace identity.

Join tables on operation_Id to follow one request.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 4. `lp9m1-004`

Given `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, what is `00f067aa0ba902b7`?

- **A.** The trace ID for the request
- **B.** The trace flags (sampled)
- **C.** The format version number
- **D.** The calling (parent) span ID

<details><summary>💡 Hint</summary>

The header has four parts. Count which part this is.

</details>

<details><summary>✅ Answer</summary>

**D.** The calling (parent) span ID

- A: The trace ID is the 32-character second field.
- B: Flags are the last field (01 = sampled).
- C: Version is the first field (00).
- D: Correct. The third field is the 16-hex-character parent span ID.

The receiver creates a span with the same trace ID and this span as parent.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 5. `lp9m1-005`

Match each OpenTelemetry span kind to the Application Insights table it lands in.

Choices: **requests** · **dependencies**

- SpanKind.SERVER
- SpanKind.CONSUMER
- SpanKind.CLIENT
- SpanKind.INTERNAL

<details><summary>💡 Hint</summary>

Server spans become requests. Client and internal spans become dependencies.

</details>

<details><summary>✅ Answer</summary>

- SpanKind.SERVER → **requests**. Incoming requests map to requests.
- SpanKind.CONSUMER → **requests**. Processing a queued message maps to requests.
- SpanKind.CLIENT → **dependencies**. Outgoing calls map to dependencies.
- SpanKind.INTERNAL → **dependencies**. Internal operations map to dependencies.

SERVER and CONSUMER → requests; CLIENT, INTERNAL, PRODUCER → dependencies.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 6. `lp9m1-006`

For each statement, select Yes if the statement is true. Otherwise, select No. A team instruments a RAG pipeline with OpenTelemetry and exports to Application Insights.

| Statement | Yes / No |
|---|---|
| Switching to a different OpenTelemetry-compatible backend would require re-instrumenting the code. | ☐ |
| The trace ID in a traceparent header is 16 hexadecimal characters. | ☐ |
| Attributes set with span.set_attribute() appear in customDimensions. | ☐ |
| Without context propagation, each service creates its own independent trace. | ☐ |

<details><summary>💡 Hint</summary>

Think about context propagation, span identity, and where custom attributes end up.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Switching to a different OpenTelemetry-compatible backend would require re-instrumenting the code. | No | Instrument once; change exporters, not instrumentation. |
| The trace ID in a traceparent header is 16 hexadecimal characters. | No | The trace ID is 32 hex characters; the parent span ID is 16. |
| Attributes set with span.set_attribute() appear in customDimensions. | Yes | Span attributes map to customDimensions. |
| Without context propagation, each service creates its own independent trace. | Yes | Propagation is what links spans across services. |

Vendor-neutral instrumentation plus W3C propagation yields one correlated trace.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 7. `lp9m1-007`

An HTTP framework instrumentation library records incoming requests without any code from you. Which OpenTelemetry component sends that telemetry on to Application Insights?

- **A.** The instrumentation library
- **B.** Context propagation
- **C.** The API
- **D.** An exporter

<details><summary>💡 Hint</summary>

OpenTelemetry has APIs, SDKs, instrumentation libraries, and one more part that ships data out.

</details>

<details><summary>✅ Answer</summary>

**D.** An exporter

- A: Instrumentation libraries capture telemetry from frameworks. Exporters transmit it.
- B: Propagation carries trace IDs between services. It doesn't send data to a backend.
- C: The API defines the interfaces for creating telemetry. It doesn't send data anywhere.
- D: Correct. Exporters serialize and send collected telemetry to a backend such as Azure Monitor.

OpenTelemetry components: APIs (interfaces), SDKs (processing, batching, sampling), instrumentation libraries (automatic capture), and exporters (send telemetry to backends). The Azure Monitor Distro bundles them.

📘 Source: [Explore OpenTelemetry and its role in observability](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/2-explore-opentelemetry-observability)

</details>

## 8. `lp9m1-008`

Which call initializes OpenTelemetry tracing, metrics and logging to Application Insights in a Python app?

- **A.** span.set_attribute()
- **B.** logging.basicConfig()
- **C.** trace.get_tracer("rag")
- **D.** configure_azure_monitor()

<details><summary>💡 Hint</summary>

The Azure Monitor Distro has one function that sets everything up.

</details>

<details><summary>✅ Answer</summary>

**D.** configure_azure_monitor()

- A: That sets a span attribute.
- B: That configures standard logging only.
- C: get_tracer gets a tracer after configuration.
- D: Correct. Call it once at startup to configure all three providers.

pip install azure-monitor-opentelemetry, then configure_azure_monitor().

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 9. `lp9m1-009`

Which environment variable should hold the Application Insights connection string in production?

- **A.** APPLICATIONINSIGHTS_CONNECTION_STRING
- **B.** OTEL_SERVICE_NAME with the endpoint
- **C.** AzureWebJobsStorage with the string
- **D.** OTEL_TRACES_SAMPLER with the key

<details><summary>💡 Hint</summary>

Production configuration shouldn't live in code. Which environment variable does the Distro read?

</details>

<details><summary>✅ Answer</summary>

**A.** APPLICATIONINSIGHTS_CONNECTION_STRING

- A: Correct. The Distro picks it up automatically and keeps it out of source code.
- B: That sets the service name.
- C: That's the Functions runtime storage setting.
- D: That chooses the sampler.

Environment variable is recommended; code-based configuration is least recommended.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 10. `lp9m1-010`

For each statement, select Yes if the statement is true. Otherwise, select No. A Flask app calls an embeddings API with the requests library and queries PostgreSQL with psycopg2, after configure_azure_monitor().

| Statement | Yes / No |
|---|---|
| Incoming Flask requests are captured as server spans automatically. | ☐ |
| The embeddings API calls need hand-written spans to appear as dependencies. | ☐ |
| psycopg2 queries appear as dependency spans automatically. | ☐ |
| Log lines from logging.getLogger() need a separate exporter to reach Application Insights. | ☐ |

<details><summary>💡 Hint</summary>

The Distro instruments common libraries automatically. Think about requests and the web framework.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Incoming Flask requests are captured as server spans automatically. | Yes | Flask/Django/FastAPI instrumentation is included. |
| The embeddings API calls need hand-written spans to appear as dependencies. | No | The requests instrumentation captures them as client spans. |
| psycopg2 queries appear as dependency spans automatically. | Yes | psycopg2 is instrumented. |
| Log lines from logging.getLogger() need a separate exporter to reach Application Insights. | No | Standard logging is integrated automatically. |

The Distro auto-collects common HTTP, web, database, Azure SDK and logging telemetry.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 11. `lp9m1-011`

Four RAG services send telemetry to one Application Insights resource but appear as one node on the Application Map. What should you set?

- **A.** A separate connection string for each service
- **B.** A higher sampling ratio on every service
- **C.** SpanKind.SERVER set on every single span
- **D.** A distinct service.name per service

<details><summary>💡 Hint</summary>

Each service needs its own cloud role name, which comes from resource attributes.

</details>

<details><summary>✅ Answer</summary>

**D.** A distinct service.name per service

- A: They can share a resource; the role name is what separates nodes.
- B: Sampling doesn't affect role names.
- C: Span kind doesn't name services.
- D: Correct. Cloud role name comes from service.namespace + service.name.

For example rag-pipeline.embedding-service, rag-pipeline.llm-orchestrator.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 12. `lp9m1-012`

APPLICATIONINSIGHTS_CONNECTION_STRING points to the production resource, but code also passes a connection string for a test resource. Where does telemetry go?

- **A.** Neither, because the conflict disables export
- **B.** The test resource, because code takes priority
- **C.** Both resources
- **D.** The production resource, because environment variables win

<details><summary>💡 Hint</summary>

When code and environment disagree about the connection string, one of them wins.

</details>

<details><summary>✅ Answer</summary>

**B.** The test resource, because code takes priority

- A: Conflicts don't disable export.
- B: Correct. For the connection string, code has the highest priority.
- C: The exporter sends to one connection string.
- D: That precedence applies to sampling settings, not the connection string.

Connection string precedence: code first, then environment variable.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 13. `lp9m1-013`

You can't change the embedding service's code, but it must appear on the Application Map as rag-pipeline.embedding-service. How can you set this?

- **A.** Rename the container image to embedding-service
- **B.** Set OTEL_SERVICE_NAME=embedding-service and OTEL_RESOURCE_ATTRIBUTES=service.namespace=rag-pipeline
- **C.** Create a second Application Insights resource for the service
- **D.** Set APPLICATIONINSIGHTS_ROLE=rag-pipeline.embedding-service

<details><summary>💡 Hint</summary>

Cloud role name comes from two OpenTelemetry resource attributes, which have standard environment variables.

</details>

<details><summary>✅ Answer</summary>

**B.** Set OTEL_SERVICE_NAME=embedding-service and OTEL_RESOURCE_ATTRIBUTES=service.namespace=rag-pipeline

- A: The image name doesn't set OpenTelemetry resource attributes.
- B: Correct. Resource attributes can be set through environment variables, and the cloud role name is namespace.name.
- C: Separate resources don't set the role name, and they split the Application Map.
- D: That isn't a variable the Distro reads for the role name.

The cloud role name is service.namespace + service.name. Set them in code (Resource.create) or with OTEL_SERVICE_NAME and OTEL_RESOURCE_ATTRIBUTES.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 14. `lp9m1-014`

A Flask RAG service uses psycopg2 for PostgreSQL. After you add the Azure Monitor OpenTelemetry Distro, where do the database queries appear?

- **A.** As log records in the traces table
- **B.** They don't appear unless you write a custom span for each query
- **C.** As dependency spans, with the database name and execution time
- **D.** As request spans, because they run inside a request

<details><summary>💡 Hint</summary>

Outgoing calls from your service, including database calls, all land in one table.

</details>

<details><summary>✅ Answer</summary>

**C.** As dependency spans, with the database name and execution time

- A: Queries are captured as spans, not as log records.
- B: psycopg2 is one of the libraries the Distro instruments automatically.
- C: Correct. The Distro's psycopg2 instrumentation records queries as dependencies.
- D: Requests are incoming HTTP calls. Outgoing database calls are dependencies.

The Distro instruments requests, urllib/urllib3, Flask/Django/FastAPI, psycopg2 and Azure SDK calls. Outgoing calls such as database queries become dependency spans.

📘 Source: [Add the OpenTelemetry SDK to an application](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/3-add-opentelemetry-sdk)

</details>

## 15. `lp9m1-015`

If you don't specify a kind when starting a span, which SpanKind is used?

- **A.** INTERNAL
- **B.** SERVER
- **C.** CLIENT
- **D.** CONSUMER

<details><summary>💡 Hint</summary>

Without a kind, OpenTelemetry assumes the span is work inside the service, not a call in or out.

</details>

<details><summary>✅ Answer</summary>

**A.** INTERNAL

- A: Correct. INTERNAL is the default and maps to dependencies.
- B: SERVER represents incoming requests.
- C: CLIENT represents outgoing calls.
- D: CONSUMER represents processing async messages.

Set kind explicitly for outgoing calls (CLIENT) or message processing (CONSUMER).

📘 Source: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

</details>

## 16. `lp9m1-016`

You want to record which model and how many tokens each LLM call used, so you can filter traces later. What should you add?

- **A.** Separate log files per model
- **B.** Span attributes like llm.model
- **C.** A new tracer for each request
- **D.** Resource attributes such as service.name

<details><summary>💡 Hint</summary>

Custom key-value context on a span is searchable later.

</details>

<details><summary>✅ Answer</summary>

**B.** Span attributes like llm.model

- A: Attributes keep the data on the span for querying.
- B: Correct. Span attributes describe a specific operation and land in customDimensions.
- C: One tracer per component is enough.
- D: Resource attributes describe the whole service.

Use namespaced keys for searchability.

📘 Source: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

</details>

## 17. `lp9m1-017`

A span named CallLlmApi represents an outgoing HTTP call to Azure OpenAI. Which kind should it use?

- **A.** SpanKind.CLIENT
- **B.** SpanKind.INTERNAL
- **C.** SpanKind.SERVER
- **D.** SpanKind.CONSUMER

<details><summary>💡 Hint</summary>

The span represents an outgoing call to another service.

</details>

<details><summary>✅ Answer</summary>

**A.** SpanKind.CLIENT

- A: Correct. Outgoing calls are CLIENT spans (dependencies).
- B: INTERNAL is for operations that don't cross process boundaries.
- C: SERVER is for incoming requests.
- D: CONSUMER is for processing async messages.

Correct span kinds put telemetry in the right tables.

📘 Source: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

</details>

## 18. `lp9m1-018`

For each statement, select Yes if the statement is true. Otherwise, select No. Code inside `with tracer.start_as_current_span("GenerateEmbedding") as span:` catches a timeout exception and returns a fallback.

| Statement | Yes / No |
|---|---|
| The SDK still records the exception automatically. | ☐ |
| Calling span.record_exception() and span.set_status() marks the span as failed with details. | ☐ |
| A span started inside this block becomes its child automatically. | ☐ |
| The span must be ended manually with span.end(). | ☐ |

<details><summary>💡 Hint</summary>

A caught exception is invisible to the SDK unless you record it. Child spans nest by themselves, and the with block ends the span.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The SDK still records the exception automatically. | No | Only exceptions that propagate out are recorded automatically. |
| Calling span.record_exception() and span.set_status() marks the span as failed with details. | Yes | Do this when you handle the exception yourself. |
| A span started inside this block becomes its child automatically. | Yes | The SDK tracks the current span via context variables. |
| The span must be ended manually with span.end(). | No | The context manager ends it when the block exits. |

start_as_current_span handles lifetime and parentage; caught errors need explicit recording.

📘 Source: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

</details>

## 19. `lp9m1-019`

A request handler creates nested spans for a RAG query. Put them in the order they start in the waterfall.

- CallLlm
- GenerateEmbedding
- ProcessQuery (root)
- SearchVectorIndex

<details><summary>💡 Hint</summary>

The parent starts first, then its children in the order the code runs.

</details>

<details><summary>✅ Answer</summary>

1. ProcessQuery (root)
2. GenerateEmbedding
3. SearchVectorIndex
4. CallLlm

Nested context managers create parent-child spans; the waterfall shows each step's share of the time.

📘 Source: [Configure spans and traces](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/4-configure-spans-traces)

</details>

## 20. `lp9m1-020`

Code sets sampling_ratio=0.5, but OTEL_TRACES_SAMPLER=microsoft.fixed_percentage and OTEL_TRACES_SAMPLER_ARG=0.1 are set on the host. What sampling applies?

- **A.** About 50%, because code takes precedence
- **B.** About 10%; env vars win for sampling
- **C.** About 60%, the two ratios combined
- **D.** No sampling, because the settings conflict

<details><summary>💡 Hint</summary>

For sampling, environment variables take precedence over code.

</details>

<details><summary>✅ Answer</summary>

**B.** About 10%; env vars win for sampling

- A: Code wins for the connection string, not sampling.
- B: Correct. For sampling, environment variables win.
- C: They don't add up.
- D: Conflicts don't disable sampling.

Adjust sampling via environment variables without redeploying.

📘 Source: [Export telemetry to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/5-export-telemetry-azure-monitor)

</details>

## 21. `lp9m1-021`

In Application Insights, which table receives log records emitted through Python's logging module?

- **A.** customMetrics
- **B.** dependencies
- **C.** traces
- **D.** requests

<details><summary>💡 Hint</summary>

Log records aren't requests or dependencies. Their table name sounds like another pillar of observability.

</details>

<details><summary>✅ Answer</summary>

**C.** traces

- A: customMetrics holds custom metric values.
- B: dependencies holds client, internal and producer spans.
- C: Correct. Log records land in the traces table.
- D: requests holds server and consumer spans.

Despite its name, the traces table holds logs; spans go to requests and dependencies.

📘 Source: [Export telemetry to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/5-export-telemetry-azure-monitor)

</details>

## 22. `lp9m1-022`

For each statement, select Yes if the statement is true. Otherwise, select No. A high-volume service uses fixed-percentage sampling at 0.05.

| Statement | Yes / No |
|---|---|
| Custom metrics are also sampled at 5%. | ☐ |
| Counts in the Performance and Failures panes become less precise at lower ratios. | ☐ |
| If the network drops, telemetry is cached and retried for up to 48 hours. | ☐ |
| Without any sampler configured, the Python Distro sends 100% of traces. | ☐ |

<details><summary>💡 Hint</summary>

Sampling applies to traces, not custom metrics. Lower ratios make counts less precise. Think about offline caching and the default.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Custom metrics are also sampled at 5%. | No | Metrics are never sampled. |
| Counts in the Performance and Failures panes become less precise at lower ratios. | Yes | Fewer data points make adjusted counts less precise. |
| If the network drops, telemetry is cached and retried for up to 48 hours. | Yes | Offline storage with retries is built in. |
| Without any sampler configured, the Python Distro sends 100% of traces. | No | The default is RateLimitedSampler. |

Sample traces for cost; metrics stay complete; offline storage covers outages.

📘 Source: [Export telemetry to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/5-export-telemetry-azure-monitor)

</details>

## 23. `lp9m1-023`

In the traceparent header 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01, what does the final 01 mean?

- **A.** The trace-context format version
- **B.** The trace is sampled
- **C.** The request had one retry
- **D.** It's the first span in the trace

<details><summary>💡 Hint</summary>

The four fields are version, trace ID, parent span ID, and one set of flags.

</details>

<details><summary>✅ Answer</summary>

**B.** The trace is sampled

- A: The version is the first field, 00.
- B: Correct. The trace flags field 01 indicates the trace is sampled.
- C: Retries aren't recorded in traceparent.
- D: Span position isn't encoded in the header.

traceparent fields: version (00), 32-hex trace ID, 16-hex parent span ID, and trace flags (01 = sampled).

📘 Source: [Export telemetry to Azure Monitor](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/5-export-telemetry-azure-monitor)

</details>

## 24. `lp9m1-024`

Which KQL query links slow requests to the dependency calls inside the same distributed trace?

- **A.** requests | union dependencies | order by duration desc
- **B.** requests | where duration > 5000 | join kind=inner (dependencies) on cloud_RoleName
- **C.** requests | where duration > 5000 | join kind=inner (dependencies) on operation_Id
- **D.** dependencies | summarize avg(duration) by name

<details><summary>💡 Hint</summary>

Requests and dependencies are joined on the field that identifies the whole operation.

</details>

<details><summary>✅ Answer</summary>

**C.** requests | where duration > 5000 | join kind=inner (dependencies) on operation_Id

- A: union stacks rows; it doesn't relate them by trace.
- B: cloud_RoleName joins by service, not by trace.
- C: Correct. operation_Id identifies the trace shared by all its spans.
- D: This summarizes dependencies without linking them to requests.

operation_Id corresponds to the OpenTelemetry trace ID.

📘 Source: [Debug distributed flows with trace data](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/6-debug-distributed-flows-trace-data)

</details>

## 25. `lp9m1-025`

Vector search spans are usually 100 ms but sometimes 5 s, mostly right after quiet periods, with normal result counts. What pattern does this suggest?

- **A.** Embedding model timeouts
- **B.** Vector search cold starts
- **C.** Context window overflow
- **D.** LLM token rate limiting

<details><summary>💡 Hint</summary>

Slow only after idle periods, with normal results, suggests something warming up.

</details>

<details><summary>✅ Answer</summary>

**B.** Vector search cold starts

- A: These are search spans, not embedding spans.
- B: Correct. Slow clusters after inactivity, with normal search.result_count, point to cold starts.
- C: Overflow appears on prompt assembly or LLM errors.
- D: Rate limiting shows 429s on LLM calls.

Attributes like search.result_count separate cold starts from genuinely heavy queries.

📘 Source: [Debug distributed flows with trace data](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/6-debug-distributed-flows-trace-data)

</details>

## 26. `lp9m1-026`

For each statement, select Yes if the statement is true. Otherwise, select No. A team investigates slow RAG responses in Application Insights.

| Statement | Yes / No |
|---|---|
| The Application Map shows average response time and failure rate per service node. | ☐ |
| Selecting a span in the transaction view shows its custom attributes. | ☐ |
| Custom span attributes can be queried as regular table columns without customDimensions. | ☐ |

<details><summary>💡 Hint</summary>

Look at the waterfall, the dependency durations, and whether attributes explain the slow spans.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The Application Map shows average response time and failure rate per service node. | Yes | Nodes and edges show key metrics. |
| Selecting a span in the transaction view shows its custom attributes. | Yes | Span details include attributes and exceptions. |
| Custom span attributes can be queried as regular table columns without customDimensions. | No | They live in customDimensions; extract them with KQL. |

Map → waterfall → KQL is the usual drill-down.

📘 Source: [Debug distributed flows with trace data](https://learn.microsoft.com/en-us/training/modules/instrument-app-opentelemetry/6-debug-distributed-flows-trace-data)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
