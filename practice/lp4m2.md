# Practice: LP4 · M2 Implement vector search on Azure Cosmos DB for NoSQL

> 26 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp4m2.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-4/implement-vector-search-azure-cosmos-db)

## 1. `lp4m2-001`

How many dimensions does Azure OpenAI's text-embedding-ada-002 model produce?

- **A.** 505
- **B.** 4,096
- **C.** 1,536
- **D.** 3,072

<details><summary>💡 Hint</summary>

This model's dimension count is also the default in the vector embedding policy.

</details>

<details><summary>✅ Answer</summary>

**C.** 1,536

- A: 505 is the flat index dimension limit.
- B: 4,096 is the quantizedFlat and diskANN dimension limit.
- C: Correct. ada-002 produces 1,536-dimensional vectors.
- D: 3,072 is text-embedding-3-large.

The dimensions in the vector policy must match the embedding model.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 2. `lp4m2-002`

Your container stores normalized Azure OpenAI embeddings for a support knowledge base. Which distance function does Learn recommend?

- **A.** hamming
- **B.** manhattan
- **C.** cosine
- **D.** euclidean

<details><summary>💡 Hint</summary>

Normalized embeddings compare well by angle. Which function measures angle?

</details>

<details><summary>✅ Answer</summary>

**C.** cosine

- A: Not a supported distance function.
- B: Not a supported distance function.
- C: Correct. Cosine handles normalized embeddings well and gives intuitive scores.
- D: Euclidean suits cases where magnitude matters; it's less common for text embeddings.

Supported: cosine (default), dotproduct, euclidean.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 3. `lp4m2-003`

A container holds 3 million product embeddings with 1,536 dimensions. Which vector index type fits best?

- **A.** flat
- **B.** A range index on /embedding
- **C.** quantizedFlat
- **D.** diskANN

<details><summary>💡 Hint</summary>

Millions of high-dimension vectors need approximate search built for scale.

</details>

<details><summary>✅ Answer</summary>

**D.** diskANN

- A: flat supports only up to 505 dimensions.
- B: Range indexes don't help embedding arrays; exclude them.
- C: quantizedFlat is recommended up to about 50,000 vectors per physical partition.
- D: Correct. DiskANN gives the best performance for millions of vectors, up to 4,096 dimensions.

flat for small/exact, quantizedFlat for moderate sizes, diskANN for large datasets.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 4. `lp4m2-004`

For each statement, select Yes if the statement is true. Otherwise, select No. You plan to add vector search to an existing `products` container that already has data.

| Statement | Yes / No |
|---|---|
| You can add a vector embedding policy to the existing container. | ☐ |
| The account needs the vector search feature enabled first. | ☐ |
| The feature must be requested through a support ticket and manually approved. | ☐ |
| Storing embeddings as float16 instead of float32 halves vector storage. | ☐ |

<details><summary>💡 Hint</summary>

Vector policies are set when a container is created, and the account feature comes first.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| You can add a vector embedding policy to the existing container. | No | Vector policies must be set at creation, and vector search is only supported on new containers. |
| The account needs the vector search feature enabled first. | Yes | Enable Vector Search for NoSQL API or EnableNoSQLVectorSearch. |
| The feature must be requested through a support ticket and manually approved. | No | It's auto-approved; it might take 15 minutes to take effect. |
| Storing embeddings as float16 instead of float32 halves vector storage. | Yes | float16 reduces storage by 50%. |

Plan vector policies before creating the container.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 5. `lp4m2-005`

Write costs are high on a vector container, and the indexing policy includes `/*` with no exclusions. What change does Learn recommend?

- **A.** Add the embedding path to excludedPaths
- **B.** Change dataType from float32 to uint8
- **C.** Disable automatic indexing for the container
- **D.** Switch the vector index from diskANN to flat

<details><summary>💡 Hint</summary>

Indexing every path includes a huge array that nobody filters on.

</details>

<details><summary>✅ Answer</summary>

**A.** Add the embedding path to excludedPaths

