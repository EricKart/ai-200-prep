# Practice: LP4 · M3 Optimize query performance for Azure Cosmos DB for NoSQL

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp4m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-4/optimize-query-performance-azure-cosmos-db)

## 1. `lp4m3-001`

Which index type does a query that uses ST_DISTANCE to find nearby points of interest need?

- **A.** Spatial index
- **B.** Composite index
- **C.** Range index
- **D.** Vector index

<details><summary>💡 Hint</summary>

Distance between coordinates needs a geography-aware index.

</details>

<details><summary>✅ Answer</summary>

**A.** Spatial index

- A: Correct. Spatial indexes support ST_DISTANCE, ST_WITHIN and ST_INTERSECTS.
- B: Composite indexes handle multi-property sorting and filters.
- C: Range indexes handle equality, ranges and single-property ORDER BY.
- D: Vector indexes support VectorDistance.

Pick the index type by the query function: spatial for geo, vector for similarity.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 2. `lp4m3-002`

What is the default indexing mode for a new Cosmos DB container?

- **A.** lazy
- **B.** consistent
- **C.** none
- **D.** eventual

<details><summary>💡 Hint</summary>

The default mode updates indexes in step with every write.

</details>

<details><summary>✅ Answer</summary>

**B.** consistent

- A: Lazy is deprecated and new containers can't use it.
- B: Correct. Consistent updates indexes synchronously with each write and is the default.
- C: None disables indexing.
- D: Eventual is a consistency level, not an indexing mode.

Consistent mode keeps queries in step with committed writes.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 3. `lp4m3-003`

Which path indexes only the scalar value of a top-level property named title?

