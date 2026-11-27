# Practice: LP6 · M1 Implement data operations in Azure Managed Redis

> 24 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp6m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-6/implement-data-operations-azure-managed-redis)

## 1. `lp6m1-001`

In the cache-aside pattern, what happens on a cache miss?

- **A.** The app returns an error and retries later
- **B.** Redis forwards the request to the database by itself
- **C.** The app reads the database, then caches the result
- **D.** Redis loads the entire database into memory

<details><summary>💡 Hint</summary>

Cache-aside loads data into the cache only when it's asked for.

</details>

<details><summary>✅ Answer</summary>

**C.** The app reads the database, then caches the result

- A: A miss isn't an error.
- B: The application, not Redis, reads the database.
- C: Correct. Data is loaded into the cache only when requested.
- D: Cache-aside avoids preloading whole datasets.

Check Redis first; on a miss, fetch from the database and cache it for next time.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 2. `lp6m1-002`

An inference API needs the highest Redis throughput and has modest memory needs. Which tier fits?

- **A.** Balanced (4:1)
- **B.** Memory Optimized (8:1)
- **C.** Compute Optimized (2:1)
- **D.** Flash Optimized (preview)

<details><summary>💡 Hint</summary>

Highest throughput with modest memory: the tier with the lowest memory-to-vCPU ratio.

</details>

<details><summary>✅ Answer</summary>

**C.** Compute Optimized (2:1)

- A: Balanced is for standard workloads.
- B: Memory Optimized favors memory over throughput.
- C: Correct. Compute Optimized is for performance-intensive workloads needing maximum throughput.
- D: Flash Optimized trades performance for cheaper large datasets.

Match the memory-to-vCPU ratio to the workload.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 3. `lp6m1-003`

For each statement, select Yes if the statement is true. Otherwise, select No. A web app stores shopping carts and preferences in cookies, and pages have become slow.

| Statement | Yes / No |
|---|---|
| Large cookies are sent with every HTTP request and response, adding bandwidth and latency. | ☐ |
| Keeping only a session id in the cookie and the data in Redis is the typical fix. | ☐ |
| Azure Managed Redis can only be used by applications hosted in Azure. | ☐ |

<details><summary>💡 Hint</summary>

Cookies travel with every request. Keep only an id in the cookie.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Large cookies are sent with every HTTP request and response, adding bandwidth and latency. | Yes | Storing too much in cookies hurts performance. |
| Keeping only a session id in the cookie and the data in Redis is the typical fix. | Yes | The session id is the key to the session data in Redis. |
| Azure Managed Redis can only be used by applications hosted in Azure. | No | It's usable by any application inside or outside Azure. |

The session store pattern keeps cookies small and session data in memory.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 4. `lp6m1-004`

A team must cache a very large product dataset where most items are rarely read, and cost matters more than peak speed. Which tier fits?

- **A.** Balanced
- **B.** Compute Optimized
- **C.** Flash Optimized (preview)
- **D.** Memory Optimized with high availability disabled

<details><summary>💡 Hint</summary>

Big dataset, mostly cold, cost first: the tier that moves cold data to NVMe.

</details>

<details><summary>✅ Answer</summary>

**C.** Flash Optimized (preview)

- A: Balanced keeps everything in memory at a higher cost for this size.
- B: Compute Optimized has the least memory per vCPU.
- C: Correct. It moves less-used data from RAM to NVMe for cost-effective large caches.
- D: Disabling HA doesn't change where data is stored; Learn says keep HA on in production.

Flash Optimized trades some performance for scaling large datasets cheaply.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 5. `lp6m1-005`

A development team needs a Redis cache for testing with lots of memory, and it doesn't need high throughput. They want the lowest price point. Which tier fits?

- **A.** Memory Optimized (8:1 memory-to-vCPU)
- **B.** Compute Optimized (2:1 memory-to-vCPU)
- **C.** Flash Optimized (preview)
- **D.** Balanced (4:1 memory-to-vCPU)

<details><summary>💡 Hint</summary>

Lots of memory and little compute means a high memory-to-vCPU ratio.

</details>

<details><summary>✅ Answer</summary>

**A.** Memory Optimized (8:1 memory-to-vCPU)

- A: Correct. Memory Optimized suits memory-intensive use without top throughput, at a lower price, which is good for dev and test.
- B: This is for maximum throughput, which the team doesn't need.
- C: Flash moves cold data to NVMe for very large datasets. It isn't the dev/test default.
- D: Balanced is the standard choice for production workloads, not the lowest price for memory.