- A: Correct. Embedding arrays don't benefit from range indexes; including them wastes storage and raises write costs.
- B: uint8 needs quantized embeddings and doesn't remove range indexing.
- C: Turning off indexing breaks your filter queries.
- D: flat can't index 1,536 dimensions and doesn't fix range indexing.

Exclude the embedding path from standard range indexes and index it with a vector index instead.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 6. `lp4m2-006`

For each statement, select Yes if the statement is true. Otherwise, select No. A new container has a quantizedFlat index on `/embedding` and holds 300 vectors so far.

| Statement | Yes / No |
|---|---|
| The quantizedFlat index is fully effective at this size. | ☐ |
| Queries may fall back to full scans and cost more RUs until more vectors are added. | ☐ |
| The same policy can also index a second path, /titleEmbedding. | ☐ |

<details><summary>💡 Hint</summary>

Approximate indexes need a minimum number of vectors before they help.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The quantizedFlat index is fully effective at this size. | No | quantizedFlat and diskANN need at least 1,000 vectors before the index becomes effective. |
| Queries may fall back to full scans and cost more RUs until more vectors are added. | Yes | With fewer than 1,000 vectors, queries fall back to full scans. |
| The same policy can also index a second path, /titleEmbedding. | Yes | Multiple vector paths can be defined in one policy. |

Index types need enough vectors; multiple embedding paths are supported.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 7. `lp4m2-007`

For each statement, select Yes if the statement is true. Otherwise, select No. You write a vector embedding policy for /embedding and leave out dataType, dimensions and distanceFunction.

| Statement | Yes / No |
|---|---|
| The distance function defaults to cosine. | ☐ |
| The dimensions default to 1,536. | ☐ |
| The data type defaults to int8 to save storage. | ☐ |

<details><summary>💡 Hint</summary>

The defaults match a common Azure OpenAI embedding model at full precision.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The distance function defaults to cosine. | Yes | cosine is the default distanceFunction. |
| The dimensions default to 1,536. | Yes | 1,536 is the default, which matches text-embedding-ada-002. |
| The data type defaults to int8 to save storage. | No | The default dataType is float32. |

Vector embedding policy defaults: dataType float32, dimensions 1,536, distanceFunction cosine. Dimensions must match your embedding model.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 8. `lp4m2-008`

A team creates a container with a flat vector index for 1,536-dimension embeddings, because they want exact results. The policy is rejected. Why?

- **A.** Exact search needs the diskANN index
- **B.** The flat index supports at most 505 dimensions
- **C.** The flat index needs at least 1,000 vectors before you create it
- **D.** Flat indexes support only the euclidean distance function

<details><summary>💡 Hint</summary>

Each index type has a maximum number of dimensions. flat's is much lower than the others.

</details>

<details><summary>✅ Answer</summary>

**B.** The flat index supports at most 505 dimensions

- A: diskANN is approximate. Exact search is what flat (or brute force) gives.
- B: Correct. flat gives 100 percent recall but limits vectors to 505 dimensions.
- C: The 1,000-vector minimum is about quantizedFlat and diskANN being effective, not about creating flat.
- D: The distance function isn't the problem. The dimension count is.

flat stores vectors in the main index with exact brute-force search and 100 percent recall, but limits vectors to 505 dimensions. quantizedFlat and diskANN support up to 4,096.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 9. `lp4m2-009`

Storage for 40 million float32 embeddings is getting expensive. Tests show that lower precision barely changes search quality. Which change does Learn suggest first?

- **A.** Switch the distance function to euclidean
- **B.** Switch the vector dataType to float16
- **C.** Reduce the dimensions in the policy without changing the model
- **D.** Remove the vector index and rely on full scans

<details><summary>💡 Hint</summary>

Precision and storage trade off. Which data type halves the size of each number?

</details>

<details><summary>✅ Answer</summary>

**B.** Switch the vector dataType to float16

- A: The distance function changes scoring, not storage size.
- B: Correct. float16 cuts vector storage by 50 percent with minimal impact on quality for most AI apps.
- C: Dimensions must match the embedding model, or inserts fail.
- D: That makes every query far more expensive.

