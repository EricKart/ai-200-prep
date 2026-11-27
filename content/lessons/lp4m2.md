# LP4 · M2: Implement vector search on Azure Cosmos DB for NoSQL

> **Learning path 4:** Develop AI solutions with Azure Cosmos DB for NoSQL · **Skill area 2:** Develop AI solutions with Azure data services · about 84 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-4/implement-vector-search-azure-cosmos-db)

Cosmos DB can store embeddings next to your data and search them by meaning. You'll learn vector policies and indexes, similarity queries, hybrid search with filters and full text, and keeping embeddings fresh with the change feed.

**In this lesson**

1. [Store and retrieve embeddings in Azure Cosmos DB](#store-and-retrieve-embeddings-in-azure-cosmos-db)
2. [Execute vector similarity queries for semantic search](#execute-vector-similarity-queries-for-semantic-search)
3. [Combine vector similarity results with metadata filtering](#combine-vector-similarity-results-with-metadata-filtering)
4. [Use the change feed to trigger embedding refresh](#use-the-change-feed-to-trigger-embedding-refresh)

## Store and retrieve embeddings in Azure Cosmos DB

📘 Microsoft Learn: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

An embedding is a **list of numbers that captures meaning**; texts that mean similar things get similar lists. In Cosmos DB you store that list right next to the document. The container needs a **vector policy** (where the list is, how long it is, how to compare) and a **vector index** to search fast. Both are set when the container is born.

**Key facts**

- Embeddings are arrays of floats from models such as Azure OpenAI. **text-embedding-ada-002 = 1,536** dimensions; **text-embedding-3-large = 3,072**.
- Store the embedding as an **array property** alongside content and filterable metadata in the same document.
- Enable the account feature first: **Vector Search for NoSQL API** (portal Features) or `az cosmosdb update --capabilities EnableNoSQLVectorSearch`; auto-approved, can take **15 minutes**.
- **Vector embedding policy** per path: `path` (required), `dataType` (float32 default, float16, int8, uint8), `dimensions` (default 1,536; must match the model), `distanceFunction` (cosine default, dotproduct, euclidean).
- Vector policies are set **at container creation** and **can't be modified**; vector search is only supported on **new** containers.
- **Cosine** = angle (recommended for normalized Azure OpenAI embeddings; scores −1 to +1, higher = more similar). **Dot product** = identical to cosine for normalized vectors, slightly faster. **Euclidean** = straight-line distance, 0 = identical.
- **float16** halves storage (50%) with minimal quality impact; int8/uint8 need quantized embeddings. Start with float32.
- Multiple vector paths (e.g. `/titleEmbedding` and `/contentEmbedding`) are allowed in one policy.
- Index types: **flat** (exact, 100% recall, max **505** dimensions), **quantizedFlat** (compressed brute force, up to **4,096** dims, up to ~**50,000 vectors per physical partition**), **diskANN** (approximate, up to 4,096 dims, best for millions).
- Exclude the embedding path from standard range indexes (`excludedPaths`) to save storage and write cost. quantizedFlat and diskANN need at least **1,000 vectors** to be effective.
- Insert with **upsert_item**; when content changes, regenerate the embedding and upsert again.

| Index | Search | Dimensions | Best for |
|---|---|---|---|
| flat | Exact brute force (100% recall) | Up to 505 | Small datasets, exact results |
| quantizedFlat | Compressed brute force | Up to 4,096 | Up to ~50,000 vectors per partition |
| diskANN | Approximate (DiskANN) | Up to 4,096 | Large datasets, millions of vectors |

> [!WARNING]
> **Exam traps**
>
> - A 1,536-dimension embedding can't use a **flat** index (max 505).
> - Vector policies can't be added to or changed on an existing container.
> - Exclude embedding paths from range indexes.

## Execute vector similarity queries for semantic search

📘 Microsoft Learn: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

Turn the user's question into an embedding with the **same model** you used for the documents, then ask for the **TOP N** documents ordered by **VectorDistance**. Higher cosine score = closer meaning.

**Key facts**

- **VectorDistance(vector_expr_1, vector_expr_2, bool_expr, obj_expr)**: document path, query vector, optional **true to force brute force**, optional options object.
- Query pattern: `SELECT TOP 10 c.id, c.title, VectorDistance(c.embedding, @queryVector) AS SimilarityScore FROM c ORDER BY VectorDistance(c.embedding, @queryVector)`. Always use **TOP N**, or the query tries to return everything.
- Generate the query vector with the **same embedding model** as the documents; different models create incompatible vector spaces.
- Pass the vector as a **parameter** (@queryVector): plan caching and readable queries.
- Cosine scores: +1 identical; 0.7–0.9 highly similar; 0.5–0.7 moderate; 0.1–0.5 low; ≤0 dissimilar. A **0.7 threshold** in WHERE returns highly relevant results.
- Result counts: **RAG 5–10**; user search 10–20 with pagination; recommendations 3–5.
- Indexed (approximate) search by default; **brute force** compares against every document: more RUs, higher latency, poor scaling. Use it for evaluation/testing or small datasets.
- Optimize: DiskANN for more than 50,000 vectors per partition, quantizedFlat for smaller; smallest TOP N; partition keys; project only needed fields; monitor RUs.

| Scenario | TOP N |
|---|---|
| RAG context for a language model | 5–10 |
| User-facing search | 10–20 with pagination |
| Recommendations | 3–5 |

> [!WARNING]
> **Exam traps**
>
> - No TOP N → the query tries to return every document.
> - Query and documents must use the same embedding model.
> - Third argument **true** forces brute-force search.

## Combine vector similarity results with metadata filtering

📘 Microsoft Learn: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

Real searches mix **meaning** with **rules**: only published networking guides, only this user's access group. Add WHERE filters to vector queries. When users type exact codes like 0x80070005, add **full-text** scoring and merge both rankings with **RRF**.

**Key facts**

- Combine VectorDistance with WHERE filters (category, date, product, `ARRAY_CONTAINS(c.accessGroups, @userGroup)`, status = 'published').
- **Pre-filtering**: filter first, then compare vectors (efficient with selective filters). **Post-filtering**: rank first, then filter; can return **fewer results than requested**. The optimizer chooses based on selectivity; index filter properties.
- Include the partition key in WHERE and pass `partition_key=` to route to one partition.
- **Hybrid search**: `ORDER BY RANK RRF(VectorDistance(…), FullTextScore(c.content, @t1, @t2))`. **Reciprocal Rank Fusion** merges rankings.
- Hybrid needs a **full-text policy** (`defaultLanguage`, `fullTextPaths`) and **fullTextIndexes** plus vector indexes.
- Weights: `RRF(…, …, [2, 1])` makes vector count twice as much. Higher vector weight for natural-language questions; higher full-text weight for codes, names and exact terms; equal weights as a start.
- **Multi-vector**: RRF over VectorDistance on titleEmbedding and contentEmbedding.
- Trade-offs: selective filters help; hybrid costs more (use it when it adds value); index all filter properties; test at production volumes.

| User searches for… | Approach |
|---|---|
| "internet keeps dropping" | Vector search |
| "error code 0x80070005 access denied" | Hybrid: RRF of VectorDistance + FullTextScore |
| Only content their group may see | WHERE ARRAY_CONTAINS(c.accessGroups, @userGroup) |
| Title or body match | Multi-vector RRF |

> [!WARNING]
> **Exam traps**
>
> - Post-filtering can return fewer rows than TOP N.
> - Hybrid search needs both a full-text policy and full-text indexes.

## Use the change feed to trigger embedding refresh

📘 Microsoft Learn: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

The change feed is a **running diary** of every insert and update in a container. A function reads the diary and **re-embeds** documents whose text changed, so search never serves stale meaning. A separate **lease container** is the bookmark that remembers how far each worker has read.

**Key facts**

- The change feed is a **persistent, ordered log of inserts and updates**; ordered **within a partition key**; each change appears once, consumers checkpoint; **enabled by default**.
- **Push model** (Azure Functions trigger or the change feed processor library): automatic delivery, partition management and load balancing, automatic checkpoints. Recommended for production embedding refresh.
- **Pull model** (`query_items_change_feed`): more control, lower resource use for batch or infrequent work, no extra dependencies; keep the **continuation token** to resume.
- Azure Functions **Cosmos DB trigger** config: database, container, **lease container** (`create_lease_container_if_not_exists`).
- Leases enable **checkpointing**, **coordination** across instances, and **failover**. A small lease container (~**400 RU/s**) is usually enough; name it differently from data containers; share it with **different leaseContainerPrefix** values.
- **Selective refresh**: re-embed only when text that affects search changed, for example by comparing a stored **content hash**.
- High volume: **batch** embedding calls, retry with exponential backoff, **queue-based** processing (Azure Queue Storage), prioritized refresh.
- Processing must be **idempotent**; handle NOT_FOUND for deleted documents, use ETags for concurrent updates, dead-letter repeatedly failing documents.
- Scale out: more instances share partitions via the lease container; watch **ChangeFeedProcessorHostLag**.

| Model | Best for |
|---|---|
| Push (Functions trigger / processor library) | Continuous production refresh with checkpoints and scaling |
| Pull (query_items_change_feed + continuation token) | Batch jobs, one-time migrations, full control |

> [!WARNING]
> **Exam traps**
>
> - Two functions on one data container can share a lease container only with **different leaseContainerPrefix** values.
> - Re-embedding on every change wastes money; compare a content hash.

## Check yourself

- **Practice questions:** [lp4m2 on GitHub](../../practice/lp4m2.md), or [on the site](https://aryantripathi.dev/ai-200/lp-4/implement-vector-search-azure-cosmos-db) with hints and saved progress
- **Cheat sheet:** [Learning path 4](../cheatsheets/lp4.md)
- **Microsoft Learn exercise:** [Build a semantic search application with Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/6-exercise-build-semantic-search)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