Memory Optimized (8:1) suits memory-intensive workloads that don't need top throughput, with a lower price point that's good for dev/test. Balanced (4:1) is for standard workloads; Compute Optimized (2:1) for maximum throughput.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 6. `lp6m1-006`

Every page on a retail site renders the same header, footer, banners and navigation menu from templates, which takes time on each request. Which Redis caching use case fits?

- **A.** Message queue
- **B.** Content cache
- **C.** Rate limiter
- **D.** Session store

<details><summary>💡 Hint</summary>

The data is the same for everyone and rarely changes.

</details>

<details><summary>✅ Answer</summary>

**B.** Content cache

- A: Queues hand work between processes. They don't serve repeated page content.
- B: Correct. Static template content such as headers and footers rarely changes, so it's ideal to cache.
- C: Rate limiting counts requests. It doesn't speed up page rendering.
- D: A session store holds per-user data such as carts, not shared page fragments.

Content cache: static template content (headers, footers, banners, navigation) rarely changes and is ideal for Redis, giving sub-millisecond access and reducing web server load.

📘 Source: [Explore Azure Managed Redis](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/2-explore-azure-managed-redis)

</details>

## 7. `lp6m1-007`

A cleanup job needs to find all keys matching `user:42:*` in production. Which command should it use?

- **A.** KEYS `user:42:*` on the primary
- **B.** SCAN with a match pattern
- **C.** FLUSHDB, then reload the data
- **D.** CLUSTER KEYSLOT for each key

<details><summary>💡 Hint</summary>

One command blocks the server while it walks every key. Use the one that iterates in steps.

</details>

<details><summary>✅ Answer</summary>

**B.** SCAN with a match pattern

- A: KEYS is expensive and blocks; don't use it in production.
- B: Correct. SCAN iterates keys without blocking the server.
- C: FLUSHDB deletes everything.
- D: That's blocked and doesn't list keys.

Avoid expensive operations: use SCAN instead of KEYS.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 8. `lp6m1-008`

Which Python client library does Learn list for Azure Managed Redis?

- **A.** Lettuce
- **B.** StackExchange.Redis
- **C.** redis-py
- **D.** node_redis

<details><summary>💡 Hint</summary>

The Python client's name is redis followed by the language's short name.

</details>

<details><summary>✅ Answer</summary>

**C.** redis-py

- A: That's the Java client.
- B: That's the C#/.NET client.
- C: Correct. redis-py is the Python client.
- D: That's the Node.js client.

StackExchange.Redis (.NET), Lettuce (Java), node_redis (Node.js), redis-py (Python).

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 9. `lp6m1-009`

An app uses MSET across keys in different hash slots and gets CROSSSLOT errors. The instance uses the OSS clustering policy. What's the fix?

- **A.** Switch the command from MSET to MGET
- **B.** Make the keys map to the same hash slot
- **C.** Enable Active-Active geo-replication on it
- **D.** Run KEYS before MSET to find each key's slot

<details><summary>💡 Hint</summary>

With OSS clustering, multi-key commands need every key in the same hash slot.

</details>

<details><summary>✅ Answer</summary>

**B.** Make the keys map to the same hash slot

- A: MGET is also multi-key and has the same constraint.
- B: Correct. With OSS clustering, all keys in a multi-key command must map to the same hash slot.
- C: Active-Active restricts cross-slot commands further.
- D: KEYS is expensive and doesn't fix slot mapping.

Enterprise clustering allows some multi-key commands across slots; OSS clustering doesn't.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 10. `lp6m1-010`

For each statement, select Yes if the statement is true. Otherwise, select No. A database uses Enterprise clustering with Active-Active geo-replication.

| Statement | Yes / No |
|---|---|
| MGET works across hash slots. | ☐ |
| DEL across hash slots works the same as without geo-replication. | ☐ |
| FLUSHALL is available to clear the cache quickly. | ☐ |

<details><summary>💡 Hint</summary>

Active-Active narrows which multi-key commands work across slots and blocks the flush commands.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| MGET works across hash slots. | Yes | In Active-Active databases, MGET, EXISTS and TOUCH work across slots. |
| DEL across hash slots works the same as without geo-replication. | No | In Active-Active, only MGET, EXISTS and TOUCH work across slots. |
| FLUSHALL is available to clear the cache quickly. | No | FLUSHALL and FLUSHDB are blocked for active geo-replication. |

Active-Active narrows which commands you can use.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 11. `lp6m1-011`