float32 gives full precision but uses the most storage. float16 reduces storage by 50 percent with minimal impact on quality. int8/uint8 need quantized embeddings.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 10. `lp4m2-010`

Your embeddings come from Azure OpenAI and are guaranteed to be normalized. You want the same ranking as cosine with slightly cheaper computation. Which distance function fits?

- **A.** dotproduct
- **B.** manhattan
- **C.** euclidean
- **D.** cosine, because it's the only option for Azure OpenAI

<details><summary>💡 Hint</summary>

For unit-length vectors, two of the functions rank results identically.

</details>

<details><summary>✅ Answer</summary>

**A.** dotproduct

- A: Correct. For normalized vectors, dot product gives the same results as cosine and can be slightly faster.
- B: Manhattan isn't a supported distance function. The options are cosine, dotproduct and euclidean.
- C: Euclidean measures straight-line distance and is described for specialized cases.
- D: cosine works, but dotproduct is also valid for normalized vectors and can be faster.

Dot product measures angle and magnitude. For normalized vectors, it's mathematically identical to cosine similarity but can be slightly faster to compute.

📘 Source: [Store and retrieve embeddings in Azure Cosmos DB](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/2-store-retrieve-embeddings)

</details>

## 11. `lp4m2-011`

A RAG app passes retrieved documents to a language model as context. How many results does Learn suggest returning?

- **A.** All matching documents
- **B.** 5–10
- **C.** 1–2
- **D.** 50–100

<details><summary>💡 Hint</summary>

RAG needs enough context to answer, but not so much that the prompt fills with noise.

</details>

<details><summary>✅ Answer</summary>

**B.** 5–10

- A: Returning everything is slow and expensive.
- B: Correct. Five to ten results give context without overwhelming the model.
- C: Too few results can miss needed context.
- D: More context doesn't always help and raises token costs.

RAG 5–10, user search 10–20 with pagination, recommendations 3–5.

📘 Source: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

</details>

## 12. `lp4m2-012`

Documents were embedded with text-embedding-ada-002. A developer embeds user queries with a different model to save cost, and results become irrelevant. Why?

- **A.** The cosine distance function works with ada-002 embeddings alone
- **B.** Different models create incompatible vector spaces
- **C.** The query vector belongs inline, not in a parameter
- **D.** The vector index has to be rebuilt after each query

<details><summary>💡 Hint</summary>

Vectors from different models live in different spaces.

</details>

<details><summary>✅ Answer</summary>

**B.** Different models create incompatible vector spaces

- A: Cosine works with any embeddings; the problem is the mismatch.
- B: Correct. Use the same model for queries and documents.
- C: Parameters are recommended and don't cause this.
- D: Indexes aren't rebuilt per query.

Query embeddings must come from the same model that produced the document embeddings.

📘 Source: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

</details>

## 13. `lp4m2-013`

For each statement, select Yes if the statement is true. Otherwise, select No. A query uses `VectorDistance(c.embedding, @queryVector)` with cosine distance.

| Statement | Yes / No |
|---|---|
| A document scoring 0.9 is more similar to the query than one scoring 0.5. | ☐ |
| Adding WHERE VectorDistance(c.embedding, @queryVector) > 0.7 keeps highly similar results. | ☐ |
| Omitting TOP N is fine because the index limits the results automatically. | ☐ |

<details><summary>💡 Hint</summary>

Cosine similarity: higher is closer. TOP N still matters.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A document scoring 0.9 is more similar to the query than one scoring 0.5. | Yes | With cosine, higher scores mean greater similarity. |
| Adding WHERE VectorDistance(c.embedding, @queryVector) > 0.7 keeps highly similar results. | Yes | A 0.7 threshold typically returns highly relevant results. |
| Omitting TOP N is fine because the index limits the results automatically. | No | Without TOP N the query tries to return all documents. |

Use TOP N, ORDER BY VectorDistance, and optional thresholds.

📘 Source: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

</details>

## 14. `lp4m2-014`

An evaluation job must compare approximate DiskANN results against exact results for 200 test queries. How do you get exact results?

