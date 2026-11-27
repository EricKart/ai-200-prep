# Practice: LP5 · M3 Optimize vector search in Azure Database for PostgreSQL

> 27 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp5m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-5/optimize-vector-search-azure-database-postgresql)

## 1. `lp5m3-001`

Azure Database for PostgreSQL runs on SSD storage, but the planner keeps choosing sequential scans for vector queries. Which setting does Learn suggest lowering to 1.1–1.5?

- **A.** effective_io_concurrency
- **B.** random_page_cost
- **C.** work_mem
- **D.** shared_buffers

<details><summary>💡 Hint</summary>

The planner thinks random reads are expensive, a default meant for spinning disks.

</details>

<details><summary>✅ Answer</summary>

**B.** random_page_cost

- A: Learn suggests raising effective_io_concurrency to 200, not lowering it.
- B: Correct. The default 4.0 assumes spinning disks; lower values encourage index scans on SSD.
- C: work_mem affects sorts and hashes, not this cost estimate.
- D: shared_buffers is the cache size, not a cost estimate.

random_page_cost tells the planner how expensive random reads are compared with sequential reads.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 2. `lp5m3-002`

What is the default value of hnsw.ef_search?

- **A.** 40
- **B.** 16
- **C.** 200
- **D.** 1

<details><summary>💡 Hint</summary>

The default HNSW search list size is a small round number.

</details>

<details><summary>✅ Answer</summary>

**A.** 40

- A: Correct. The default ef_search is 40.
- B: 16 is the default HNSW m (connections per node).
- C: 200 is at the high-accuracy end of the suggested range.
- D: 1 is the default for ivfflat.probes.

Increase ef_search to 100–200 for high accuracy; lower it to about 20 for latency-critical apps.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 3. `lp5m3-003`

A server handles 300 concurrent connections. A developer wants to set work_mem to 256 MB globally so vector sorts stop spilling. What's the risk?

- **A.** work_mem is just a planner hint and has no effect on sorts
- **B.** Azure ignores work_mem changes above 64 MB
- **C.** It applies per operation per connection, so total use can explode
- **D.** Higher work_mem lowers the cache hit ratio below 99% immediately

<details><summary>💡 Hint</summary>

work_mem is allocated per sort or hash, in every connection.

</details>

<details><summary>✅ Answer</summary>

**C.** It applies per operation per connection, so total use can explode

- A: That describes effective_cache_size.
- B: Learn doesn't describe such a cap.
- C: Correct. Raise it per session or transaction for vector queries instead.
- D: Learn ties the hit ratio to shared_buffers, not work_mem.