- **A.** /title/[]
- **B.** /*/title
- **C.** /title/*
- **D.** /title/?

<details><summary>💡 Hint</summary>

A path ending in /? means just this value. /* means everything below it.

</details>

<details><summary>✅ Answer</summary>

**D.** /title/?

- A: /[] indexes array elements.
- B: That isn't valid index path syntax.
- C: /* indexes everything under the path.
- D: Correct. /? indexes the scalar value at the property.

/? = scalar, /[] = array elements, /* = everything under the path.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 4. `lp4m3-004`

For each statement, select Yes if the statement is true. Otherwise, select No. A container uses partition key `/tenantId` and a selective policy with `/*` in excludedPaths.

| Statement | Yes / No |
|---|---|
| The tenantId path is indexed automatically anyway. | ☐ |
| id and _ts remain indexed even though /* is excluded. | ☐ |
| With /* excluded, every property is still range-indexed by default. | ☐ |
| If /* is excluded and /title/? is included, title is indexed because the more specific path wins. | ☐ |

<details><summary>💡 Hint</summary>

id and _ts are always indexed. Excluding /* means you must opt in to everything else.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The tenantId path is indexed automatically anyway. | No | The partition key isn't indexed automatically unless it's /id; include it explicitly. |
| id and _ts remain indexed even though /* is excluded. | Yes | id and _ts are always indexed in consistent mode. |
| With /* excluded, every property is still range-indexed by default. | No | Excluding /* means only explicitly included paths (plus id and _ts) are indexed. |
| If /* is excluded and /title/? is included, title is indexed because the more specific path wins. | Yes | The more specific path takes precedence. |

Selective policies must explicitly include every queried property, including the partition key.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 5. `lp4m3-005`

A container is used only as a key-value store: items are read by id and partition key, and bulk writes must be as fast as possible. Which indexing mode fits?

- **A.** consistent
- **B.** lazy
- **C.** consistent, with just /_ts in includedPaths
- **D.** none

<details><summary>💡 Hint</summary>

No queries except point reads, and writes must be fast. Indexing can be switched off entirely.

</details>

<details><summary>✅ Answer</summary>

**D.** none

- A: Consistent adds index work to each write you don't need here.
- B: Lazy is deprecated and unavailable for new containers.
- C: id and _ts are always indexed in consistent mode anyway, so this still maintains indexes.
- D: Correct. None treats the container as a pure key-value store and can speed up bulk writes.

Use none only when you never query by secondary properties; queries would otherwise do full scans.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 6. `lp4m3-006`

An old container still uses the lazy indexing mode, and a teammate wants to create a new container with the same setting. What should you tell them?

- **A.** Lazy indexing works only with shared database throughput
- **B.** Lazy indexing is deprecated: new containers can't use it, and existing ones should move to consistent
- **C.** Lazy indexing is the recommended mode for AI workloads with heavy writes
- **D.** Lazy indexing is the default for containers created from the portal

<details><summary>💡 Hint</summary>

One of the indexing modes is no longer offered.

</details>

<details><summary>✅ Answer</summary>

**B.** Lazy indexing is deprecated: new containers can't use it, and existing ones should move to consistent

- A: Throughput mode isn't the issue. Lazy indexing is deprecated.
- B: Correct. Lazy mode is deprecated, so migrate existing containers to consistent.
- C: Lazy mode is deprecated. For write-heavy key-value use, Learn discusses the none mode.
- D: The default indexing mode is consistent.

Azure Cosmos DB previously supported lazy indexing. It's deprecated: new containers can't use it, and existing containers with lazy indexing should migrate to consistent mode.

📘 Source: [Understand indexes in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/2-understand-indexes-cosmos-db)

</details>

## 7. `lp4m3-007`

A query runs `ORDER BY c.relevanceScore DESC, c.uploadDate DESC` and fails with an error. What does it need?

- **A.** A range index on relevanceScore and another on uploadDate
- **B.** A composite index (relevanceScore DESC, uploadDate DESC)
- **C.** A tuple index covering both of the sorted properties
- **D.** A spatial index on uploadDate for the date sort

<details><summary>💡 Hint</summary>

Sorting on two properties needs one index that covers both, in that order.

</details>

<details><summary>✅ Answer</summary>

**B.** A composite index (relevanceScore DESC, uploadDate DESC)

- A: ORDER BY on two properties needs a composite index, not a single range index.
- B: Correct. The composite index must match the property sequence and directions.
- C: Tuple indexes are for properties inside array elements.
- D: Spatial indexes are for geospatial functions.

Multi-property ORDER BY requires a matching composite index.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 8. `lp4m3-008`

For each statement, select Yes if the statement is true. Otherwise, select No. A container has one composite index: `(relevanceScore DESC, uploadDate DESC)`.

| Statement | Yes / No |
|---|---|
| It serves ORDER BY c.relevanceScore ASC, c.uploadDate ASC. | ☐ |
| It serves ORDER BY c.relevanceScore DESC, c.uploadDate ASC. | ☐ |
| It serves ORDER BY c.uploadDate DESC, c.relevanceScore DESC. | ☐ |

<details><summary>💡 Hint</summary>

A composite index serves its exact order and the full reverse, and nothing else.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| It serves ORDER BY c.relevanceScore ASC, c.uploadDate ASC. | Yes | Composite indexes support the exact opposite order on all paths. |
| It serves ORDER BY c.relevanceScore DESC, c.uploadDate ASC. | No | Mixed orders need a separate composite index. |
| It serves ORDER BY c.uploadDate DESC, c.relevanceScore DESC. | No | The property sequence must match. |

Same sequence; same directions or the exact reverse.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 9. `lp4m3-009`

A query filters `category = 'reports' AND department = 'finance' AND createdDate > '2024-06-01'`. How should the composite index be ordered?

- **A.** category, department, createdDate
- **B.** createdDate, category, department
- **C.** department, createdDate, category
- **D.** A single range index on createdDate

<details><summary>💡 Hint</summary>

Equality filters first, the range filter last.

</details>

<details><summary>✅ Answer</summary>

**A.** category, department, createdDate

- A: Correct. Equality filters first, the single range filter last.
- B: The range filter must be last.
- C: The range filter can't be in the middle.
- D: A single range index doesn't optimize the combined filter as well.

Place equality filters first; each composite index supports one range filter, and it goes last.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 10. `lp4m3-010`

You're replacing composite index X with a better composite index Y on a busy container with millions of items. What order of steps keeps queries supported?

- **A.** Switch indexing mode to none, then add Y afterward
- **B.** Add Y and remove X together in one policy update
- **C.** Remove X first, then add Y in a second update
- **D.** Add Y, wait for the transformation, then remove X

<details><summary>💡 Hint</summary>

Removing an index takes effect at once. Adding one takes effect only after the transformation.

</details>

<details><summary>✅ Answer</summary>

**D.** Add Y, wait for the transformation, then remove X

- A: Mode none disables indexing entirely.
- B: X would stop being used immediately while Y is still being built.
- C: Removing X takes effect immediately, so queries scan until Y is built.
- D: Correct. Add the new index first, wait, then remove the old one.

Added indexes help only after transformation; removed ones stop being used right away.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 11. `lp4m3-011`

Documents store chunks as an array of objects with position and tokens. Queries filter on both properties within the same chunk. Which path improves this?

- **A.** /chunks/position/? and /chunks/tokens/?
- **B.** /chunks/[]/{position, tokens}/?
- **C.** /chunks/*
- **D.** A composite index on (/position, /tokens)

<details><summary>💡 Hint</summary>

Indexing several properties of the same array element uses a special path syntax.

</details>

<details><summary>✅ Answer</summary>

**B.** /chunks/[]/{position, tokens}/?

- A: Those paths aren't array-element paths.
- B: Correct. A tuple index indexes the property combination within each array element.
- C: /chunks/* indexes everything separately, not the combination per element.
- D: Composite indexes on top-level paths don't index combinations inside array elements.

Tuple indexes suit chunked documents filtered on chunk position, size or other metadata.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 12. `lp4m3-012`

You added a composite index to a container with millions of items an hour ago, but the slow query costs the same RUs. Nothing else changed. What's the most likely reason?

- **A.** Composite indexes don't reduce RU cost
- **B.** The index transformation hasn't finished, so queries can't use the new index yet
- **C.** The query must name the index in a hint
- **D.** The container needs a restart before new indexes load

<details><summary>💡 Hint</summary>

Changing an indexing policy starts background work. Can large containers take hours?

</details>

<details><summary>✅ Answer</summary>

**B.** The index transformation hasn't finished, so queries can't use the new index yet

- A: They do once they're built and match the query.
- B: Correct. Index changes apply asynchronously, and new indexes help only after the transformation completes.
- C: Cosmos DB picks indexes automatically. There's no index hint to add.
- D: Cosmos DB containers aren't restarted. The transformation runs in the background.

Index changes run as an asynchronous transformation. New indexes don't improve queries until it completes, which can take hours on large containers. Track progress in the portal or CLI.

📘 Source: [Configure range and composite indexes](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/3-configure-range-composite-indexes)

</details>

## 13. `lp4m3-013`

You upgrade from a 1,536-dimension embedding model to text-embedding-3-large (3,072 dimensions). What must you do in Cosmos DB?

- **A.** Create a new container with an updated vector policy and migrate
- **B.** Increase quantizationByteSize to 512
- **C.** Edit the dimensions in the existing vector policy
- **D.** Change the vector index type to flat

<details><summary>💡 Hint</summary>

Can the vector embedding policy be changed in place?

</details>

<details><summary>✅ Answer</summary>

**A.** Create a new container with an updated vector policy and migrate

- A: Correct. Different dimensions require a new container and data migration.
- B: Index tuning doesn't change the policy's dimensions.
- C: Vector policies can't be modified after creation.
- D: flat supports at most 505 dimensions.

Plan dimensions, data type and distance function up front; vector policies are immutable.

📘 Source: [Tune vector indexes for embedding workloads](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/4-tune-vector-indexes-embeddings)

</details>

## 14. `lp4m3-014`

Users always filter by category first, and each category holds a few hundred 384-dimension vectors. They want exact results. Which vector index fits?

- **A.** flat
- **B.** diskANN
- **C.** quantizedFlat
- **D.** none

<details><summary>💡 Hint</summary>

Small, pre-filtered sets and exact results: brute force over few vectors is fine.

</details>

<details><summary>✅ Answer</summary>

**A.** flat

- A: Correct. Flat gives exact results and works well when filters shrink the candidate set (and 384 ≤ 505 dims).
- B: diskANN is approximate and aimed at large datasets.
- C: quantizedFlat trades slight accuracy for speed.
- D: Without a vector index, similarity queries scan everything; flat is the right index here.

Flat indexes suit small candidate sets and exact-accuracy needs.

📘 Source: [Tune vector indexes for embedding workloads](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/4-tune-vector-indexes-embeddings)

</details>

## 15. `lp4m3-015`

For each statement, select Yes if the statement is true. Otherwise, select No. A team tunes a diskANN index on a large embedding collection.

| Statement | Yes / No |
|---|---|
| Raising indexingSearchListSize can improve index quality but slows index builds. | ☐ |
| indexingSearchListSize also applies to quantizedFlat indexes. | ☐ |
| Most applications perform well with the default parameters. | ☐ |
| indexingSearchListSize can be set as high as 5,000. | ☐ |

<details><summary>💡 Hint</summary>

Most apps need no tuning. A bigger search list means better quality but slower builds, and it applies to diskANN.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Raising indexingSearchListSize can improve index quality but slows index builds. | Yes | Higher values improve quality and accuracy but take longer to build. |
| indexingSearchListSize also applies to quantizedFlat indexes. | No | It's a diskANN-only parameter. |
| Most applications perform well with the default parameters. | Yes | Tune only if you observe accuracy issues or need specific latency targets. |
| indexingSearchListSize can be set as high as 5,000. | No | Valid values range from 10 to 500 (default 100). |

Defaults are usually fine; quantizationByteSize applies to both, indexingSearchListSize only to diskANN.

📘 Source: [Tune vector indexes for embedding workloads](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/4-tune-vector-indexes-embeddings)

</details>

## 16. `lp4m3-016`

Search quality on a quantizedFlat index is slightly below target, and the team can accept more storage. Which vector index setting should they raise?

- **A.** The policy's dimensions, above the model's output size
- **B.** The container's partition count
- **C.** indexingSearchListSize on the quantizedFlat index
- **D.** quantizationByteSize

<details><summary>💡 Hint</summary>

Quantization compresses vectors. Which setting controls how much is kept?

</details>

<details><summary>✅ Answer</summary>

**D.** quantizationByteSize

- A: Dimensions must match the embedding model.
- B: Partitions don't control how much vectors are compressed.
- C: indexingSearchListSize is a diskANN setting.
- D: Correct. Larger values keep more information, which improves accuracy at the cost of storage and possibly throughput.

quantizationByteSize controls how much compression is applied. Larger values preserve more information and improve accuracy, with more storage and possibly lower throughput. The default is chosen dynamically.

📘 Source: [Tune vector indexes for embedding workloads](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/4-tune-vector-indexes-embeddings)

</details>

## 17. `lp4m3-017`

Query metrics show 48,000 retrieved documents and 25 output documents for a frequent query. What does this suggest?

- **A.** Filtering is inefficient, so an index is likely missing
- **B.** The container has too many vector indexes
- **C.** The query uses too strong a consistency level
- **D.** The partition key has too many distinct values

<details><summary>💡 Hint</summary>

Many documents read but few returned means the filter isn't using an index.

</details>

<details><summary>✅ Answer</summary>

**A.** Filtering is inefficient, so an index is likely missing

- A: Correct. A high retrieved-to-output ratio points to inefficient filtering; check indexes.
- B: Vector indexes don't cause scans of metadata filters.
- C: Consistency affects replica reads, not this ratio.
- D: High cardinality is good for partition keys.

Use index utilization and retrieved vs output counts to find missing indexes.

📘 Source: [Reduce RU costs with strategic indexing](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/5-reduce-ru-costs-strategic-indexing)

</details>

## 18. `lp4m3-018`

An IoT ingestion pipeline writes thousands of documents per second and queries them once a day for a report. What indexing strategy fits?

- **A.** Index every property with /* and add many composite indexes
- **B.** Index minimally: only the few properties the daily query needs
- **C.** Switch to bounded staleness to reduce write cost
- **D.** Use comprehensive composite indexes because AI apps are read-heavy

<details><summary>💡 Hint</summary>

Heavy writes and rare reads: every indexed path costs on each write.

</details>

<details><summary>✅ Answer</summary>

**B.** Index minimally: only the few properties the daily query needs

- A: Every index raises write latency and RUs.
- B: Correct. Write-heavy workloads benefit from minimal indexing.
- C: Consistency doesn't change write RU cost per operation.
- D: This workload is write-heavy, not read-heavy.

Write-heavy → minimal indexes; read-heavy → comprehensive indexes.

📘 Source: [Reduce RU costs with strategic indexing](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/5-reduce-ru-costs-strategic-indexing)

</details>

## 19. `lp4m3-019`

A document has title, documentType, category, uploadDate, a large content field, summary and an embedding. Queries filter on documentType, category and uploadDate and show content and summary. Which two belong in the indexing policy? (Select two.)

- **A.** /content/? in includedPaths
- **B.** /documentType/? in includedPaths
- **C.** /summary/? in includedPaths
- **D.** A vector index on /embedding

<details><summary>💡 Hint</summary>

Index only what you filter on, and think about what the embedding needs instead of range indexing.

</details>

<details><summary>✅ Answer</summary>

**B.** /documentType/? in includedPaths  
**D.** A vector index on /embedding

- A: content is only displayed; don't index it.
- B: Correct. documentType is filtered, so index it.
- C: summary is only displayed; don't index it.
- D: Correct. Embedding search uses a vector index, not a range index.

Index the properties used in queries plus a vector index; exclude display-only fields.

📘 Source: [Reduce RU costs with strategic indexing](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/5-reduce-ru-costs-strategic-indexing)

</details>

## 20. `lp4m3-020`

Query metrics show a high ratio of retrieved to output documents for a frequent query. You add the missing index. What should you do next, following Learn's workflow?

- **A.** Immediately remove the old indexes to save write RUs
- **B.** Wait for the transformation to complete, then measure the query's RU cost again
- **C.** Switch the account to strong consistency to make the index take effect
- **D.** Recreate the container so that the index applies to existing items

<details><summary>💡 Hint</summary>

An index change isn't instant. What proves it worked?

</details>

<details><summary>✅ Answer</summary>

**B.** Wait for the transformation to complete, then measure the query's RU cost again

- A: Removing indexes too early can make other queries fall back to scans.
- B: Correct. Create the index, wait for the transformation, then measure again to confirm the improvement.
- C: Consistency doesn't control when indexes take effect.
- D: Policy changes transform existing data in the background. You don't need a new container.

When metrics show low index utilization or high retrieved-to-output ratios, add or modify indexes, wait for the transformation to complete, and measure query costs again.

📘 Source: [Reduce RU costs with strategic indexing](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/5-reduce-ru-costs-strategic-indexing)

</details>

## 21. `lp4m3-021`

A user uploads a document and immediately searches for it in the same app. Which consistency level does Learn recommend for this read-your-writes need?

- **A.** Session
- **B.** Strong
- **C.** Eventual
- **D.** Consistent prefix

<details><summary>💡 Hint</summary>

The user needs to see their own write right away.

</details>

<details><summary>✅ Answer</summary>

**A.** Session

- A: Correct. Session guarantees read-your-writes within the session.
- B: Strong works but doubles read RUs and adds latency; Session is the recommended balance.
- C: Eventual may return stale data with no ordering.
- D: Consistent prefix guarantees order, not freshness.

Session suits most AI apps: users see their own uploads immediately.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

## 22. `lp4m3-022`

Which consistency levels read from two replicas and cost about twice the read RUs?

- **A.** Session and eventual
- **B.** Strong and bounded staleness
- **C.** Consistent prefix and session
- **D.** Bounded staleness and eventual

<details><summary>💡 Hint</summary>

Two levels read from two replicas.

</details>

<details><summary>✅ Answer</summary>

**B.** Strong and bounded staleness

- A: These read from one replica.
- B: Correct. Strong and bounded staleness read from two replicas (minority quorum).
- C: These read from one replica.
- D: Eventual reads from one replica.

Strong and bounded staleness reads cost 2×; the other levels 1×.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

## 23. `lp4m3-023`

Put the five Cosmos DB consistency levels in order from strongest to weakest.

- Bounded staleness
- Consistent prefix
- Eventual
- Session
- Strong

<details><summary>💡 Hint</summary>

From the strongest guarantee down to the weakest.

</details>

<details><summary>✅ Answer</summary>

1. Strong
2. Bounded staleness
3. Session
4. Consistent prefix
5. Eventual

Stronger levels give fresher reads at the cost of latency, availability and (for the top two) read RUs.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

## 24. `lp4m3-024`

For each statement, select Yes if the statement is true. Otherwise, select No. An upload service writes a document, and a separate search service queries it for the same user, both using Session consistency.

| Statement | Yes / No |
|---|---|
| The search service sees the new document only if it receives the session token from the upload. | ☐ |
| Session tokens are global and work for every partition. | ☐ |
| Writes under Session consistency cost more RUs than under Eventual. | ☐ |

<details><summary>💡 Hint</summary>

Session guarantees follow the session token, and they apply per partition.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The search service sees the new document only if it receives the session token from the upload. | Yes | Across services you must pass session tokens explicitly. |
| Session tokens are global and work for every partition. | No | Session tokens are partition-bound. |
| Writes under Session consistency cost more RUs than under Eventual. | No | Write RU costs don't vary by consistency level. |

Pass session tokens between services that handle the same user flow.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

## 25. `lp4m3-025`

A globally distributed app uses multiple write regions and asks for Strong consistency for payment records. What should you know?

- **A.** Strong costs the same read RUs as Session
- **B.** Strong guarantees reads at most K versions behind
- **C.** Strong isn't supported with multiple write regions
- **D.** Strong reads from a single replica

<details><summary>💡 Hint</summary>

One consistency level can't work with multiple write regions.

</details>

<details><summary>✅ Answer</summary>

**C.** Strong isn't supported with multiple write regions

- A: Strong reads cost 2× because they read from two replicas.
- B: That describes bounded staleness.
- C: Correct. Strong consistency with multiple write regions isn't supported.
- D: Strong reads from two replicas.

For multi-region writes, choose Session or weaker; Strong needs a single write region.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

## 26. `lp4m3-026`

An analytics job uses Eventual consistency. PBS metrics show it returns the latest data 99.6% of the time. What does Learn suggest?

- **A.** Move to bounded staleness to reduce read RUs
- **B.** Switch the job to Strong to remove the remaining 0.4%
- **C.** PBS measures Session reads, so ignore it here
- **D.** Eventual is probably safe for more operations

<details><summary>💡 Hint</summary>

Probabilistic bounded staleness shows how often weaker reads are already up to date.

</details>

<details><summary>✅ Answer</summary>

**D.** Eventual is probably safe for more operations

- A: Bounded staleness reads cost 2×, so it raises RUs.
- B: Strong doubles read RUs; analytics rarely needs it.
- C: PBS measures how often eventual reads return the latest data.
- D: Correct. If PBS shows current data more than 99% of the time, you might use eventual for more operations.

Use PBS metrics (Metrics → Consistency) to validate weaker consistency choices.

📘 Source: [Choose consistency levels for optimal performance](https://learn.microsoft.com/en-us/training/modules/optimize-query-performance-azure-cosmos-db/6-choose-consistency-levels-performance)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