Which two practices does Learn recommend for connecting to Azure Managed Redis? (Select two.)

- **A.** Connect with the hostname rather than the public IP
- **B.** Disable TLS on the connection to reduce latency
- **C.** Connect to the public IP so that DNS isn't needed
- **D.** Place Redis and the app in the same Azure region

<details><summary>💡 Hint</summary>

Keep the app close to the cache, and don't rely on an IP that can change.

</details>

<details><summary>✅ Answer</summary>

**A.** Connect with the hostname rather than the public IP  
**D.** Place Redis and the app in the same Azure region

- A: Correct. IP addresses can change during scale operations.
- B: TLS is required by default (1.2 and 1.3).
- C: Public IPs can change; use hostnames.
- D: Correct. Co-locating reduces latency.

Co-locate, use hostnames, keep TLS on; scale when metrics stay above 75%.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 12. `lp6m1-012`

For each statement, select Yes if the statement is true. Otherwise, select No. A database uses the Enterprise clustering policy without geo-replication.

| Statement | Yes / No |
|---|---|
| MSET works across hash slots. | ☐ |
| CLUSTER NODES can be used to inspect the topology. | ☐ |
| Every client library can connect to this database. | ☐ |

<details><summary>💡 Hint</summary>

Enterprise clustering hides the cluster from clients. Think about what that allows and what it blocks.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| MSET works across hash slots. | Yes | Enterprise clustering allows DEL, MSET, MGET, EXISTS, UNLINK and TOUCH across slots. |
| CLUSTER NODES can be used to inspect the topology. | No | CLUSTER INFO, HELP, KEYSLOT, NODES and SLOTS are blocked with Enterprise clustering. |
| Every client library can connect to this database. | Yes | All client libraries work with the Enterprise clustering policy. |

With Enterprise clustering, all client libraries work, and DEL, MSET, MGET, EXISTS, UNLINK and TOUCH work across slots. CLUSTER INFO/HELP/KEYSLOT/NODES/SLOTS are blocked. Active-Active narrows cross-slot commands to MGET, EXISTS and TOUCH.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 13. `lp6m1-013`

An app caches each user's full 4 MB recommendation payload under one key, and responses are slow under load. Which best practice does Learn give first?

- **A.** Turn off TLS to make the payload smaller
- **B.** Move the cache to a different region from the app
- **C.** Split the data into several keys with smaller values
- **D.** Use KEYS to find and delete the large values

<details><summary>💡 Hint</summary>

Redis works best with many small values.

</details>

<details><summary>✅ Answer</summary>

**C.** Split the data into several keys with smaller values

- A: TLS is required, and it doesn't change payload size.
- B: Placing the cache in the same region as the app is the recommendation.
- C: Correct. Use smaller values and divide large chunks across multiple keys.
- D: KEYS is an expensive command that shouldn't be used in production.

Best practices: use smaller values (divide large data into multiple keys), use pipelining, avoid KEYS (use SCAN), co-locate in one region, use hostnames, and keep TLS on.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 14. `lp6m1-014`

Your production cache's Used Memory Percentage has stayed around 80% for two weeks, and CPU is at 78%. What does Learn suggest?

- **A.** Disable high availability to free memory
- **B.** Scale the instance, because the metrics consistently exceed 75%
- **C.** Wait until memory reaches 100%, because eviction handles the rest
- **D.** Run FLUSHALL weekly to keep memory low

<details><summary>💡 Hint</summary>

Learn gives one percentage threshold for memory, CPU, clients and bandwidth.

</details>

<details><summary>✅ Answer</summary>

**B.** Scale the instance, because the metrics consistently exceed 75%

- A: High availability should stay on in production.
- B: Correct. Learn says to scale when key metrics consistently exceed 75%.
- C: Running near capacity risks evictions and latency. Learn's threshold is 75%.
- D: Flushing deletes all data, which defeats the cache.

Monitor Used Memory Percentage, CPU, Connected Clients and Network bandwidth, and scale when they consistently exceed 75%.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 15. `lp6m1-015`

To cut costs, a teammate proposes disabling high availability on the production cache that holds user sessions. What does Learn recommend?

- **A.** Disable it and enable Flash Optimized instead
- **B.** Keep high availability on in production; disable it only for dev or test
- **C.** Disable it, because Redis data is always rebuilt from the database
- **D.** Disable it, but turn on data persistence to replace it

<details><summary>💡 Hint</summary>

It's production data that users depend on.

</details>

<details><summary>✅ Answer</summary>

**B.** Keep high availability on in production; disable it only for dev or test

