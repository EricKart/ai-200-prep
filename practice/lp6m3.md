# Practice: LP6 · M3 Implement vector storage in Azure Managed Redis

> 23 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp6m3.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-6/implement-vector-storage-azure-managed-redis)

## 1. `lp6m3-001`

Your app has a 1,536-float NumPy embedding to store in a Redis hash for vector search. How should it be stored?

- **A.** As a comma-separated string
- **B.** As bytes from embedding.tobytes()
- **C.** As 1,536 separate hash fields
- **D.** As a JSON array in a hash field

<details><summary>💡 Hint</summary>

Redis Hash fields hold strings or bytes. Convert the array to raw bytes.

</details>

<details><summary>✅ Answer</summary>

**B.** As bytes from embedding.tobytes()

- A: A text string isn't the binary format the index expects.
- B: Correct. Redis stores hash vectors as binary blobs for efficiency.
- C: The vector is one field holding bytes.
- D: JSON arrays are for Redis JSON documents, not hash fields.

Convert NumPy arrays with tobytes() before storing them in a hash.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 2. `lp6m3-002`

Which dialect must you set for Redis vector queries?

- **A.** dialect(1)
- **B.** No dialect is needed
- **C.** dialect(2)
- **D.** dialect(3)

<details><summary>💡 Hint</summary>

Vector queries need a specific query dialect.

</details>

<details><summary>✅ Answer</summary>

**C.** dialect(2)

- A: Learn says vector queries need dialect 2.
- B: Vector queries require dialect 2.
- C: Correct. Use .dialect(2) for vector queries.
- D: Learn specifies dialect 2.

Query("*=>[KNN 5 @embedding $query_vec AS score]").dialect(2)

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 3. `lp6m3-003`

You need the 3 nearest documents to a question, but only within the documentation category. Which query string is correct?

- **A.** [KNN 3 @embedding $query_vec]=>@category:{documentation}
- **B.** @category:{documentation}=>[KNN 3 @embedding $query_vec AS score]
- **C.** *=>[KNN 3 @embedding $query_vec AS score] @category:{documentation}
- **D.** @embedding:[VECTOR_RANGE 3 $query_vec]=>{category: documentation}

<details><summary>💡 Hint</summary>

Put the filter before the arrow and the KNN clause after it.

</details>

<details><summary>✅ Answer</summary>

**B.** @category:{documentation}=>[KNN 3 @embedding $query_vec AS score]

- A: The KNN clause belongs after =>.
- B: Correct. The filter goes before the vector search operator =>.
- C: The filter must come before =>, not after the KNN clause.
- D: VECTOR_RANGE takes a distance threshold, not a count, and this isn't the filter syntax.

Hybrid queries filter first, then find the K nearest within the filtered set.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 4. `lp6m3-004`

A support bot must return every document within cosine distance 0.2 of the question, however many that is. Which query type fits?

- **A.** A VECTOR_RANGE query with 0.2
- **B.** A KNN query with K set to 100
- **C.** A FLAT index queried with K = 1
- **D.** A query with EF_RUNTIME set to 0.2

<details><summary>💡 Hint</summary>

"However many" means a distance cut-off, not a fixed count.

</details>

<details><summary>✅ Answer</summary>

**A.** A VECTOR_RANGE query with 0.2

- A: Correct. Range queries return all vectors within the distance.
- B: KNN returns a fixed number, not everything within a threshold.
- C: FLAT is an algorithm; K = 1 returns one result.
- D: EF_RUNTIME is an exploration count, not a distance threshold.

KNN = fixed count; VECTOR_RANGE = everything within a distance.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 5. `lp6m3-005`

For each statement, select Yes if the statement is true. Otherwise, select No. An index has `DIM 1536`, `DISTANCE_METRIC COSINE` and prefix `doc:`.

| Statement | Yes / No |
|---|---|
| Adding a hash with key doc:042 and an embedding field indexes it automatically. | ☐ |
| A query with a 768-dimension vector returns approximate results. | ☐ |
| A score of 0.05 means the document is very similar to the query. | ☐ |
| Loading 1 million documents with individual hset calls is the fastest way to ingest. | ☐ |

<details><summary>💡 Hint</summary>

