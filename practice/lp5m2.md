# Practice: LP5 · M2 Implement vector search with Azure Database for PostgreSQL

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp5m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-5/implement-vector-search-azure-database-postgresql)

## 1. `lp5m2-001`

Which pgvector operator calculates cosine distance?

- **A.** <->
- **B.** <#>
- **C.** <=>
- **D.** @>

<details><summary>💡 Hint</summary>

pgvector has three distance operators. Cosine is the one with an equals sign.

</details>

<details><summary>✅ Answer</summary>

**C.** <=>

- A: <-> is L2 (Euclidean) distance.
- B: <#> is negative inner product.
- C: Correct. <=> is cosine distance.
- D: @> is the JSONB containment operator.

<-> L2, <=> cosine, <#> negative inner product.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 2. `lp5m2-002`

You enable vector search on an Azure Database for PostgreSQL database. Which command adds pgvector?

- **A.** az postgres flexible-server parameter set --name vector.enabled
- **B.** CREATE EXTENSION IF NOT EXISTS vector;
- **C.** ALTER DATABASE SET vector = on;
- **D.** CREATE EXTENSION IF NOT EXISTS pgvector_search;

<details><summary>💡 Hint</summary>

Extensions are added with a CREATE statement, and the extension's name is short.

</details>

<details><summary>✅ Answer</summary>

**B.** CREATE EXTENSION IF NOT EXISTS vector;

- A: Learn enables pgvector with CREATE EXTENSION.
- B: Correct. The extension name is vector.
- C: Extensions aren't enabled with a database setting like this.
- D: That isn't the extension's name.

Run CREATE EXTENSION with a role such as azure_pg_admin.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 3. `lp5m2-003`

Inserts into `embedding vector(1536)` fail after the team switched to a sentence transformer model. What's the likely cause?

- **A.** Sentence transformer vectors need the <#> operator to insert
- **B.** Its 384-dimension output doesn't match vector(1536)
- **C.** pgvector needs a halfvec column for non-OpenAI models
- **D.** The extension has to be re-created after any model change

<details><summary>💡 Hint</summary>

vector(n) must match the model's output size.

</details>

<details><summary>✅ Answer</summary>

**B.** Its 384-dimension output doesn't match vector(1536)

- A: Operators are for queries, not inserts.
- B: Correct. Sentence transformers typically output 384 dimensions; mismatched counts cause insert errors.
- C: halfvec is about precision, not model vendors.
- D: The extension doesn't need re-creating.

vector(n) must match the model's output dimension.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 4. `lp5m2-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A query uses `ORDER BY embedding <=> $1 LIMIT 10` on a vector(1536) column.

| Statement | Yes / No |
|---|---|
| Rows with smaller values are more similar to the query. | ☐ |
| A cosine distance of 2 means the vectors point in opposite directions. | ☐ |
| Storing the column as halfvec(1536) would double the storage. | ☐ |
| The <#> operator returns cosine similarity, where larger is better. | ☐ |

<details><summary>💡 Hint</summary>

For distances, smaller means closer. Cosine distance runs from 0 to 2. halfvec saves space.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Rows with smaller values are more similar to the query. | Yes | Smaller distance means more similar. |
| A cosine distance of 2 means the vectors point in opposite directions. | Yes | Cosine distance ranges from 0 (identical direction) to 2 (opposite). |
| Storing the column as halfvec(1536) would double the storage. | No | halfvec halves the storage. |
| The <#> operator returns cosine similarity, where larger is better. | No | <#> is negative inner product; like the other operators, smaller is better. |

pgvector distances: smaller is closer; vector type ≈ 4 bytes per dimension.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 5. `lp5m2-005`

A model produces sparse embeddings with about 3,000 non-zero values out of 30,000 dimensions, and you want an HNSW index. What should you know?

- **A.** sparsevec can't be indexed at all, so store it as vector(30000)
- **B.** HNSW handles any number of non-zero elements on sparsevec
- **C.** HNSW on sparsevec allows up to 1,000 non-zero elements
- **D.** halfvec is required for sparse embeddings above 1,000 values

<details><summary>💡 Hint</summary>

HNSW on sparse vectors has a limit on non-zero elements.

</details>

<details><summary>✅ Answer</summary>