- A: Flash Optimized is about storage cost, not availability.
- B: Correct. Use high availability for production workloads.
- C: Sessions may not be in any database, and an outage would log users out.
- D: Persistence helps recovery. It isn't a replacement for high availability.

Enable high availability for production workloads and only disable it for dev/test. For data protection, add data persistence or periodic import/export.

📘 Source: [Client libraries and development best practices](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/3-client-libraries-best-practices)

</details>

## 16. `lp6m1-016`

A Python app connects to Azure Managed Redis with redis-py. Which port should it use?

- **A.** 6379
- **B.** 6380
- **C.** 443
- **D.** 10000

<details><summary>💡 Hint</summary>

Azure Managed Redis listens on a different port from the older Azure Cache for Redis.

</details>

<details><summary>✅ Answer</summary>

**D.** 10000

- A: Learn doesn't list 6379 for these services.
- B: 6380 is for Azure Cache for Redis instances.
- C: 443 isn't the Redis port here.
- D: Correct. Azure Managed Redis and Enterprise caches use port 10000.

Azure Managed Redis: 10000; Azure Cache for Redis: 6380.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 17. `lp6m1-017`

A rate limiter counts requests per user across many API instances and must avoid race conditions. Which command fits?

- **A.** INCR on a per-user key
- **B.** GET then SET with the new value
- **C.** HSET on a per-user field
- **D.** LPUSH to a per-user list

<details><summary>💡 Hint</summary>

Counting across many instances needs an atomic operation.

</details>

<details><summary>✅ Answer</summary>

**A.** INCR on a per-user key

- A: Correct. INCR is atomic, so concurrent increments don't conflict.
- B: Read-then-write can race between instances.
- C: HSET overwrites a field; it doesn't increment atomically here.
- D: A list grows with entries rather than counting atomically.

INCR, DECR, INCRBY and DECRBY are atomic counters.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 18. `lp6m1-018`

For each statement, select Yes if the statement is true. Otherwise, select No. You store a user profile with `r.hset('user:1001', mapping={...})` and want it to expire in one hour.

| Statement | Yes / No |
|---|---|
| SETEX can store the hash and set its expiry in one command. | ☐ |
| r.expire('user:1001', 3600) adds the one-hour expiry. | ☐ |
| If r.ttl('user:1001') returns -1, the key exists but has no expiry. | ☐ |
| If r.ttl('user:1001') returns -2, the key exists with no expiry. | ☐ |

<details><summary>💡 Hint</summary>

SETEX is for strings. Hashes get their expiry separately. Learn the TTL return codes.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| SETEX can store the hash and set its expiry in one command. | No | SETEX is for string values; for hashes, set the data then use EXPIRE. |
| r.expire('user:1001', 3600) adds the one-hour expiry. | Yes | EXPIRE works on keys of any type. |
| If r.ttl('user:1001') returns -1, the key exists but has no expiry. | Yes | -1 means no expiration; -2 means the key doesn't exist. |
| If r.ttl('user:1001') returns -2, the key exists with no expiry. | No | -2 means the key doesn't exist; -1 means no expiry. |

Expiry commands operate on keys, so they work with every data type.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 19. `lp6m1-019`

An instance uses the OSS clustering policy, and code built with `redis.Redis(...)` fails on keys in other slots. What should the Python code use?

- **A.** redis.Redis with port 6380
- **B.** redis.Redis with decode_responses=False
- **C.** redis.cluster.RedisCluster
- **D.** redis.asyncio.Redis

<details><summary>💡 Hint</summary>

With OSS clustering, the client must understand the cluster.

</details>

<details><summary>✅ Answer</summary>

**C.** redis.cluster.RedisCluster

- A: 6380 is the Azure Cache for Redis port and doesn't address clustering.
- B: decode_responses only changes byte/string handling.
- C: Correct. With OSS clustering, connect with redis.cluster.RedisCluster.
- D: The async client doesn't change clustering support.

The clustering policy changes how you connect: OSS needs a cluster-aware client.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 20. `lp6m1-020`

Match each cached item to Learn's suggested TTL range.

Choices: **1–5 minutes** · **15–60 minutes** · **1–24 hours** · **24 hours or more**

- Live stock levels that change constantly
- Product recommendations that change a few times a day
- A user's profile details
- A list of country codes

<details><summary>💡 Hint</summary>

The more often data changes, the shorter its TTL.

</details>

<details><summary>✅ Answer</summary>