Prefixed keys are indexed automatically. Query dimensions must match exactly.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Adding a hash with key doc:042 and an embedding field indexes it automatically. | Yes | Redis indexes keys with the prefix automatically. |
| A query with a 768-dimension vector returns approximate results. | No | Dimension mismatches are rejected with an error. |
| A score of 0.05 means the document is very similar to the query. | Yes | Lower COSINE distance means more similar. |
| Loading 1 million documents with individual hset calls is the fastest way to ingest. | No | Pipelines batch commands for 10–100× throughput. |

Match DIM exactly, read scores as distances, and use pipelines for bulk loads.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 6. `lp6m3-006`

A team stores image embeddings and uses COSINE because "it's best for text". Results look odd. What does Learn recommend for image embeddings and spatial data?

- **A.** L2
- **B.** COSINE with FLAT
- **C.** HNSW with EF_RUNTIME 10
- **D.** IP

<details><summary>💡 Hint</summary>

COSINE suits text. Images and spatial data use a different metric.

</details>

<details><summary>✅ Answer</summary>

**A.** L2

- A: Correct. L2 suits image embeddings and spatial data where magnitude matters.
- B: The metric, not the algorithm, is the issue.
- C: EF_RUNTIME tunes exploration, not the metric.
- D: IP is only for pre-normalized embeddings.

COSINE for text, L2 for images and spatial data, IP for pre-normalized embeddings.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 7. `lp6m3-007`

HNSW queries are fast but sometimes miss clearly relevant documents. What should you adjust first?

- **A.** Lower DIM to 768 in the index schema
- **B.** Remove dialect(2) from the vector query
- **C.** Switch the DISTANCE_METRIC to IP
- **D.** Raise EF_RUNTIME (start near 50, up to 200)

<details><summary>💡 Hint</summary>

HNSW explores a limited part of the graph. One runtime setting widens the search.

</details>

<details><summary>✅ Answer</summary>

**D.** Raise EF_RUNTIME (start near 50, up to 200)

- A: DIM must match the model exactly.
- B: Vector queries need dialect 2.
- C: Changing the metric would break semantic results for text.
- D: Correct. Higher EF_RUNTIME explores more of the graph for better accuracy.

EF_RUNTIME trades speed for accuracy per query.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 8. `lp6m3-008`

An ingestion script loads 500,000 documents with one hset call each, and throughput tops out at a few hundred writes per second. What does Learn suggest?

- **A.** Store the embeddings as JSON text strings instead of bytes
- **B.** Batch the hset commands in a pipeline and call execute()
- **C.** Create a new index for every 10,000 documents
- **D.** Switch the index algorithm from HNSW to FLAT

<details><summary>💡 Hint</summary>

Each command waits for a network round trip. How do you send many at once?

</details>

<details><summary>✅ Answer</summary>

**B.** Batch the hset commands in a pipeline and call execute()

- A: Text strings are larger and don't fix network round trips.
- B: Correct. Pipelines batch commands into one round trip, which removes per-command network overhead.
- C: Many indexes complicate search and don't speed up writes.
- D: The algorithm affects search, not how fast you can send writes.

Individual hset commands are limited by network overhead to a few hundred per second. Pipelines batch many commands and send them in one round trip.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 9. `lp6m3-009`

What does the query string *=>[KNN 5 @embedding $query_vec AS score] do?

- **A.** Searches only documents whose embedding field equals the query vector
- **B.** Returns every document within a distance of 5 from the query vector
- **C.** Searches all documents and returns the 5 nearest neighbors in the embedding field, with a score
- **D.** Returns 5 random documents and scores them against the query

<details><summary>💡 Hint</summary>

Read it in parts: what the asterisk means, what KNN 5 asks for, and what AS names.

</details>

<details><summary>✅ Answer</summary>

**C.** Searches all documents and returns the 5 nearest neighbors in the embedding field, with a score

- A: KNN finds the nearest vectors, not exact matches.
- B: That's a range query. KNN returns a fixed number of results.
- C: Correct. * means no pre-filter, KNN 5 asks for five neighbors, and AS score names the distance.
- D: KNN ranks by distance. It doesn't pick at random.