**C.** HNSW on sparsevec allows up to 1,000 non-zero elements

- A: sparsevec can be indexed within the limit.
- B: There's a 1,000 non-zero element limit.
- C: Correct. Learn notes the 1,000 non-zero element limit for HNSW on sparsevec.
- D: halfvec is for dense half-precision vectors.

sparsevec stores only non-zero values; HNSW supports up to 1,000 of them.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 6. `lp5m2-006`

Match each pgvector operator to the distance it calculates.

Choices: **L2 (Euclidean) distance** · **Cosine distance** · **Negative inner product**

- <->
- <=>
- <#>

<details><summary>💡 Hint</summary>

One operator has a hash mark, one has an equals sign, and one has a dash.

</details>

<details><summary>✅ Answer</summary>

- <-> → **L2 (Euclidean) distance**. <-> is L2 (Euclidean) distance, used with vector_l2_ops.
- <=> → **Cosine distance**. <=> is cosine distance, used with vector_cosine_ops.
- <#> → **Negative inner product**. <#> is negative inner product, used with vector_ip_ops for maximum inner product search.

pgvector operators: <-> L2 distance, <=> cosine distance, <#> negative inner product. For all three, smaller results mean closer vectors.

📘 Source: [Store and query embeddings with pgvector](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/2-store-query-embeddings-pgvector)

</details>

## 7. `lp5m2-007`

Queries use the <=> operator. Which operator class should the HNSW index use?

- **A.** gin_trgm_ops
- **B.** vector_l2_ops
- **C.** vector_cosine_ops
- **D.** vector_ip_ops

<details><summary>💡 Hint</summary>

The operator class must match the operator used in queries.

</details>

<details><summary>✅ Answer</summary>

**C.** vector_cosine_ops

- A: That's for trigram text search, not vectors.
- B: vector_l2_ops matches <->.
- C: Correct. vector_cosine_ops matches <=>.
- D: vector_ip_ops matches <#>.

Operator class and query operator must match, or PostgreSQL falls back to a sequential scan.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 8. `lp5m2-008`

You create an IVFFlat index on a new, empty table and then load 500,000 vectors. Search results are poor. Why?

- **A.** IVFFlat can't index more than 100,000 vectors
- **B.** IVFFlat needs existing data to train its clusters
- **C.** IVFFlat has to be created with CONCURRENTLY
- **D.** IVFFlat requires the vector_ip_ops operator class

<details><summary>💡 Hint</summary>

IVFFlat learns something from the data when the index is built.

</details>

<details><summary>✅ Answer</summary>

**B.** IVFFlat needs existing data to train its clusters

- A: Learn gives no such limit.
- B: Correct. An IVFFlat index created on an empty table isn't usable; load data first.
- C: CONCURRENTLY avoids blocking; it doesn't fix untrained clusters.
- D: Any matching operator class works.

Load data, then create IVFFlat. HNSW, by contrast, can start on an empty table.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 9. `lp5m2-009`

For each statement, select Yes if the statement is true. Otherwise, select No. A product search app uses HNSW with default settings.

| Statement | Yes / No |
|---|---|
| The default number of connections per node (m) is 16. | ☐ |
| The default hnsw.ef_search value is 40. | ☐ |
| Raising ef_search to 100–200 typically lowers recall. | ☐ |

<details><summary>💡 Hint</summary>

HNSW defaults: 16 connections per node and a search list of 40. A bigger search list raises recall.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The default number of connections per node (m) is 16. | Yes | m defaults to 16. |
| The default hnsw.ef_search value is 40. | Yes | Start with the default of 40. |
| Raising ef_search to 100–200 typically lowers recall. | No | Values of 100–200 typically achieve 99%+ recall. |

m and ef_construction shape the graph; ef_search sets query-time width.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 10. `lp5m2-010`

EXPLAIN ANALYZE shows Seq Scan for `SELECT id FROM documents ORDER BY embedding <-> $1`, although an HNSW index with vector_l2_ops exists on a large table. What is most likely missing?

- **A.** A LIMIT clause on the query
- **B.** A GIN index on the content column
- **C.** An IVFFlat index as well
- **D.** A halfvec column type

<details><summary>💡 Hint</summary>

The planner uses a vector index only for ORDER BY distance with a LIMIT.

</details>