- **A.** Remove TOP N so that every document gets compared
- **B.** Switch the distance function from cosine to euclidean
- **C.** Rebuild the container with a flat index
- **D.** Pass true as the third argument to VectorDistance

<details><summary>💡 Hint</summary>

VectorDistance takes more than two arguments.

</details>

<details><summary>✅ Answer</summary>

**D.** Pass true as the third argument to VectorDistance

- A: Removing TOP N returns everything; it doesn't change the search method.
- B: The distance function doesn't make search exact.
- C: flat can't hold 1,536 dimensions, and rebuilding isn't needed.
- D: Correct. true forces brute-force search for 100% accurate results.

Reserve brute force for evaluation and testing or very small datasets.

📘 Source: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

</details>

## 15. `lp4m2-015`

Vector queries for a user-facing search page are slow and costly. Which two changes follow Learn's optimization guidance? (Select two.)

- **A.** Request TOP 10 instead of TOP 100 when the page shows 10
- **B.** Force brute-force search for more accurate ranking
- **C.** Embed the 1,536 numbers directly in the query text
- **D.** Project id, title and score instead of SELECT *

<details><summary>💡 Hint</summary>

Return fewer results and fewer properties.

</details>

<details><summary>✅ Answer</summary>

**A.** Request TOP 10 instead of TOP 100 when the page shows 10  
**D.** Project id, title and score instead of SELECT *

- A: Correct. Use the smallest reasonable TOP N.
- B: Brute force consumes far more RUs and adds latency.
- C: Inline vectors are unwieldy and lose plan caching.
- D: Correct. Project only needed fields.

Limit results, project fields, use partition keys, and pick the right index type.

📘 Source: [Execute vector similarity queries for semantic search](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/3-execute-vector-similarity-queries)

</details>

## 16. `lp4m2-016`

Users search for exact error codes such as 0x80070005 as well as plain-language descriptions. Which query approach does Learn recommend?

- **A.** Brute-force VectorDistance with true as the third argument
- **B.** A cosine similarity threshold of 0.9 in the WHERE clause
- **C.** Hybrid search: RRF over VectorDistance and FullTextScore
- **D.** Plain vector search, with TOP N raised to 100 results

<details><summary>💡 Hint</summary>

Exact codes need keyword matching, and descriptions need meaning. Combine both rankings.

</details>

<details><summary>✅ Answer</summary>

**C.** Hybrid search: RRF over VectorDistance and FullTextScore

- A: Exact vector math still doesn't match exact codes.
- B: A threshold filters results; it doesn't add keyword matching.
- C: Correct. RRF merges semantic and keyword rankings.
- D: More vector results don't add exact keyword matching.

Hybrid search combines vector similarity with full-text scoring through Reciprocal Rank Fusion.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 17. `lp4m2-017`

A hybrid query uses `RRF(VectorDistance(…), FullTextScore(…), [1, 3])`. What does the weight array do?

- **A.** Full-text score counts three times as much as vector similarity
- **B.** Limits the query to partitions 1 and 3
- **C.** Vector similarity counts three times as much as full-text
- **D.** Returns 1 vector result and 3 full-text results per query

<details><summary>💡 Hint</summary>

The weights array scales each ranking's contribution.

</details>

<details><summary>✅ Answer</summary>

**A.** Full-text score counts three times as much as vector similarity

- A: Correct. Weights map in order: vector 1, full-text 3.
- B: Weights have nothing to do with partitions.
- C: Weights follow the order of the scoring functions, so it's the reverse.
- D: Weights influence ranking, not result counts.

Use higher full-text weight when users search for codes, names and exact terms.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 18. `lp4m2-018`

For each statement, select Yes if the statement is true. Otherwise, select No. A vector query asks for TOP 10 with a filter that excludes most documents.

| Statement | Yes / No |
|---|---|
| With post-filtering, the query might return fewer than 10 results. | ☐ |
| Selective filters can improve performance by reducing the vectors compared. | ☐ |
| You choose pre- or post-filtering with a query hint for every query. | ☐ |
| Post-filtering always returns exactly the number of results requested in TOP. | ☐ |