*=>[KNN 5 @embedding $query_vec AS score] searches all documents, finds 5 nearest neighbors in @embedding and returns their scores. Use .dialect(2), and pass the query vector as bytes.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 10. `lp6m3-010`

Your embedding model outputs pre-normalized vectors, and its documentation asks for inner product scoring. Which DISTANCE_METRIC fits, according to Learn?

- **A.** COSINE, because IP isn't supported for vectors
- **B.** L2
- **C.** IP
- **D.** FLOAT64

<details><summary>💡 Hint</summary>

One metric is reserved for pre-normalized vectors.

</details>

<details><summary>✅ Answer</summary>

**C.** IP

- A: IP is a supported metric. Learn limits it to pre-normalized or specialized models.
- B: L2 is the guidance for image embeddings and spatial data.
- C: Correct. Use IP only with pre-normalized embeddings or models that require it.
- D: FLOAT64 is a data type, not a distance metric.

COSINE: text embeddings. L2: image embeddings and spatial data. IP (inner product): only for pre-normalized embeddings or models that require it.

📘 Source: [Index and query vector data](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/2-index-query-vector-data)

</details>

## 11. `lp6m3-011`

How much memory does one 1,536-dimension FLOAT32 vector need?

- **A.** About 6 KB
- **B.** About 1.5 KB
- **C.** About 24 KB
- **D.** About 12 KB

<details><summary>💡 Hint</summary>

4 bytes per value times 1,536 values.

</details>

<details><summary>✅ Answer</summary>

**A.** About 6 KB

- A: Correct. 1,536 × 4 bytes ≈ 6 KB.
- B: That's 384 dimensions.
- C: That's far too large.
- D: That's FLOAT64 at 8 bytes per dimension.

FLOAT32 = 4 bytes per dimension; FLOAT64 = 8.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 12. `lp6m3-012`

A prototype searches 3,000 FAQ embeddings and needs exact results. Which algorithm fits?

- **A.** DiskANN
- **B.** FLAT
- **C.** HNSW
- **D.** IVFFlat

<details><summary>💡 Hint</summary>

A few thousand vectors and exact results: brute force is fine.

</details>

<details><summary>✅ Answer</summary>

**B.** FLAT

- A: DiskANN isn't one of Redis's algorithms here.
- B: Correct. FLAT is exact and suits under 10,000 vectors.
- C: HNSW is approximate and aimed at larger sets.
- D: IVFFlat isn't one of Redis's algorithms in this module.

Redis offers FLAT (exact) and HNSW (approximate).

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 13. `lp6m3-013`

Match each workload to Learn's quick configuration guide.

Choices: **FLOAT32 · COSINE · FLAT** · **FLOAT32 · COSINE · HNSW** · **FLOAT32 · L2 · HNSW**

- Text search over a few thousand documents
- Product recommendations across millions of items
- Finding visually similar product images

<details><summary>💡 Hint</summary>

Small text, large text, and images each have their own row in the guide.

</details>

<details><summary>✅ Answer</summary>

- Text search over a few thousand documents → **FLOAT32 · COSINE · FLAT**. Small text search: FLAT.
- Product recommendations across millions of items → **FLOAT32 · COSINE · HNSW**. Recommendations: COSINE with HNSW.
- Finding visually similar product images → **FLOAT32 · L2 · HNSW**. Image similarity: L2 with HNSW.

Dataset size picks the algorithm; the embedding type picks the metric.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 14. `lp6m3-014`

For each statement, select Yes if the statement is true. Otherwise, select No. A team proposes FLOAT64 for 10 million text embeddings "for better accuracy".

| Statement | Yes / No |
|---|---|
| FLOAT64 doubles vector memory compared with FLOAT32. | ☐ |
| Learn says FLOAT64 gives meaningfully better accuracy for typical AI embeddings. | ☐ |
| Larger vectors can also slow distance calculations. | ☐ |

<details><summary>💡 Hint</summary>

Double the bytes, but no meaningful gain for embeddings.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| FLOAT64 doubles vector memory compared with FLOAT32. | Yes | 8 bytes per dimension instead of 4. |
| Learn says FLOAT64 gives meaningfully better accuracy for typical AI embeddings. | No | The extra precision provides no meaningful improvement for nearly all AI applications. |
| Larger vectors can also slow distance calculations. | Yes | Larger data means more memory transfer. |