<details><summary>✅ Answer</summary>

**A.** A LIMIT clause on the query

- A: Correct. Vector indexes are most effective with ORDER BY and LIMIT; Learn lists the missing LIMIT as a cause of Seq Scan.
- B: GIN indexes help full-text search, not vector ordering.
- C: A second index type isn't needed.
- D: The data type isn't the cause here.

Check operator class, index validity, table size and the LIMIT clause when you see Seq Scan.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 11. `lp5m2-011`

A query asks for `LIMIT 100` results from an HNSW index while `hnsw.ef_search` is still at its default. What should you change?

- **A.** Lower hnsw.ef_search to 20 for speed
- **B.** Rebuild the index with a larger m
- **C.** Raise hnsw.ef_search to at least 100
- **D.** Switch the operator class to vector_ip_ops

<details><summary>💡 Hint</summary>

Compare ef_search with the number of results you ask for.

</details>

<details><summary>✅ Answer</summary>

**C.** Raise hnsw.ef_search to at least 100

- A: Lower values trade recall for speed and are still below the LIMIT.
- B: m is a build-time parameter; ef_search is the query-time setting here.
- C: Correct. ef_search should be at least as large as the number of results you request; the default is 40.
- D: The operator class must match the query operator; it isn't the issue.

Set ef_search per session with SET hnsw.ef_search = …; it should be at least the LIMIT.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 12. `lp5m2-012`

A 50-million-row embeddings table needs searches under 100 ms, and the team can accept that a few true nearest neighbors are occasionally missed. What fits?

- **A.** No index, with LIMIT 10 to keep the scan short
- **B.** An exact sequential scan with a larger server
- **C.** An approximate nearest-neighbor index such as HNSW
- **D.** A B-tree index on the embedding column

<details><summary>💡 Hint</summary>

The team accepts "occasionally missed". Which kind of index trades a little accuracy for speed?

</details>

<details><summary>✅ Answer</summary>

**C.** An approximate nearest-neighbor index such as HNSW

- A: Without an index, the database still compares every row before sorting.
- B: An exact scan computes 50 million distances per query, far too slow for 100 ms.
- C: Correct. ANN search trades perfect accuracy for dramatic speed, measured as recall.
- D: B-tree indexes don't support nearest-neighbor distance search.

Approximate nearest-neighbor (ANN) indexes examine only a subset of vectors, trading perfect accuracy for speed. Recall measures how many true nearest neighbors appear in the results.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 13. `lp5m2-013`

An IVFFlat index has lists = 100. You're choosing a starting value for ivfflat.probes. What does Learn suggest?

- **A.** Set probes to 1 so that queries stay as fast as possible
- **B.** Set probes equal to lists divided by 2, then never change it
- **C.** Set probes to 100 so that every cluster is searched
- **D.** Start at 10, the square root of lists, then tune for recall and latency

<details><summary>💡 Hint</summary>

Learn gives a square-root rule of thumb.

</details>

<details><summary>✅ Answer</summary>

**D.** Start at 10, the square root of lists, then tune for recall and latency

- A: One probe is fast but searches the fewest clusters, which can hurt recall. Learn's starting point is sqrt(lists).
- B: Learn gives sqrt(lists) as the starting point, and says to adjust it for your recall and latency needs.
- C: That searches everything, which removes the index's speed benefit.
- D: Correct. Start with probes = sqrt(lists) and adjust based on your recall and latency needs.

probes controls how many clusters are searched at query time. Higher values improve recall but increase latency. Start with probes = sqrt(lists), set per session with SET ivfflat.probes.

📘 Source: [Perform fast vector similarity search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/3-perform-fast-vector-similarity-search)

</details>

## 14. `lp5m2-014`

You must rebuild a vector index on a production table without blocking queries. What should you use?

- **A.** VACUUM FULL documents to rebuild storage
- **B.** DROP INDEX first, then CREATE INDEX again
- **C.** REINDEX INDEX on the existing vector index
- **D.** CREATE INDEX CONCURRENTLY, then swap names

<details><summary>💡 Hint</summary>

Build a replacement without blocking reads and writes.

</details>

<details><summary>✅ Answer</summary>

**D.** CREATE INDEX CONCURRENTLY, then swap names