Use SET work_mem (or SET LOCAL) for the sessions that need it.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 4. `lp5m3-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A team tunes memory for a dedicated vector search server.

| Statement | Yes / No |
|---|---|
| A buffer cache hit ratio below 99% can mean shared_buffers is too small. | ☐ |
| effective_cache_size allocates memory for PostgreSQL's cache. | ☐ |
| The default random_page_cost of 4.0 is tuned for SSD storage. | ☐ |
| Inner product (<#>) is the cheapest operator but needs normalized vectors to be meaningful. | ☐ |

<details><summary>💡 Hint</summary>

A low cache hit ratio means more memory is needed. One parameter only hints at the OS cache.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A buffer cache hit ratio below 99% can mean shared_buffers is too small. | Yes | Learn uses <99% as a sign shared_buffers may be too small. |
| effective_cache_size allocates memory for PostgreSQL's cache. | No | It's a planner hint and doesn't allocate memory. |
| The default random_page_cost of 4.0 is tuned for SSD storage. | No | 4.0 reflects spinning disks; use 1.1–1.5 on Azure's SSDs. |
| Inner product (<#>) is the cheapest operator but needs normalized vectors to be meaningful. | Yes | Inner product is fastest and requires pre-normalized vectors. |

Measure cache hits and IO, then size shared_buffers; remember which settings are hints.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 5. `lp5m3-005`

After loading 800,000 new products, EXPLAIN ANALYZE shows Seq Scan on a query that used the vector index yesterday. The operator class matches and LIMIT is present. What should you try first?

- **A.** Raise random_page_cost to 4.0
- **B.** Drop the vector index and rebuild it with IVFFlat
- **C.** Run ANALYZE on the table to refresh statistics
- **D.** Set ivfflat.probes to its default of 1

<details><summary>💡 Hint</summary>

The table changed a lot, and the planner is using old row counts.

</details>

<details><summary>✅ Answer</summary>

**C.** Run ANALYZE on the table to refresh statistics

- A: Raising it discourages index scans.
- B: Switching index types doesn't fix stale statistics.
- C: Correct. Outdated statistics after big data changes can make the planner skip the index.
- D: probes doesn't influence whether the planner uses an index.

Stale statistics, large result shares and operator mismatches are the common reasons an index is skipped.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 6. `lp5m3-006`

Vector queries on a dedicated search server keep reading index pages from disk. The cache hit ratio is 94%. Which parameter should you look at?

- **A.** random_page_cost, so that disk reads become cheaper
- **B.** work_mem, so that each sort gets more memory
- **C.** shared_buffers, PostgreSQL's shared page cache
- **D.** max_connections, so that fewer sessions compete

<details><summary>💡 Hint</summary>

Which parameter sizes the memory cache that every session reads data pages from?

</details>

<details><summary>✅ Answer</summary>

**C.** shared_buffers, PostgreSQL's shared page cache

- A: That changes the planner's cost estimates, not how much data stays in memory.
- B: work_mem helps sorts and hashes avoid spilling, not cache hits on index pages.
- C: Correct. A hit ratio below 99% on vector workloads suggests shared_buffers may be too small.
- D: Connection count doesn't size the shared cache.

shared_buffers controls PostgreSQL's shared memory cache. For vector workloads, it should hold the vector indexes and hot data; a hit ratio below 99% suggests it's too small. Azure tunes it by tier, within an allowed range.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 7. `lp5m3-007`

After you raise hnsw.ef_search on a shared server, product search improves, but nightly reports on the same server get slower. Which best practice from Learn does this show?

- **A.** Disable the vector index during report runs
- **B.** Set every memory parameter to its maximum for the tier
- **C.** Monitor for regressions in other workloads
- **D.** Leave parameters at their defaults on a shared server

<details><summary>💡 Hint</summary>

A change helped one workload and hurt another.

</details>

<details><summary>✅ Answer</summary>

**C.** Monitor for regressions in other workloads

- A: That would break product search instead of addressing the trade-off.
- B: Maximum values aren't a tuning strategy, and they risk memory problems.
- C: Correct. Parameters that help vector search can harm other workloads, so watch overall system health after changes.
- D: Learn encourages tuning, with measurement and monitoring.

Best practices: measure with EXPLAIN ANALYZE and Azure Monitor, monitor for regressions because vector tuning can hurt other workloads, and document what you changed and why.

📘 Source: [Tune PostgreSQL for pgvector](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/2-tune-postgresql-pgvector)

</details>

## 8. `lp5m3-008`

A recommendation engine with two million products must reach 99%+ recall at low latency, the data is mostly read, and memory is ample. Which index fits best?

- **A.** A B-tree on the embedding
- **B.** An HNSW index
- **C.** No index (sequential scan)
- **D.** An IVFFlat index

<details><summary>💡 Hint</summary>

High recall, mostly reads, plenty of memory: the graph-based index.

</details>

<details><summary>✅ Answer</summary>

**B.** An HNSW index

- A: B-tree indexes don't support vector similarity.
- B: Correct. HNSW gives 99%+ recall and consistent latency for read-mostly workloads.
- C: Over 1M rows an index is essential.
- D: IVFFlat has a lower recall ceiling.

HNSW for high recall and read-mostly data; IVFFlat when memory or build time is tight.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 9. `lp5m3-009`

For a table with 5,000 rows of embeddings, what does Learn say about a vector index?

- **A.** DiskANN is the one index that works at this size
- **B.** It's essential; queries are unusable without one
- **C.** HNSW can't be built on fewer than 10,000 rows
- **D.** Its benefit is limited; a sequential scan may be fast enough

<details><summary>💡 Hint</summary>

With very few rows, scanning them all may already be fast enough.

</details>

<details><summary>✅ Answer</summary>

**D.** Its benefit is limited; a sequential scan may be fast enough

- A: DiskANN targets very large datasets.
- B: That's the guidance for more than one million rows.
- C: HNSW can even be built on an empty table.
- D: Correct. Under 10,000 rows, the benefit is limited.

Index benefit grows with table size: limited under 10k, essential above 1M.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 10. `lp5m3-010`

For each statement, select Yes if the statement is true. Otherwise, select No. An HNSW index is created with `m = 16, ef_construction = 64`.

| Statement | Yes / No |
|---|---|
| ef_construction of 64 meets Learn's guidance of at least 2 × m. | ☐ |
| Raising ef_construction later changes query time without rebuilding. | ☐ |
| Raising hnsw.ef_search at query time doesn't require a rebuild. | ☐ |

<details><summary>💡 Hint</summary>

ef_construction should be at least twice m. Build settings need a rebuild; query settings don't.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| ef_construction of 64 meets Learn's guidance of at least 2 × m. | Yes | 2 × 16 = 32, and 64 is 4 × m. |
| Raising ef_construction later changes query time without rebuilding. | No | Changing m or ef_construction requires rebuilding; ef_construction affects build time and quality. |
| Raising hnsw.ef_search at query time doesn't require a rebuild. | Yes | ef_search is a runtime setting. |

Build-time parameters (m, ef_construction) need a rebuild; ef_search is set per session.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 11. `lp5m3-011`

A catalog reloads large batches of products every night, and the database has limited memory. Which index type does Learn suggest?

- **A.** No index
- **B.** HNSW with m = 64
- **C.** IVFFlat
- **D.** HNSW with ef_construction = 400

<details><summary>💡 Hint</summary>

Frequent rebuilds and little memory favor the index that builds fast and stores centroids.

</details>

<details><summary>✅ Answer</summary>

**C.** IVFFlat

- A: Large catalogs still need an index for interactive queries.
- B: Higher m increases memory, which is limited here.
- C: Correct. IVFFlat suits limited memory and frequent bulk updates, with faster builds.
- D: Higher ef_construction lengthens builds further.

IVFFlat trades some recall for lower memory and faster builds.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 12. `lp5m3-012`

You must build a vector index on a busy production table without blocking writes, and track its progress. Which two actions are correct? (Select two.)

- **A.** Use REINDEX INDEX without CONCURRENTLY
- **B.** Temporarily set ivfflat.probes to 1
- **C.** Use CREATE INDEX CONCURRENTLY
- **D.** Watch pg_stat_progress_create_index

<details><summary>💡 Hint</summary>

Build without blocking writes, and use a system view to follow the build.

</details>

<details><summary>✅ Answer</summary>

**C.** Use CREATE INDEX CONCURRENTLY  
**D.** Watch pg_stat_progress_create_index

- A: Plain REINDEX blocks writes.
- B: probes is a query-time setting unrelated to builds.
- C: Correct. CONCURRENTLY allows writes during the build.
- D: Correct. It shows phase, blocks and tuples done.

Index builds lock writes by default; CONCURRENTLY takes longer but avoids downtime.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 13. `lp5m3-013`

You created an HNSW index a month ago, but you suspect queries aren't using it. Which check does Learn describe?

- **A.** Run ANALYZE and assume the index is used afterwards
- **B.** Query pg_stat_user_indexes and look at idx_scan for the index
- **C.** Compare the index size with the table size
- **D.** Check pg_stat_progress_create_index for the index

<details><summary>💡 Hint</summary>

PostgreSQL keeps usage counters for each index.

</details>

<details><summary>✅ Answer</summary>

**B.** Query pg_stat_user_indexes and look at idx_scan for the index

- A: ANALYZE refreshes statistics, but it doesn't tell you whether the index was used.
- B: Correct. Low idx_scan counts suggest the index isn't being used, so check the operator class.
- C: Size doesn't show whether queries use the index.
- D: That view tracks index builds in progress, not later usage.

Check index health with pg_stat_user_indexes: pg_relation_size for size, and idx_scan / idx_tup_read for usage. Low idx_scan means the index isn't used; verify the query operator matches the index operator class.

📘 Source: [Choose and configure vector indexes](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/3-choose-configure-vector-indexes)

</details>

## 14. `lp5m3-014`

Almost every recommendation query includes `WHERE in_stock = true`. Which index reduces size and maintenance for this pattern?

- **A.** A partial index with WHERE in_stock = true
- **B.** A B-tree index on every column
- **C.** A second HNSW index on the embedding
- **D.** A GIN index on the attributes JSONB column

<details><summary>💡 Hint</summary>

Most queries share one condition. An index can cover only those rows.

</details>

<details><summary>✅ Answer</summary>

**A.** A partial index with WHERE in_stock = true

- A: Correct. A partial index covers only in-stock rows and is used for queries with that condition.
- B: Indexing everything raises write and storage costs.
- C: An extra vector index doesn't help this filter.
- D: GIN helps containment queries on JSONB.

Partial indexes suit filters that nearly every query shares.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 15. `lp5m3-015`

Products store price inside a JSONB attributes column with a GIN index, and queries filter `(attributes->>'price')::numeric BETWEEN 100 AND 500`. They're slow. What should you add?

- **A.** An expression index on the extracted price
- **B.** An HNSW index on the attributes JSONB column
- **C.** A second GIN index on the same attributes column
- **D.** A partial index WHERE price > 0 on the table

<details><summary>💡 Hint</summary>

A GIN index on JSONB doesn't help a numeric range on one extracted value.

</details>

<details><summary>✅ Answer</summary>

**A.** An expression index on the extracted price

- A: Correct. An expression index enables range queries on that JSONB field.
- B: HNSW indexes vectors, not JSONB.
- C: GIN doesn't accelerate range queries.
- D: price isn't a column here, and the filter isn't selective.

GIN serves containment; expression or structured-column B-tree indexes serve ranges.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 16. `lp5m3-016`

For each statement, select Yes if the statement is true. Otherwise, select No. A products table has a B-tree index on `(category_id, price)` and three vector columns.

| Statement | Yes / No |
|---|---|
| The index helps WHERE category_id = 5 AND price < 100. | ☐ |
| The index helps WHERE price < 100 on its own. | ☐ |
| One HNSW index can cover all three vector columns. | ☐ |

<details><summary>💡 Hint</summary>

Composite B-trees need their leading column. Each vector column needs its own index.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The index helps WHERE category_id = 5 AND price < 100. | Yes | Filters on the leftmost columns use the index. |
| The index helps WHERE price < 100 on its own. | No | price isn't the leftmost column. |
| One HNSW index can cover all three vector columns. | No | Each vector column needs its own index. |

Composite B-tree indexes serve leading-column filters; vector indexes are per column.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 17. `lp5m3-017`

User-activity embeddings arrive daily and grow to 80 million rows. Old months are dropped, queries filter by date, and rebuilding one index takes hours. What does Learn suggest?

- **A.** Store each day's vectors in a separate database
- **B.** Range-partition by date, creating indexes on the parent
- **C.** Use a single unpartitioned table with a larger HNSW m
- **D.** Move all vectors into one JSONB column

<details><summary>💡 Hint</summary>

Huge, growing tables filtered by date, with old data dropped, suit partitioning.

</details>

<details><summary>✅ Answer</summary>

**B.** Range-partition by date, creating indexes on the parent

- A: Separate databases block cross-day queries and joins.
- B: Correct. Date-range partitions prune scans, drop old data easily and keep per-partition indexes manageable.
- C: A denser graph makes builds even longer.
- D: JSONB doesn't hold or index vectors for similarity search.

Indexes created on the parent table are created on every partition and can be rebuilt independently.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 18. `lp5m3-018`

Every recommendation query filters on brand and release year, which are stored inside a JSONB attributes column. The filters are slow. The attributes are known when you design the schema. What does Learn suggest?

- **A.** Turn brand and release year into extra vector dimensions
- **B.** Drop the filters and sort by vector distance only
- **C.** Add more vector indexes on the embedding column
- **D.** Move them into structured columns with B-tree indexes

<details><summary>💡 Hint</summary>

Use JSONB for flexible attributes. What should you use for attributes you always filter on?

</details>

<details><summary>✅ Answer</summary>

**D.** Move them into structured columns with B-tree indexes

- A: Vectors capture meaning. Exact filters belong in structured columns.
- B: That changes the results, which isn't acceptable.
- C: The bottleneck is the metadata filter, not the vector search.
- D: Correct. Native columns give efficient B-tree indexes and accurate planner statistics for frequent filters.

Structured columns with native types allow efficient B-tree indexes, type safety and accurate statistics. Use them for attributes known at design time that you frequently filter or sort on.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 19. `lp5m3-019`

Your embedding model can output 768 or 1,536 dimensions, and tests show 768 gives acceptable quality. You also want to catch any inserts from the wrong model. How should you define the column?

- **A.** embedding vector, with no dimension, so that any model works
- **B.** embedding vector(1536), padding the 768 values with zeros
- **C.** embedding vector(768)
- **D.** embedding JSONB, so that dimensions can vary

<details><summary>💡 Hint</summary>

Lower dimensions save cost. A fixed size in the column definition acts as validation.

</details>

<details><summary>✅ Answer</summary>

**C.** embedding vector(768)

- A: Without a dimension, mismatched vectors aren't caught at insert time.
- B: Padding wastes storage and hides a model mismatch.
- C: Correct. Fewer dimensions cut storage and compute, and an explicit size makes mismatched inserts fail.
- D: JSONB can't use pgvector operators or vector indexes.

Lower dimensions reduce storage and computation while keeping reasonable quality for many use cases. Declaring vector(768) validates inserts: vectors with other dimensions fail.

📘 Source: [Optimize data layout](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/4-optimize-data-layout)

</details>

## 20. `lp5m3-020`

How many read replicas can an Azure Database for PostgreSQL primary have?

- **A.** Up to ten
- **B.** Up to two
- **C.** Unlimited
- **D.** Up to five

<details><summary>💡 Hint</summary>

There's a fixed limit on read replicas per primary.

</details>

<details><summary>✅ Answer</summary>

**D.** Up to five

- A: Learn gives a lower number.
- B: Learn gives a higher number.
- C: There's a limit of five.
- D: Correct. You can create up to five read replicas per primary.

Replicas can be in other regions and each has its own endpoint.

📘 Source: [Scale for high-volume workloads](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/5-scale-high-volume-workloads)

</details>

## 21. `lp5m3-021`

A user saves new preferences and the next page shows recommendations based on them. Similarity searches are routed to read replicas. Where should the preference read go?

- **A.** To the primary server
- **B.** To the closest read replica
- **C.** To any replica, because replication is synchronous
- **D.** To the Redis cache with a 60-minute TTL

<details><summary>💡 Hint</summary>

Replicas lag slightly. A read that must see the user's own write goes to the primary.

</details>

<details><summary>✅ Answer</summary>

**A.** To the primary server

- A: Correct. Replicas apply changes asynchronously; reads needing immediate consistency go to the primary.
- B: The replica may not have the update yet.
- C: Replication is asynchronous.
- D: A 60-minute cache could serve stale preferences.

Route staleness-tolerant similarity searches to replicas and read-your-writes queries to the primary.

📘 Source: [Scale for high-volume workloads](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/5-scale-high-volume-workloads)

</details>

## 22. `lp5m3-022`

Which two are good caching candidates for a vector recommendation service, according to Learn? (Select two.)

- **A.** Embedding lookups for popular products
- **B.** Precomputed "similar items" for top products
- **C.** Inventory counts that change every second
- **D.** Arbitrary similarity queries with user-typed text

<details><summary>💡 Hint</summary>

Cache things that are popular and expensive to compute.

</details>

<details><summary>✅ Answer</summary>

**A.** Embedding lookups for popular products  
**B.** Precomputed "similar items" for top products

- A: Correct. Frequently requested and slow to change.
- B: Correct. Bounded key space, frequent requests, low change rate.
- C: Rapidly changing data causes constant invalidation.
- D: Arbitrary queries have an infinite key space.

Cache what's requested often, changes slowly and has bounded keys.

📘 Source: [Scale for high-volume workloads](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/5-scale-high-volume-workloads)

</details>

## 23. `lp5m3-023`

For each statement, select Yes if the statement is true. Otherwise, select No. A Memory Optimized server runs at 25% average CPU for months with low memory use, and the baseline load is predictable.

| Statement | Yes / No |
|---|---|
| Learn suggests considering a scale-down. | ☐ |
| General Purpose might suffice if memory use stays low. | ☐ |
| Reserved capacity discounts apply only to burst capacity above the baseline. | ☐ |
| The next step should be adding read replicas to spread the load. | ☐ |

<details><summary>💡 Hint</summary>

Low steady usage means you may be paying for more than you need.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Learn suggests considering a scale-down. | Yes | If average CPU is below 30%, consider scaling down. |
| General Purpose might suffice if memory use stays low. | Yes | Consistently low memory use suggests General Purpose may be enough. |
| Reserved capacity discounts apply only to burst capacity above the baseline. | No | Reserve the baseline; use on-demand pricing for bursts. |
| The next step should be adding read replicas to spread the load. | No | The server is underused; replicas address volume a single server can't handle. |

Review utilization regularly, right-size, and reserve the baseline.

📘 Source: [Scale for high-volume workloads](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/5-scale-high-volume-workloads)

</details>

## 24. `lp5m3-024`

Single vector queries are slow, and memory pressure is causing heavy disk I/O. The server isn't yet at its tier's maximum size, and total query volume is modest. What does Learn suggest first?

- **A.** Add a cache in front of the database
- **B.** Scale up to a larger server
- **C.** Add read replicas
- **D.** Partition the table by tenant

<details><summary>💡 Hint</summary>

Is the problem total volume, or each query on its own?

</details>

<details><summary>✅ Answer</summary>

**B.** Scale up to a larger server

- A: Caching helps with repeated reads at high volume, not with slow single queries caused by memory pressure.
- B: Correct. Scale up when single-query latency is high, memory pressure causes disk I/O, and you haven't hit the tier's limits.
- C: Replicas help when total volume is high. These queries are slow one at a time.
- D: Partitioning helps very large tables with a natural partition key, which isn't the problem here.

Scale up when single-query latency is too high, memory pressure causes disk I/O, or you're below the tier maximum. Scale out (replicas or caching) when total volume exceeds one server or the workload is read-heavy with acceptable staleness.

📘 Source: [Scale for high-volume workloads](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/5-scale-high-volume-workloads)

</details>

## 25. `lp5m3-025`

With PgBouncer in transaction mode, a query needs hnsw.ef_search = 200 for one high-accuracy search. How should the code set it?

- **A.** SET LOCAL hnsw.ef_search = 200 in the transaction
- **B.** SET hnsw.ef_search = 200 once when the app first starts
- **C.** Pass ef_search in the connection string to port 5432
- **D.** ALTER SYSTEM SET hnsw.ef_search = 200

<details><summary>💡 Hint</summary>

In transaction mode, a plain SET might not stay on your connection. Scope the setting to the transaction.

</details>

<details><summary>✅ Answer</summary>

**A.** SET LOCAL hnsw.ef_search = 200 in the transaction

- A: Correct. SET LOCAL applies to the current transaction and reverts afterwards, which is safe with pooling.
- B: Session settings don't persist across transactions in transaction mode.
- C: Bypassing PgBouncer defeats the pooling.
- D: A server-wide change affects every query.

Use SET LOCAL for per-query work_mem, ef_search or probes with pooled connections.

📘 Source: [Connection optimization](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/6-connection-optimization)

</details>

## 26. `lp5m3-026`

Ten app instances share a database that allows 1,000 connections. Following Learn's guidance, what maximum pool size should each instance use?

- **A.** About 100, leaving headroom
- **B.** 10 each
- **C.** 1,000 each
- **D.** 5,000 each through PgBouncer

<details><summary>💡 Hint</summary>

Divide the server's connection limit across instances, and leave some headroom.

</details>

<details><summary>✅ Answer</summary>

**A.** About 100, leaving headroom

- A: Correct. Cap each instance at the database limit divided by the number of instances, with headroom.
- B: That's far smaller than needed and causes waiting.
- C: Ten instances at 1,000 each would far exceed the limit.
- D: max_client_conn is a PgBouncer client setting, not each app pool's maximum.

Max pool size per instance ≈ database connections ÷ instances.

📘 Source: [Connection optimization](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/6-connection-optimization)

</details>

## 27. `lp5m3-027`

For each statement, select Yes if the statement is true. Otherwise, select No. An app moves from direct connections to PgBouncer in transaction mode.

| Statement | Yes / No |
|---|---|
| A LISTEN/NOTIFY channel for cache invalidation keeps working. | ☐ |
| A named prepared statement from one transaction might not exist in the next. | ☐ |
| Settings applied with plain SET persist for the rest of the client session. | ☐ |
| Retries for OperationalError should add random jitter to the backoff. | ☐ |

<details><summary>💡 Hint</summary>

Transaction mode hands connections around, so session-level features break.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A LISTEN/NOTIFY channel for cache invalidation keeps working. | No | LISTEN/NOTIFY requires persistent connections and doesn't work with transaction pooling. |
| A named prepared statement from one transaction might not exist in the next. | Yes | Different server connections may be assigned between transactions. |
| Settings applied with plain SET persist for the rest of the client session. | No | Session variables reset between transactions; use SET LOCAL. |
| Retries for OperationalError should add random jitter to the backoff. | Yes | Jitter stops instances retrying at the same moment. |

Transaction pooling cuts connections but changes session behavior.

📘 Source: [Connection optimization](https://learn.microsoft.com/en-us/training/modules/optimize-vector-search-azure-database-postgresql/6-connection-optimization)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