Use FLOAT32 unless you need maximum precision for specialized research.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 15. `lp6m3-015`

With FLAT indexing, Learn's example gives about 10 ms for 10,000 vectors. Roughly how long might the same search take over 1 million vectors?

- **A.** About 1,000 ms
- **B.** About 10 ms
- **C.** About 10 seconds
- **D.** About 100 ms

<details><summary>💡 Hint</summary>

Brute force grows in step with the number of vectors.

</details>

<details><summary>✅ Answer</summary>

**A.** About 1,000 ms

- A: Correct. Learn's example: 1 million vectors could take around 1,000 ms.
- B: FLAT time grows with dataset size.
- C: That's ten times more than linear growth.
- D: Linear growth from 10,000 to 1M is 100×.

FLAT scales linearly; HNSW keeps queries fast on large datasets.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 16. `lp6m3-016`

A product recommendation engine must return similar items in under 10 milliseconds across several million product embeddings. A slightly imperfect top 10 is acceptable. Which algorithm fits?

- **A.** HNSW
- **B.** FLAT
- **C.** KNN with no index
- **D.** FLAT with FLOAT64

<details><summary>💡 Hint</summary>

Millions of vectors and a strict latency budget call for approximate search.

</details>

<details><summary>✅ Answer</summary>

**A.** HNSW

- A: Correct. HNSW gives near-instant results on millions of vectors by trading a little accuracy for speed.
- B: FLAT compares every vector, which gets too slow at millions of items.
- C: Searching without an index is brute force, which is the slow path.
- D: A bigger data type makes brute force slower, not faster.

FLAT guarantees exact results but slows linearly with dataset size. HNSW builds a multi-layer graph for near-instant search on millions of vectors with a small accuracy trade-off.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 17. `lp6m3-017`

A team switches to an embedding model that outputs 3,072 dimensions, but the Redis index was created with DIM 1536. What happens to similarity search?

- **A.** The vectors don't match the index, because DIM must equal the model's output exactly
- **B.** Redis truncates the vectors to 1,536 values and searches normally
- **C.** Redis expands the index to 3,072 dimensions on the first insert
- **D.** Search works, but returns approximate results

<details><summary>💡 Hint</summary>

Distance calculations line vectors up one position at a time.

</details>

<details><summary>✅ Answer</summary>

**A.** The vectors don't match the index, because DIM must equal the model's output exactly

- A: Correct. Distances compare position by position, so dimensions must match exactly.
- B: Redis doesn't adjust dimensions for you. Mismatched vectors don't work.
- C: DIM is fixed in the schema. You need a new index for the new model.
- D: A dimension mismatch is a failure, not a lower-accuracy search.

Embedding models output fixed lengths (384, 768, 1024, 1536, 3072…). The index DIM must match the model's output exactly because distance calculations compare each dimension by position.

📘 Source: [Choose vector types and indexing strategies](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/3-vector-types-index-strategy)

</details>

## 18. `lp6m3-018`

Products have only flat fields (name, price, category) plus one embedding, and memory cost matters most. Which structure should you use?

- **A.** Redis Stream
- **B.** Redis Hash
- **C.** Redis List
- **D.** Redis JSON

<details><summary>💡 Hint</summary>

Flat fields and lowest memory point to the simpler structure.

</details>

<details><summary>✅ Answer</summary>

**B.** Redis Hash

- A: Streams are for task queues.
- B: Correct. Hash stores vectors as compact bytes with the lowest memory and fastest queries.
- C: Lists aren't used for indexed vectors here.
- D: JSON adds formatting overhead for flexibility you don't need.

Hash for flat data and maximum performance; JSON when data is nested.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>

## 19. `lp6m3-019`

Each product document has nested specs, several image URLs and two embeddings (title and image). Which structure fits best?

- **A.** A Redis Hash per spec
- **B.** A Hash with both embeddings concatenated
- **C.** Redis JSON documents
- **D.** A Redis String per embedding

<details><summary>💡 Hint</summary>

Nested specs and several embeddings fit a document structure.