<details><summary>💡 Hint</summary>

Post-filtering can leave you short. Selective filters reduce work.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| With post-filtering, the query might return fewer than 10 results. | Yes | If top matches fail the filter, fewer rows come back. |
| Selective filters can improve performance by reducing the vectors compared. | Yes | Pre-filtering shrinks the search space. |
| You choose pre- or post-filtering with a query hint for every query. | No | The query optimizer chooses automatically based on selectivity. |
| Post-filtering always returns exactly the number of results requested in TOP. | No | Post-filtering can return fewer results if top matches fail the filter. |

Filters and vector search work together; the optimizer picks the strategy.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 19. `lp4m2-019`

You try a hybrid query, but it fails because the container was configured only with a vector policy and a diskANN index. What else is required?

- **A.** A second vector path for /content in the vector policy
- **B.** Changing the distance function to dotproduct
- **C.** A flat index in place of the diskANN vector index
- **D.** A full-text policy and full-text indexes on the text paths

<details><summary>💡 Hint</summary>

Full-text scoring needs its own policy and index.

</details>

<details><summary>✅ Answer</summary>

**D.** A full-text policy and full-text indexes on the text paths

- A: Another vector path doesn't enable FullTextScore.
- B: Distance function doesn't enable full-text scoring.
- C: Index type isn't the issue, and flat can't hold large dimensions.
- D: Correct. Hybrid search needs a full-text policy and fullTextIndexes as well as vector indexes.

Configure fullTextPaths in the full-text policy and fullTextIndexes in the indexing policy.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 20. `lp4m2-020`

A vector query filters to one category of 1,000 documents out of 100,000. The optimizer applies the filter before comparing vectors. What's the effect?

- **A.** Only those 1,000 documents are compared, which improves efficiency
- **B.** The query returns fewer than TOP N results by design
- **C.** The filter is ignored because vector queries can't filter
- **D.** All 100,000 are ranked first, and then the filter removes most of them

<details><summary>💡 Hint</summary>

Before or after: when is the filter applied, and how many vectors are compared?

</details>

<details><summary>✅ Answer</summary>

**A.** Only those 1,000 documents are compared, which improves efficiency

- A: Correct. Pre-filtering reduces the search space before vector comparison.
- B: That risk belongs to post-filtering, not pre-filtering.
- C: Vector queries can combine with metadata filters.
- D: That describes post-filtering.

Pre-filtering reduces the search space before vector comparison, which helps with selective filters. Post-filtering ranks first, preserving ranking quality but sometimes returning fewer results than requested.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 21. `lp4m2-021`

A team plans to use hybrid search (VectorDistance plus FullTextScore) for every query, including ones where pure vector search already works well. What does Learn advise?

- **A.** Avoid hybrid search, because RRF can't weight the two rankings
- **B.** Use hybrid search only where it adds clear value, because it costs more
- **C.** Use hybrid everywhere, because it always improves relevance at no extra cost
- **D.** Use hybrid search only on containers with a flat index

<details><summary>💡 Hint</summary>

Combining two scoring functions means doing two kinds of work.

</details>

<details><summary>✅ Answer</summary>

**B.** Use hybrid search only where it adds clear value, because it costs more

- A: RRF accepts a weights array.
- B: Correct. Hybrid search evaluates both scoring functions, so use it when it helps.
- C: Evaluating two scoring functions costs more.
- D: Hybrid search doesn't depend on the flat index.

Hybrid search costs more because it evaluates both VectorDistance and FullTextScore. Use it when it provides clear value, such as queries mixing exact terms and meaning.

📘 Source: [Combine vector similarity results with metadata filtering](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/4-combine-vector-metadata-filtering)

</details>

## 22. `lp4m2-022`

What does the change feed processor store in the lease container?

- **A.** The embeddings generated for each document
- **B.** The vector index for the monitored container's embeddings
- **C.** Partition ownership and the checkpoint for each partition
- **D.** Copies of every changed document, kept for replay

<details><summary>💡 Hint</summary>

The lease container is how processor instances share work and remember progress.

</details>

<details><summary>✅ Answer</summary>