- A: VACUUM FULL reclaims space and locks the table; it doesn't rebuild the vector index structure.
- B: Dropping first leaves queries without an index.
- C: REINDEX blocks writes during the rebuild.
- D: Correct. Build concurrently, verify, drop the old index and rename.

CREATE INDEX CONCURRENTLY takes longer but keeps serving requests.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 15. `lp5m2-015`

You're migrating from a 1,536-dimension model to a 3,072-dimension model with no downtime. Put the parallel-column steps in order.

- Add a new column, embedding_v2 vector(3072)
- Backfill embedding_v2 in batches
- Create an HNSW index on embedding_v2
- Drop the old column and index, then rename the new ones
- Switch queries to embedding_v2 after comparing results

<details><summary>💡 Hint</summary>

Add the new column and its index, fill it, switch, then clean up.

</details>

<details><summary>✅ Answer</summary>

1. Add a new column, embedding_v2 vector(3072)
2. Create an HNSW index on embedding_v2
3. Backfill embedding_v2 in batches
4. Switch queries to embedding_v2 after comparing results
5. Drop the old column and index, then rename the new ones

Parallel columns let you validate the new model and roll back if it underperforms.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 16. `lp5m2-016`

For each statement, select Yes if the statement is true. Otherwise, select No. Editors update document text hundreds of times an hour, and embeddings are regenerated in the same transaction.

| Statement | Yes / No |
|---|---|
| Marking rows embedding_stale = TRUE and re-embedding in batches would lower content update latency. | ☐ |
| Synchronous re-embedding in the same transaction is Learn's advice for frequent edits. | ☐ |
| PostgreSQL reclaims disk space immediately when a row is updated. | ☐ |
| VACUUM FULL is the non-locking option for busy tables. | ☐ |

<details><summary>💡 Hint</summary>

For frequent edits, mark rows stale and re-embed in batches.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Marking rows embedding_stale = TRUE and re-embedding in batches would lower content update latency. | Yes | Batching decouples content updates from embedding generation. |
| Synchronous re-embedding in the same transaction is Learn's advice for frequent edits. | No | For frequent changes, Learn recommends async batch processing with a stale flag. |
| PostgreSQL reclaims disk space immediately when a row is updated. | No | MVCC keeps old row versions until VACUUM reclaims them. |
| VACUUM FULL is the non-locking option for busy tables. | No | VACUUM FULL locks the table; standard VACUUM runs concurrently. |

For frequent updates: stale flags, batch re-embedding, and tuned autovacuum.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 17. `lp5m2-017`

A table will hold 1 million rows with `vector(1536)` embeddings. Roughly how much storage does the vector column alone need, before any index?

- **A.** About 6 GB
- **B.** About 1.5 GB
- **C.** About 60 GB
- **D.** About 12 GB

<details><summary>💡 Hint</summary>

Each float32 element is 4 bytes. Multiply by dimensions and rows.

</details>

<details><summary>✅ Answer</summary>

**A.** About 6 GB

- A: Correct. 1,536 dimensions × 4 bytes ≈ 6 KB per row, so about 6 GB for a million rows.
- B: That's the size for 384-dimension vectors.
- C: That's ten times too large.
- D: That's the size for 3,072-dimension vectors.

Vector column storage ≈ dimensions × 4 bytes × rows; indexes add more on top.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 18. `lp5m2-018`

You loaded embeddings from a new document domain, adding about 35% more rows. Search latency is up, and users say results are less relevant. What does Learn suggest?

- **A.** Drop the index and rely on exact scans
- **B.** Change the operator class to vector_ip_ops
- **C.** Lower hnsw.ef_search to make queries faster
- **D.** Rebuild the vector index, for example with CREATE INDEX CONCURRENTLY

<details><summary>💡 Hint</summary>

ANN indexes are shaped by the data they were built on. A lot of new data changes that.

</details>

<details><summary>✅ Answer</summary>

**D.** Rebuild the vector index, for example with CREATE INDEX CONCURRENTLY

- A: Exact scans are too slow at this size.
- B: The operator class must match the query operator. Changing it doesn't fix a stale structure.
- C: That lowers recall further, which makes relevance worse.
- D: Correct. Adding more than 20–30% new data, especially from a new domain, often warrants rebuilding the ANN index.