- Live stock levels that change constantly → **1–5 minutes**. Frequently changing data: 1–5 minutes.
- Product recommendations that change a few times a day → **15–60 minutes**. Moderate change rate: 15–60 minutes.
- A user's profile details → **1–24 hours**. Relatively stable data: 1–24 hours.
- A list of country codes → **24 hours or more**. Static reference data: 24+ hours.

Balance data freshness against cache hit rate when choosing TTLs.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 21. `lp6m1-021`

An app caches pickled Python objects in Redis. After the connection is created with decode_responses=True, reading them back fails. What should you change?

- **A.** Use decode_responses=False for binary data such as pickled objects
- **B.** Connect on port 6380 instead of 10000
- **C.** Store the objects with HSET instead of SET
- **D.** Add an expiry to each key

<details><summary>💡 Hint</summary>

One connection option turns bytes into text automatically.

</details>

<details><summary>✅ Answer</summary>

**A.** Use decode_responses=False for binary data such as pickled objects

- A: Correct. decode_responses=True converts responses to strings, which breaks binary data.
- B: The port is about which service you connect to, not decoding.
- C: The data type doesn't fix the decoding of binary values.
- D: Expiry controls lifetime, not how values are decoded.

decode_responses=True converts byte responses to strings, which suits text. For binary data such as images or pickled objects, use decode_responses=False.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 22. `lp6m1-022`

A production app should stop using an access key and connect to Azure Managed Redis with Microsoft Entra ID. What does Learn point to for redis-py?

- **A.** `redis.cluster.RedisCluster`, which handles authentication
- **B.** The redis-entraid package, with a token for `https://redis.azure.com/.default`
- **C.** Port `6380` with TLS turned off
- **D.** A password set to the app's client ID

<details><summary>💡 Hint</summary>

Entra ID support for redis-py comes from an add-on library.

</details>

<details><summary>✅ Answer</summary>

**B.** The redis-entraid package, with a token for `https://redis.azure.com/.default`

- A: RedisCluster is for OSS clustering. It doesn't add Entra ID authentication.
- B: Correct. redis-entraid adds Entra ID authentication to redis-py.
- C: Azure Managed Redis uses port 10000, and TLS is required.
- D: A client ID isn't a credential, and Entra ID authentication uses tokens.

For production, use Microsoft Entra ID authentication with the redis-entraid package, requesting tokens for `https://redis.azure.com/.default`.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 23. `lp6m1-023`

Background workers must process inference jobs in the order they were submitted (first in, first out). Which Redis data type and commands fit?

- **A.** A List, adding with LPUSH and taking with RPOP
- **B.** A List, adding with LPUSH and taking with LPOP
- **C.** A Hash, adding with HSET and reading with HGETALL
- **D.** A String counter, using INCR for each job

<details><summary>💡 Hint</summary>

Lists can act as a stack or a queue, depending on which ends you use.

</details>

<details><summary>✅ Answer</summary>

**A.** A List, adding with LPUSH and taking with RPOP

- A: Correct. Lists are ordered, and pushing on one end while popping from the other gives a FIFO queue.
- B: Pushing and popping on the same end gives LIFO (a stack), not FIFO.
- C: Hashes hold field-value pairs with no order for processing.
- D: A counter tracks a number. It doesn't hold the jobs.

Redis Lists are ordered collections. LPUSH/RPUSH add to either end and LPOP/RPOP remove; using opposite ends gives a FIFO queue, the same end gives LIFO.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

## 24. `lp6m1-024`

A team stores each field of a product (name, price, category, rating) as a separate key, such as product:42:name. Memory use is higher than expected. What does Learn suggest?

- **A.** Serialize every product into one giant string key
- **B.** Use MSET so that the separate keys take less space
- **C.** Store each product as one Hash with HSET
- **D.** Store each field as a List element

<details><summary>💡 Hint</summary>

One data type holds an object's fields under a single key.

</details>

<details><summary>✅ Answer</summary>

**C.** Store each product as one Hash with HSET

- A: Very large values are discouraged, and you'd lose per-field access.
- B: MSET writes several keys at once, but it doesn't make them smaller.
- C: Correct. Hashes keep field-value pairs in one key and are more memory-efficient than separate keys.
- D: Lists are for ordered collections, not named fields.

Hashes store objects as field-value pairs within a single key (HSET, HGET, HGETALL) and are more memory-efficient than storing each field as a separate key.

📘 Source: [Implement data operations](https://learn.microsoft.com/en-us/training/modules/implement-data-operations-azure-managed-redis/4-implement-data-operations)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
