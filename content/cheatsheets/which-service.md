# Which service, setting or command?

> One table for the whole AI-200 syllabus: the need as the exam phrases it, the answer, and what people confuse it with.  
> Practise these at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200).

## Container hosting: ACR and App Service (LP1)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Exact same image on every node | Pull by digest (repo@sha256:…) | Tags (even stable ones) can move |
| Geo-replication, private endpoints, content trust | ACR Premium tier | Basic/Standard lack these |
| Build an image without local Docker | az acr build (quick task) | az acr run runs a command in an existing image |
| Rebuild when the base image is patched | ACR base image trigger | Source code trigger = commits |
| Container listens on 8000 in App Service | WEBSITES_PORT=8000 | Not used by sidecar-enabled apps |
| Files must survive restarts and be shared by instances | WEBSITES_ENABLE_APP_SERVICE_STORAGE=true (/home) | Container file system is ephemeral |
| Value must not swap to production | Slot setting | Normal app settings swap |
| One local helper process per instance, same lifecycle | App Service sidecar | Shared/GPU model → separate service |
| Sidecar call from the main container | `http://localhost:<port>` | Not the container name |

## Azure Container Apps (LP2)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Service reachable only inside the environment | --ingress internal | external = callable from outside |
| Reviewable config as the single source of truth | --yaml (other flags ignored) | az containerapp up is for quick prototypes |
| Map a stored secret to an env var | secretref:`<secret-name>` | Never paste the value in YAML |
| Send 10% of traffic to a new revision | Multiple revision mode + traffic weights | Single revision mode can't split |
| Testers hit one revision via its own URL | Revision label | Traffic weight on latest moves real users |
| Changes that create a new revision | Template: image, env vars, scale rules | Secrets, ingress, traffic = application scope |
| Scale on queue depth, down to zero | KEDA Service Bus/Storage Queue scaler | CPU/memory rules never reach zero |
| WebSockets or gRPC scaling | TCP scale rule | HTTP rule = request concurrency |
| GPU or more than 4 cores / 8 GiB per container | Dedicated workload profile | Consumption max 4 cores / 8 GiB |
| Run AI-generated Python safely | Dynamic sessions: built-in code interpreter | Custom container pool for native binaries |
| Backend calls the session pool API | Azure ContainerApps Session Executor role, audience https://dynamicsessions.io | Users never get the token |

## Azure Kubernetes Service (LP3)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Stable internal name for Pods | ClusterIP Service | LoadBalancer = public IP |
| Public production API | LoadBalancer Service (or ingress controller) | NodePort is for testing |
| Pod stuck Pending: insufficient memory | Lower requests or add nodes | Not an image or app problem |
| Service has no endpoints | Fix Pod labels / Service selector | Changing Service type won't help |
| Config file updates without Pod restart | ConfigMap mounted as a volume (no subPath) | Env vars need a restart |
| Secrets stay in a vault, audited, rotated | Key Vault + Secrets Store CSI Driver | Plain Kubernetes Secrets |
| Pods on many nodes share one volume | azurefile-csi (ReadWriteMany) | managed-csi disks are ReadWriteOnce |
| Test a Service from your laptop | kubectl port-forward | kubectl top shows usage |

## Cosmos DB for NoSQL (LP4)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Cheapest read of one known item | Point read (id + partition key) ≈ 1 RU | Queries cost more |
| Prevent lost updates | _etag optimistic concurrency | _ts is just a timestamp |
| Millions of vectors, fast search | diskANN vector index | flat max 505 dims |
| Exact codes plus meaning in search | Hybrid: RRF(VectorDistance, FullTextScore) | Pure vector search |
| Keep embeddings fresh after edits | Change feed (push: Functions trigger + leases) | Polling the container |
| ORDER BY on two properties | Composite index (same order or exact reverse) | Single range indexes |
| User sees their own upload immediately | Session consistency | Strong doubles read RUs |
| Multi-region writes | Session or weaker | Strong isn't supported |

## Azure Database for PostgreSQL (LP5)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Connection pooling on Azure | Built-in PgBouncer, port 6432 (not Burstable) | 5432 = direct |
| Production TLS check of CA and host | sslmode=verify-full | require doesn't validate certificates |
| Cosine distance in pgvector | <=> with vector_cosine_ops | <-> L2, <#> negative inner product |
| High recall, read-mostly, ample memory | HNSW index | IVFFlat: less memory, faster builds |
| Index an empty table that will fill up | HNSW | IVFFlat needs training data |
| Rebuild index without downtime | CREATE INDEX CONCURRENTLY, then swap | REINDEX blocks writes |
| Exact case names must match | Hybrid with ts_rank + GIN index | Vector-only search |
| Per-query accuracy with pooled connections | SET LOCAL hnsw.ef_search | Plain SET doesn't persist in transaction mode |

## Azure Managed Redis (LP6)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Load data into cache only when requested | Cache-aside | Preloading whole databases |
| Connect redis-py to Azure Managed Redis | Port 10000 | 6380 = Azure Cache for Redis |
| Find keys in production | SCAN | KEYS blocks the server |
| Every API instance must clear its cache now | Pub/sub broadcast | Streams give each message to one consumer |
| Each job processed once, survives crashes | Streams + consumer group (XACK, XCLAIM) | Pub/sub has no durability |
| Vector KNN query in Redis | *=>[KNN k @field $vec] with dialect(2) | Missing dialect 2 fails |
| Flat records, lowest memory | Hash with tobytes() vectors | JSON for nested data |

## Backend integration (LP7)

| You need… | Answer | Don't confuse with |
|---|---|---|
| Each request handled by one worker, absorbs bursts | Service Bus queue | Topic = fan-out copies |
| Several services react to one result | Service Bus topic + subscriptions | Queue competing consumers |
| Ordered processing per document | Service Bus sessions | Duplicate detection doesn't order |
| Long job loses its lock (default 1 min) | AutoLockRenewer / renew_message_lock | Lock max is 5 minutes |
| React to a blob upload without polling | Event Grid system topic (BlobCreated) | Custom topics are for your own events |
| Handler work takes over 30 seconds | Return 202 Accepted, process async | 400 stops retries |
| HTTP work longer than 230 seconds | Async request-reply via Service Bus trigger | functionTimeout can't beat the load balancer |
| Wait days for human approval | Durable Functions: external event + durable timer (task_any) | time.sleep in an orchestrator |
| Many responders watch one live job | Web PubSub operation group | Groups don't assign work |

## Secrets, configuration and observability (LP8–LP9)

| You need… | Answer | Don't confuse with |
|---|---|---|
| App reads a secret value | Key Vault Secrets User | Key Vault Contributor can't read secrets |
| Rotate a key automatically | SecretNearExpiry (30 days) → Function → new version | Expiry doesn't block reads |
| Refresh cache after rotation | SecretNewVersionCreated event | Fixed TTL alone |
| Shared non-secret settings and flags | App Configuration (+ Key Vault references for secrets) | Secrets stored directly in App Configuration |
| Same key, different value per environment | App Configuration labels | Environment-specific key names |
| Turn a pipeline stage off in seconds | Feature flag kill switch | Code rollback |
| Trace ID in Application Insights | operation_Id | cloud_RoleName = service |
| Each service its own Application Map node | service.name (+ service.namespace) | Separate connection strings |
| Exception totals under sampling | sum(itemCount) | count() undercounts |
| Interactive investigation with filters | Workbook with parameters | Dashboards are at-a-glance |
| Alert on p95 latency per service | Log search alert | Smart detection learns baselines |

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
