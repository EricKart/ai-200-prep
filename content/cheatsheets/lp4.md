# LP4 cheat sheet: Develop AI solutions with Azure Cosmos DB for NoSQL

> Skill area 2 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-4)

## Which one?

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

## Must remember

### M1: Build queries for Azure Cosmos DB for NoSQL

- Partition key is **permanent** for a container.
- Uniqueness is **id + partition key**, not id alone.
- Autoscale with max 4,000 runs between **400 and 4,000** RU/s.
- get_container_client doesn't check the container exists; the first operation does.
- Keys = full account access; prefer Entra ID + Data Reader/Contributor roles.
- String comparisons are case-sensitive; use UPPER/LOWER for case-insensitive matches.
- No partition key in the filter → cross-partition query (enable_cross_partition_query=True).

Lesson: [lp4m1](../lessons/lp4m1.md) · Practice: [lp4m1](../../practice/lp4m1.md)

### M2: Implement vector search on Azure Cosmos DB for NoSQL

- A 1,536-dimension embedding can't use a **flat** index (max 505).
- Vector policies can't be added to or changed on an existing container.
- Exclude embedding paths from range indexes.
- No TOP N → the query tries to return every document.
- Query and documents must use the same embedding model.
- Third argument **true** forces brute-force search.
- Post-filtering can return fewer rows than TOP N.
- Hybrid search needs both a full-text policy and full-text indexes.
- Two functions on one data container can share a lease container only with **different leaseContainerPrefix** values.
- Re-embedding on every change wastes money; compare a content hash.

Lesson: [lp4m2](../lessons/lp4m2.md) · Practice: [lp4m2](../../practice/lp4m2.md)

### M3: Optimize query performance for Azure Cosmos DB for NoSQL

- Mode **none** = point reads only; queries do full scans.
- Partition key isn't indexed automatically (unless it's /id).
- Lazy indexing is deprecated; new containers can't use it.
- Only one range filter per composite index, and it goes **last**.
- Removing an index takes effect **immediately**; adding one waits for the transformation.
- indexingSearchListSize applies to **diskANN only**.
- Upgrading to a 3,072-dimension model means a **new container**.
- High retrieved count vs low output count = missing or unused index.
- Don't create dozens of composite indexes for rare queries.
- Strong isn't supported with multiple write regions.
- Switching reads from Strong to Session halves read RU cost.
- Session tokens must be passed between services that share a user flow.

Lesson: [lp4m3](../lessons/lp4m3.md) · Practice: [lp4m3](../../practice/lp4m3.md)

## Commands and syntax you'll see

```text
SELECT p.id, p.name FROM products p WHERE …
az cosmosdb update --capabilities EnableNoSQLVectorSearch
```


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
