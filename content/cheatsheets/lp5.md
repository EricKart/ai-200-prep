# LP5 cheat sheet: Develop AI solutions with Azure Database for PostgreSQL

> Skill area 2 · one page to review before the exam · full lessons in [content/lessons](../lessons/) · practise at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-5)

## Which one?

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

## Must remember

### M1: Build and query with Azure Database for PostgreSQL

- PgBouncer: port **6432**, General Purpose or Memory Optimized only.
- Backup retention: 7 days default, max **35**.
- PITR restores to a **new** server.
- Entra token resource: **https://ossrdbms-aad.database.windows.net**.
- sslmode=disable is rejected by Azure.
- Can't connect from your laptop on public access? Check the **firewall rules**.
- Default referential action is **RESTRICT**.
- An index on (conversation_id, created_at) doesn't serve a filter on created_at alone.
- Aliases can't be used in WHERE.
- OFFSET gets slower the deeper you page.
- xmax = 0 → the row was inserted, not updated.
- COPY for 10,000+ rows; executemany for hundreds to a few thousand.
- Never build SQL with f-strings from user input.

Lesson: [lp5m1](../lessons/lp5m1.md) · Practice: [lp5m1](../../practice/lp5m1.md)

### M2: Implement vector search with Azure Database for PostgreSQL

- Cosine **distance** (pgvector) is smaller-is-better, unlike Cosmos DB's cosine **similarity** score.
- halfvec halves storage; sparsevec stores only non-zeros.
- Index built with vector_l2_ops but query uses <=> → **no index use**.
- IVFFlat on an empty table isn't usable; load data first.
- VACUUM FULL locks the table.
- Default autovacuum triggers at 20% changed rows.
- Average vectors only for related examples; different aspects → separate queries.
- Thresholds stop irrelevant results; LIMIT controls resources. Use both.
- Recall = share of the relevant chunks you actually retrieved.
- Composite (document_id, chunk_index) supports fetching neighbours.

Lesson: [lp5m2](../lessons/lp5m2.md) · Practice: [lp5m2](../../practice/lp5m2.md)

### M3: Optimize vector search in Azure Database for PostgreSQL

- work_mem multiplies by connections and operations; don't raise it globally.
- effective_cache_size doesn't allocate memory.
- ef_construction affects build time and graph quality, not query time or index size.
- Changing HNSW m means rebuilding the index.
- GIN on JSONB doesn't accelerate range queries.
- One vector index per vector column.
- Read replicas are asynchronous; a user's just-saved preferences should be read from the primary.
- Up to five read replicas per primary.
- In transaction mode use **SET LOCAL**, not SET.
- LISTEN/NOTIFY needs persistent connections; it doesn't work with transaction pooling.

Lesson: [lp5m3](../lessons/lp5m3.md) · Practice: [lp5m3](../../practice/lp5m3.md)

## Commands and syntax you'll see

```text
CREATE EXTENSION
az postgres flexible-server parameter set --name pgbouncer.enabled --value true
CREATE EXTENSION IF NOT EXISTS vector;
SELECT * FROM pg_extension WHERE extname = 'vector';
SET ivfflat.probes = 10
EXPLAIN ANALYZE
SET work_mem = '256MB'
CREATE INDEX … (category_id) WHERE in_stock = true
SET LOCAL work_mem = '256MB'
SET LOCAL hnsw.ef_search = 200
```


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