</details>

<details><summary>✅ Answer</summary>

**C.** Redis JSON documents

- A: Splitting specs across keys loses the document structure.
- B: Concatenating vectors breaks dimension matching.
- C: Correct. JSON handles nested structures and multiple vectors per item.
- D: Separate strings lose the link to metadata and the index.

Choose JSON for nested data and multiple vectors per item.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>

## 20. `lp6m3-020`

For each statement, select Yes if the statement is true. Otherwise, select No. A team stores vectors in Redis JSON documents.

| Statement | Yes / No |
|---|---|
| The embedding is stored as a numeric array, produced with tolist(). | ☐ |
| Index fields are referenced with JSONPath such as $.name and an as_name alias. | ☐ |
| JSON uses less memory than Hash for the same vector. | ☐ |

<details><summary>💡 Hint</summary>

JSON stores vectors as number lists and uses JSONPath. It isn't the smaller option.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The embedding is stored as a numeric array, produced with tolist(). | Yes | JSON stores the vector as a JSON array. |
| Index fields are referenced with JSONPath such as $.name and an as_name alias. | Yes | Use $. paths and as_name. |
| JSON uses less memory than Hash for the same vector. | No | JSON adds array formatting overhead; Hash is lower. |

JSON trades some memory and speed for flexibility.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>

## 21. `lp6m3-021`

You're moving product vectors from Hash to JSON. Put the steps in order.

- Convert it to a JSON document with the vector as a list
- Delete the old index and create a new one with the JSON IndexType
- Read each product from its Hash key
- Write the JSON document to Redis

<details><summary>💡 Hint</summary>

Read the old data, convert, write, then rebuild the index for the new type.

</details>

<details><summary>✅ Answer</summary>

1. Read each product from its Hash key
2. Convert it to a JSON document with the vector as a list
3. Write the JSON document to Redis
4. Delete the old index and create a new one with the JSON IndexType

Switching structures means re-ingesting data and recreating the index.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>

## 22. `lp6m3-022`

1 million flat product records with 1,536-dimension embeddings must give the lowest query latency and memory. A developer wants JSON "for future flexibility". What does Learn recommend?

- **A.** Use both, storing every product twice
- **B.** Use FLOAT64 in JSON to offset the extra overhead
- **C.** Use Hash now; re-ingest into JSON later if needed
- **D.** Use JSON, because JSON queries vectors faster

<details><summary>💡 Hint</summary>

Choose for today's needs. Migrating later is possible.

</details>

<details><summary>✅ Answer</summary>

**C.** Use Hash now; re-ingest into JSON later if needed

- A: Storing everything twice wastes memory.
- B: FLOAT64 doubles memory and doesn't help.
- C: Correct. For simple metadata, Hash gives the best balance; switching later means re-ingesting.
- D: Hash is faster than JSON.

Hash saves significant memory and latency at this scale; use JSON when complexity requires it.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>

## 23. `lp6m3-023`

You're storing a vector in a Redis Hash with the rest of a document's metadata. How should the embedding field be written, compared with storing it in a JSON document?

- **A.** In a Hash, as a numeric list; in JSON, as bytes
- **B.** In both, as a comma-separated string
- **C.** In both, as bytes from tobytes()
- **D.** In a Hash, as bytes from tobytes(); in JSON, as a numeric list from tolist()

<details><summary>💡 Hint</summary>

Hashes store raw bytes, and JSON stores arrays.

</details>

<details><summary>✅ Answer</summary>

**D.** In a Hash, as bytes from tobytes(); in JSON, as a numeric list from tolist()

- A: That's the wrong way round.
- B: Neither structure expects a text string of numbers.
- C: JSON documents store the embedding as a numeric array.
- D: Correct. Hash fields hold binary bytes, while JSON stores the vector as a numeric array.

With Hash, store embeddings as bytes (embedding.tobytes()) together with metadata via hset mapping. With JSON, store embeddings as numeric arrays (embedding.tolist()) and reference fields with JSONPath.

📘 Source: [Optimize Redis data structures for vector storage](https://learn.microsoft.com/en-us/training/modules/implement-vector-storage-azure-managed-redis/4-optimize-redis-data-structure)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