**C.** Partition ownership and the checkpoint for each partition

- A: Embeddings are written back to the documents.
- B: Vector indexes live in the data container's indexing policy.
- C: Correct. Leases track which instance owns each partition and its checkpoint.
- D: The change feed itself records changes; leases don't copy documents.

Leases give checkpointing, coordination across instances and failover.

📘 Source: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

</details>

## 23. `lp4m2-023`

Editors fix typos in metadata fields many times a day, and each change triggers an expensive embedding call. How should you reduce cost?

- **A.** Re-embed only when a stored content hash changes
- **B.** Turn off the change feed for that container
- **C.** Switch from the push model to the pull model
- **D.** Increase the lease container to 4,000 RU/s

<details><summary>💡 Hint</summary>

Not every edit changes the text that was embedded.

</details>

<details><summary>✅ Answer</summary>

**A.** Re-embed only when a stored content hash changes

- A: Correct. Selective refresh skips changes that don't affect semantic content.
- B: You'd lose embedding refresh entirely.
- C: Pull changes when you read, not whether you re-embed.
- D: Lease throughput doesn't reduce embedding API calls.

Store a hash of the embedded text and refresh only when it differs.

📘 Source: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

</details>

## 24. `lp4m2-024`

For each statement, select Yes if the statement is true. Otherwise, select No. A team plans embedding refresh with the Cosmos DB change feed.

| Statement | Yes / No |
|---|---|
| The change feed must be turned on for each container before use. | ☐ |
| Changes within one partition key arrive in modification order. | ☐ |
| The pull model stores progress in the lease container automatically. | ☐ |

<details><summary>💡 Hint</summary>

The change feed is on by default. Order is per partition key. Pull doesn't use leases.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The change feed must be turned on for each container before use. | No | It's enabled by default on all containers. |
| Changes within one partition key arrive in modification order. | Yes | Ordered delivery within a partition key. |
| The pull model stores progress in the lease container automatically. | No | With pull, you keep the continuation token yourself. |

Push uses leases and automatic checkpoints; pull uses continuation tokens you store.

📘 Source: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

</details>

## 25. `lp4m2-025`

Two Azure Functions both monitor the knowledge-base container: one refreshes embeddings and one updates a search log. They should share one lease container. What must differ?

- **A.** Their leaseContainerPrefix values
- **B.** The partition keys they read from
- **C.** The database names they connect to
- **D.** The embedding models they call

<details><summary>💡 Hint</summary>

Two processors can share a lease container if their leases don't collide.

</details>

<details><summary>✅ Answer</summary>

**A.** Their leaseContainerPrefix values

- A: Correct. Functions monitoring the same container can share a lease container with different prefixes.
- B: Both read the same data container's partitions.
- C: They use the same database.
- D: Embedding models aren't related to lease sharing.

Share a lease container with different leaseContainerPrefix values, or use separate lease containers.

📘 Source: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

</details>

## 26. `lp4m2-026`

You're building production embedding refresh from the change feed and want reliable delivery with little operational code. Which consumption model does Learn recommend?

- **A.** The push model, using Azure Functions or the change feed processor
- **B.** Enabling the change feed on each container first
- **C.** A nightly full scan of the container
- **D.** The pull model with a loop that polls every second

<details><summary>💡 Hint</summary>

One model sends changes to you. The other makes you go and ask.

</details>

<details><summary>✅ Answer</summary>

**A.** The push model, using Azure Functions or the change feed processor

- A: Correct. Push delivers changes to your code and handles progress, which is simpler and more reliable for production.
- B: The change feed is enabled by default on all containers.
- C: A scan reprocesses everything and misses the point of the change feed.
- D: Pull gives more control, but you manage polling and progress yourself.

For embedding refresh in production, the push model (Azure Functions or the change feed processor library) provides better reliability and simpler operations. Use pull for batch scenarios or more control.

📘 Source: [Use the change feed to trigger embedding refresh](https://learn.microsoft.com/en-us/training/modules/implement-vector-search-azure-cosmos-db/5-change-feed-trigger-embedding-refresh)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