ANN indexes optimize for the data distribution at creation. Rising latency, falling relevance, or adding more than 20–30% new data (especially a new domain) signal a rebuild. Use CREATE INDEX CONCURRENTLY to avoid blocking.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 19. `lp5m2-019`

A small internal tool can tolerate a short pause in writes at night. You need to rebuild its vector index. Which approach does Learn describe as simpler for this case?

- **A.** Switch to an IVFFlat index on an empty table
- **B.** CREATE INDEX CONCURRENTLY followed by a rename
- **C.** Drop the column and reload all embeddings
- **D.** REINDEX INDEX during a low-traffic period

<details><summary>💡 Hint</summary>

Brief interruptions are acceptable here, so you don't need the non-blocking route.

</details>

<details><summary>✅ Answer</summary>

**D.** REINDEX INDEX during a low-traffic period

- A: IVFFlat needs data to train, and an empty table gives an unusable index.
- B: This avoids blocking, but it's the more involved option, meant for systems that can't tolerate downtime.
- C: That loses data and takes much longer than rebuilding the index.
- D: Correct. REINDEX is simpler, but it blocks writes, so schedule it during quiet periods.

For systems that tolerate brief interruptions, REINDEX INDEX is simpler but blocks writes. For systems that can't, use CREATE INDEX CONCURRENTLY, verify, drop the old index, and rename.

📘 Source: [Manage index lifecycle and embedding updates](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/4-manage-index-lifecycle-embedding-updates)

</details>

## 20. `lp5m2-020`

A legal assistant should return nothing rather than unrelated contracts when no good match exists. What should the query add?

- **A.** A threshold: WHERE embedding <=> $1 < 0.4
- **B.** A GIN index on the embedding column
- **C.** An ORDER BY on created_at instead of distance
- **D.** A larger LIMIT, such as LIMIT 100 rows

<details><summary>💡 Hint</summary>

Returning nothing beats returning something unrelated. Add a cut-off on distance.

</details>

<details><summary>✅ Answer</summary>

**A.** A threshold: WHERE embedding <=> $1 < 0.4

- A: Correct. A threshold sets a quality floor; empty results can be the right answer.
- B: GIN indexes are for full-text, not vector distance.
- C: Ordering by date ignores similarity.
- D: A larger LIMIT returns more weak matches.

Combine a threshold for quality with LIMIT for resource control.

📘 Source: [Run vector similarity search for semantic retrieval](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/5-run-vector-similarity-search-semantic-retrieval)

</details>

## 21. `lp5m2-021`

An attorney searches for "Smith v. Jones" and expects that exact case name, but vector search returns semantically similar cases first. What should you implement?

- **A.** Lower the cosine distance threshold to 0.1
- **B.** Switch the distance operator from <=> to <->
- **C.** Average the query vector with the top result's vector
- **D.** Hybrid search: vector similarity plus ts_rank

<details><summary>💡 Hint</summary>

Exact names need keyword matching. Combine it with vector similarity.

</details>

<details><summary>✅ Answer</summary>

**D.** Hybrid search: vector similarity plus ts_rank

- A: A stricter threshold may remove results but doesn't match exact names.
- B: Changing the distance metric doesn't add keyword matching.
- C: Averaging doesn't add exact term matching.
- D: Correct. Hybrid search captures both semantic and lexical relevance.

Use hybrid search for exact terms, names and codes; speed it with a GIN index on the tsvector.

📘 Source: [Run vector similarity search for semantic retrieval](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/5-run-vector-similarity-search-semantic-retrieval)

</details>

## 22. `lp5m2-022`

A user wants documents about "mergers AND environmental compliance". You have an embedding for each concept. What does Learn recommend?

- **A.** Average the two embeddings and run one query
- **B.** Query each aspect separately and combine the results
- **C.** Use whichever concept has more documents
- **D.** Run the merger query alone, then filter by keyword

<details><summary>💡 Hint</summary>

Two separate concepts are better searched one at a time.

</details>

<details><summary>✅ Answer</summary>

**B.** Query each aspect separately and combine the results

- A: The average may land near neither concept.
- B: Correct. Different aspects shouldn't be averaged; retrieve for each and rank by combined relevance.
- C: That ignores the other aspect.
- D: That ignores half the query's meaning.

Average only semantically related examples; query distinct aspects separately.

