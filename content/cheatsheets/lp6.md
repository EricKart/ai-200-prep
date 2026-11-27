# LP6 cheat sheet: Enhance AI solutions with Azure Managed Redis

> Skill area 2 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-6)

## Which one?

| You need… | Answer | Don't confuse with |
|---|---|---|
| Load data into cache only when requested | Cache-aside | Preloading whole databases |
| Connect redis-py to Azure Managed Redis | Port 10000 | 6380 = Azure Cache for Redis |
| Find keys in production | SCAN | KEYS blocks the server |
| Every API instance must clear its cache now | Pub/sub broadcast | Streams give each message to one consumer |
| Each job processed once, survives crashes | Streams + consumer group (XACK, XCLAIM) | Pub/sub has no durability |
| Vector KNN query in Redis | *=>[KNN k @field $vec] with dialect(2) | Missing dialect 2 fails |
| Flat records, lowest memory | Hash with tobytes() vectors | JSON for nested data |

## Must remember

### M1: Implement data operations in Azure Managed Redis

- Cache-aside loads on demand; it doesn't preload whole databases.
- Compute Optimized has the **lowest** memory-to-vCPU ratio.
- FLUSHALL and FLUSHDB are blocked with active geo-replication.
- Use SCAN, never KEYS, in production.
- SETEX is for strings; for hashes, HSET then EXPIRE.
- TTL −1 = no expiry; −2 = key doesn't exist.
- Port 10000 for Azure Managed Redis.

Lesson: [lp6m1](../lessons/lp6m1.md) · Practice: [lp6m1](../../practice/lp6m1.md)

### M2: Implement event messaging with Azure Managed Redis

- A subscriber that restarts misses everything published while it was down.
- Publishers get no delivery confirmation.
- Acknowledged entries still use memory until trimmed.
- Unacknowledged tasks stay pending; reclaim them with XCLAIM.
- Several workers subscribed to one channel = duplicate processing.
- XREADGROUP with > gets new messages; with 0 gets your pending ones.

Lesson: [lp6m2](../lessons/lp6m2.md) · Practice: [lp6m2](../../practice/lp6m2.md)

### M3: Implement vector storage in Azure Managed Redis

- Vector queries need **dialect 2**.
- In hybrid queries, the filter comes **before** =>.
- Redis returns distances: lower = more similar.
- FLOAT64 doubles memory without meaningful accuracy gains for embeddings.
- FLAT is exact; HNSW is approximate.
- JSON index fields use $. paths with as_name.
- Changing from Hash to JSON means re-ingesting and a new index.

Lesson: [lp6m3](../lessons/lp6m3.md) · Practice: [lp6m3](../../practice/lp6m3.md)


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