📘 Source: [Run vector similarity search for semantic retrieval](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/5-run-vector-similarity-search-semantic-retrieval)

</details>

## 23. `lp5m2-023`

For each statement, select Yes if the statement is true. Otherwise, select No. A filtered vector query: `WHERE category = 'contracts' AND practice_area = 'corporate' ORDER BY embedding <=> $1 LIMIT 10`.

| Statement | Yes / No |
|---|---|
| B-tree indexes on category and practice_area can help this query. | ☐ |
| Running ANALYZE after loading data helps the planner choose well. | ☐ |
| PostgreSQL always uses the vector index, whatever the filter selectivity. | ☐ |

<details><summary>💡 Hint</summary>

Indexes on filter columns and fresh statistics help the planner.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| B-tree indexes on category and practice_area can help this query. | Yes | Index frequently filtered columns. |
| Running ANALYZE after loading data helps the planner choose well. | Yes | Accurate statistics guide the planner. |
| PostgreSQL always uses the vector index, whatever the filter selectivity. | No | With very selective filters, it may scan matching rows without the vector index. |

The planner optimizes total cost; inspect plans with EXPLAIN ANALYZE.

📘 Source: [Run vector similarity search for semantic retrieval](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/5-run-vector-similarity-search-semantic-retrieval)

</details>

## 24. `lp5m2-024`

Match each retrieval metric to what it measures.

Choices: **Precision** · **Recall** · **MRR**

- The fraction of retrieved chunks that are actually relevant
- The fraction of relevant chunks that were retrieved
- How high the first relevant result appears in the list

<details><summary>💡 Hint</summary>

Precision: of what you retrieved, how much was relevant. Recall: of what was relevant, how much did you get. MRR: how soon the first hit appears.

</details>

<details><summary>✅ Answer</summary>

- The fraction of retrieved chunks that are actually relevant → **Precision**. Low precision feeds the LLM irrelevant context.
- The fraction of relevant chunks that were retrieved → **Recall**. Low recall means missing information.
- How high the first relevant result appears in the list → **MRR**. Mean Reciprocal Rank rewards early relevant results.

Measure retrieval separately from generation with a labelled evaluation set.

📘 Source: [Implement retrieval patterns for RAG pipelines](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/6-implement-retrieval-patterns-rag-pipelines)

</details>

## 25. `lp5m2-025`

Retrieved contract chunks often say "as described above" without containing the referenced text. Which pattern helps?

- **A.** Switching to fixed-size chunks with no overlap
- **B.** Context-window retrieval of adjacent chunks
- **C.** Removing the source_documents table entirely
- **D.** Lowering the LIMIT to one chunk per query

<details><summary>💡 Hint</summary>

The chunk refers to text that's next to it in the document.

</details>

<details><summary>✅ Answer</summary>

**B.** Context-window retrieval of adjacent chunks

- A: Fixed-size chunks without overlap can cut ideas mid-thought.
- B: Correct. Fetching neighbours (e.g. 46 and 48 around 47) supplies the missing context.
- C: The source table is needed for citations.
- D: Fewer chunks make the missing context worse.

Context windows cost more tokens but reduce incomplete answers.

📘 Source: [Implement retrieval patterns for RAG pipelines](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/6-implement-retrieval-patterns-rag-pipelines)

</details>

## 26. `lp5m2-026`

Evaluation shows low recall: answers miss relevant clauses. Which two changes does Learn suggest? (Select two.)

- **A.** Increase hnsw.ef_search
- **B.** Tighten the distance threshold
- **C.** Loosen the distance threshold
- **D.** Retrieve fewer chunks per query

<details><summary>💡 Hint</summary>

Low recall: search more widely and accept slightly less similar matches.

</details>

<details><summary>✅ Answer</summary>

**A.** Increase hnsw.ef_search  
**C.** Loosen the distance threshold

- A: Correct. Higher ef_search searches more candidates and improves recall.
- B: Tighter thresholds improve precision, not recall.
- C: Correct. Looser thresholds include more candidates.
- D: Fewer chunks lower recall.

Recall levers: looser thresholds, more chunks, higher ef_search or probes.

📘 Source: [Implement retrieval patterns for RAG pipelines](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-database-postgresql/6-implement-retrieval-patterns-rag-pipelines)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
