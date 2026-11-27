# Practice: LP4 · M1 Build queries for Azure Cosmos DB for NoSQL

> 28 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp4m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-4/build-query-azure-cosmos-db)

## 1. `lp4m1-001`

Which Cosmos DB resource is the fundamental unit of scalability and holds the JSON items?

- **A.** Account
- **B.** Partition key
- **C.** Database
- **D.** Container

<details><summary>💡 Hint</summary>

Which level of the hierarchy holds the items and is the unit of scale?

</details>

<details><summary>✅ Answer</summary>

**D.** Container

- A: The account is the top-level management unit with the endpoint.
- B: A partition key is a container setting, not a resource.
- C: A database is a logical namespace that groups containers.
- D: Correct. Containers are the unit of scalability and hold items.

Account → database → container → item; containers scale and hold the documents.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 2. `lp4m1-002`

A chat app stores each user's conversation history. Queries almost always filter by user. Which property is the best partition key?

- **A.** /createdDate
- **B.** /isActive
- **C.** /userId
- **D.** /messageType

<details><summary>💡 Hint</summary>

Pick a property every item has, with many distinct values, that most queries filter on.

</details>

<details><summary>✅ Answer</summary>

**C.** /userId

- A: Date keys can create hot partitions during busy periods.
- B: A boolean gives two partitions and hot spots.
- C: Correct. userId has high cardinality and groups each user's data together.
- D: A few message types give low cardinality.

Choose a property that exists in every item, has many distinct values, and matches your queries.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 3. `lp4m1-003`

Autoscale throughput is configured with a maximum of 4,000 RU/s. What range does the container scale within?

- **A.** 400 to 4,000 RU/s
- **B.** 1,000 to 4,000 RU/s
- **C.** 0 to 4,000 RU/s
- **D.** 4,000 to 40,000 RU/s

<details><summary>💡 Hint</summary>

Autoscale's minimum is a fixed percentage of the maximum you set.

</details>

<details><summary>✅ Answer</summary>

**A.** 400 to 4,000 RU/s

- A: Correct. Autoscale scales between 10% of the maximum and the maximum.
- B: 1,000 RU/s is the smallest allowed maximum, not the floor here.
- C: Autoscale doesn't go to zero.
- D: The configured value is the maximum.

Autoscale minimum = 10% of the configured maximum.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 4. `lp4m1-004`

Four containers in one database have unpredictable, uneven usage, and the team wants to keep cost down. Where should throughput be provisioned?

- **A.** Shared throughput at the database level
- **B.** Dedicated throughput on the busiest container, none on the rest
- **C.** Dedicated manual throughput on each container
- **D.** Autoscale on the account

<details><summary>💡 Hint</summary>

Uneven, unpredictable use across several containers suggests pooling the RUs.

</details>

<details><summary>✅ Answer</summary>

**A.** Shared throughput at the database level

- A: Correct. Database-level throughput is shared across containers with variable usage.
- B: The other containers would then have no throughput.
- C: Dedicated throughput gives predictable performance but costs more for variable usage.
- D: Throughput is provisioned on databases or containers, not accounts.

Shared database throughput suits containers with variable usage; dedicated suits critical predictable workloads.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 5. `lp4m1-005`

For each statement, select Yes if the statement is true. Otherwise, select No. A container uses `/categoryId` as its partition key.

| Statement | Yes / No |
|---|---|
| Two items can share the id product-1 if they have different categoryId values. | ☐ |
| You can switch the partition key to /brandId later with a setting change. | ☐ |
| If you create an item without an id, the SDK generates one for you. | ☐ |
| _ts records when the item was last modified, in Unix seconds. | ☐ |

<details><summary>💡 Hint</summary>

Uniqueness is id plus partition key. The partition key can't change, and the SDK won't invent an id.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Two items can share the id product-1 if they have different categoryId values. | Yes | id plus partition key value uniquely identifies an item. |
| You can switch the partition key to /brandId later with a setting change. | No | You can't change the partition key without a new container and migration. |
| If you create an item without an id, the SDK generates one for you. | No | You must provide an id; the SDK doesn't generate one. |
| _ts records when the item was last modified, in Unix seconds. | Yes | _ts is a Unix timestamp of the last modification. |

Design ids and partition keys up front: the key is permanent and ids are yours to supply.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 6. `lp4m1-006`

Two workers read the same cached model output, change it and write it back, and one worker's change keeps getting lost. Which system property helps prevent this?

- **A.** _ts
- **B.** _self
- **C.** _rid
- **D.** _etag

<details><summary>💡 Hint</summary>

Optimistic concurrency uses a value that changes every time the item changes.

</details>

<details><summary>✅ Answer</summary>

**D.** _etag

- A: _ts shows when it changed but doesn't block a stale write.
- B: _self is a URI for addressing the item.
- C: _rid is an internal resource identifier.
- D: Correct. Writing with an _etag condition fails if the item changed since it was read.

_etag enables optimistic concurrency: the update fails with a conflict if someone else changed the item.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 7. `lp4m1-007`

A team wants to cut RU consumption for a busy workload. Which three factors does Learn say increase RU charges? (Select three.)

- **A.** Projecting fewer properties
- **B.** Stronger consistency levels such as strong
- **C.** Using point reads instead of queries
- **D.** Larger item sizes
- **E.** Cross-partition queries

<details><summary>💡 Hint</summary>

Bigger items, stronger guarantees and wider queries all cost more.

</details>

<details><summary>✅ Answer</summary>

**B.** Stronger consistency levels such as strong  
**D.** Larger item sizes  
**E.** Cross-partition queries

- A: Returning fewer properties can lower RU cost.
- B: Correct. Strong and bounded staleness consume more RUs.
- C: Point reads are the cheapest way to read one item.
- D: Correct. Larger documents cost more to read and write.
- E: Correct. Spanning partitions costs more than single-partition queries.

Item size, indexing policy, consistency, query complexity and cross-partition fan-out drive RU cost.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 8. `lp4m1-008`

For each statement, select Yes if the statement is true. Otherwise, select No. You're explaining the Cosmos DB for NoSQL resource model to a new developer.

| Statement | Yes / No |
|---|---|
| The hierarchy runs account → database → container → item. | ☐ |
| The account provides the DNS endpoint https://<account-name>.documents.azure.com:443/. | ☐ |
| Items in one container must all follow the same schema. | ☐ |
| By default, an account can hold up to 500 databases and containers combined. | ☐ |

<details><summary>💡 Hint</summary>

Think top-down from the account, and remember Cosmos DB doesn't enforce a schema.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The hierarchy runs account → database → container → item. | Yes | Accounts are the top-level unit, then databases, containers and items. |
| The account provides the DNS endpoint https://<account-name>.documents.azure.com:443/. | Yes | SDK connections use the account's endpoint. |
| Items in one container must all follow the same schema. | No | Containers are schema-agnostic, so items can have different structures. |
| By default, an account can hold up to 500 databases and containers combined. | Yes | That's the default limit Learn gives. |

Cosmos DB organizes resources as account → database → container → item. The account gives the DNS endpoint; containers are schema-agnostic; by default an account holds up to 500 databases and containers combined.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 9. `lp4m1-009`

A developer proposes partitioning an inference-results container by the boolean property isActive, because most queries filter on it. What problem does Learn warn about?

- **A.** The container would need a nested path such as /metadata/isActive
- **B.** Only two values exist, so traffic and data pile up in hot partitions
- **C.** Queries filtered on isActive would become cross-partition queries
- **D.** Boolean properties can't be used as partition key paths

<details><summary>💡 Hint</summary>

How many distinct values does a boolean have? Think about how the data spreads.

</details>

<details><summary>✅ Answer</summary>

**B.** Only two values exist, so traffic and data pile up in hot partitions

- A: Nested paths are allowed, but they don't fix low cardinality.
- B: Correct. Low-cardinality keys such as booleans create hot partitions and limit scale.
- C: Filtering on the partition key routes to one partition. The problem is the lack of spread.
- D: The issue isn't the data type. It's that there are only two values.

Partition keys need high cardinality. A key with only a few values, such as a boolean, creates hot partitions that get disproportionate traffic and storage.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 10. `lp4m1-010`

A database uses shared manual throughput. The team plans to add many small containers to it. What does Learn say about this model?

- **A.** Shared throughput is available only with autoscale
- **B.** Shared throughput supports an unlimited number of containers
- **C.** Each container in the database still needs its own 400 RU/s minimum
- **D.** The database has a minimum of 400 RU/s, shared across up to 25 containers

<details><summary>💡 Hint</summary>

Shared throughput has a minimum RU/s and a maximum number of containers.

</details>

<details><summary>✅ Answer</summary>

**D.** The database has a minimum of 400 RU/s, shared across up to 25 containers

- A: Shared throughput works with manual throughput too, as this database shows.
- B: Learn gives a limit of 25 containers for shared throughput.
- C: That's dedicated container throughput. Shared throughput pools RUs across containers.
- D: Correct. Shared database throughput starts at 400 RU/s and can serve up to 25 containers.

With manual throughput, a container with dedicated throughput has a minimum of 400 RU/s. A database with shared throughput also has a 400 RU/s minimum and can share it across up to 25 containers.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 11. `lp4m1-011`

You want to log how many RUs each Cosmos DB operation in your app uses, so that you can find expensive ones. Where does each operation report its RU charge?

- **A.** In the activity ID returned with each request
- **B.** Only in Azure Monitor, about an hour later
- **C.** In the x-ms-request-charge response header
- **D.** In the item's _ts system property

<details><summary>💡 Hint</summary>

Each response carries its own cost in a header.

</details>

<details><summary>✅ Answer</summary>

**C.** In the x-ms-request-charge response header

- A: The activity ID identifies a request for support. It isn't the charge.
- B: Each response carries its charge right away. Azure Monitor is for aggregated views.
- C: Correct. Every operation returns its RU cost in this header.
- D: _ts is the last-modified timestamp, not a cost.

Every operation returns its RU charge in the x-ms-request-charge response header. Log it (with the activity ID) to find expensive patterns.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 12. `lp4m1-012`

An app fetches a 1-KB user profile by id and partition key, and also writes a 1-KB cached result. Roughly how do the two operations compare in RU cost?

- **A.** About 100 RUs each, because both use the network
- **B.** About 10 RUs for the read; about 1 RU for the write
- **C.** Both cost about the same, because the item size is the same
- **D.** About 1 RU for the read; about 5–10 RUs for the write

<details><summary>💡 Hint</summary>

Point reads are the cheapest operation there is. Writes pay for indexing too.

</details>

<details><summary>✅ Answer</summary>

**D.** About 1 RU for the read; about 5–10 RUs for the write

- A: Point reads are the cheapest operation, at about 1 RU.
- B: That's the wrong way round. Writes cost more than point reads.
- C: Writes include indexing overhead, so they cost more than point reads.
- D: Correct. A 1-KB point read costs about 1 RU, and a 1-KB write about 5–10 RUs.

Point reads (single 1-KB item by id and partition key) cost around 1 RU. Writing a 1-KB item costs about 5–10 RUs depending on consistency and indexing.

📘 Source: [Explore Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/2-explore-cosmos-db-nosql)

</details>

## 13. `lp4m1-013`

A FastAPI service creates a new CosmosClient for every incoming request, and latency is erratic under load. What should you change?

- **A.** Create a new client for each container instead of per request
- **B.** Create one CosmosClient at startup and reuse it
- **C.** Call get_container_client before every query
- **D.** Switch from Entra ID to account keys

<details><summary>💡 Hint</summary>

Clients hold connection pools and routing caches. How many should an app create?

</details>

<details><summary>✅ Answer</summary>

**B.** Create one CosmosClient at startup and reuse it

- A: More clients still discard cached state.
- B: Correct. A single reused client keeps warm connection pools and cached routing information.
- C: Container handles are cheap but don't fix the client problem.
- D: Authentication method doesn't fix per-request client creation.

Register CosmosClient as a singleton or application-scoped service.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 14. `lp4m1-014`

Which built-in role lets an identity read and write items with Entra ID authentication?

- **A.** Cosmos DB Built-in Data Reader
- **B.** Cosmos DB Account Key Operator
- **C.** Cosmos DB Built-in Data Contributor
- **D.** Cosmos DB Built-in Owner

<details><summary>💡 Hint</summary>

Read and write with Entra ID: one built-in role says it can contribute data.

</details>

<details><summary>✅ Answer</summary>

**C.** Cosmos DB Built-in Data Contributor

- A: Data Reader allows read operations only.
- B: Learn doesn't list this role.
- C: Correct. Data Contributor allows read and write operations.
- D: Learn doesn't list this role.

Data Reader for reads; Data Contributor for reads and writes.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 15. `lp4m1-015`

Startup code must make sure the products container exists, and the app may restart many times. Which method should it call?

- **A.** database.create_container_if_not_exists()
- **B.** container.upsert_item()
- **C.** database.create_container()
- **D.** database.get_container_client()

<details><summary>💡 Hint</summary>

Startup code runs many times. Choose the call that's safe to repeat.

</details>

<details><summary>✅ Answer</summary>

**A.** database.create_container_if_not_exists()

- A: Correct. It creates the container if needed and returns it otherwise, so restarts don't fail.
- B: upsert_item writes items, not containers.
- C: create_container fails if the container already exists.
- D: get_container_client only makes a handle; it doesn't create anything.

*_if_not_exists methods are idempotent, which suits application initialization.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 16. `lp4m1-016`

Match each SDK call to its behavior.

Choices: **Fails with 409 if the item exists** · **Inserts or replaces the item** · **Fails if the item doesn't exist** · **Cheapest way to fetch one known item**

- create_item
- upsert_item
- replace_item
- read_item with id and partition key

<details><summary>💡 Hint</summary>

Create fails if it exists, replace fails if it doesn't, and upsert doesn't care.

</details>

<details><summary>✅ Answer</summary>

- create_item → **Fails with 409 if the item exists**. create_item catches accidental duplicates with a 409 Conflict.
- upsert_item → **Inserts or replaces the item**. upsert creates the item or replaces the existing one.
- replace_item → **Fails if the item doesn't exist**. replace requires the item to exist.
- read_item with id and partition key → **Cheapest way to fetch one known item**. A point read costs about 1 RU for a 1-KB item.

Pick the write method by whether you expect the item to exist.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 17. `lp4m1-017`

A cache lookup with read_item raises CosmosResourceNotFoundError when the result hasn't been computed yet. What should the code do?

- **A.** Retry read_item until the item appears
- **B.** Switch to a cross-partition query to search all partitions
- **C.** Catch the exception and compute the value as a fallback
- **D.** Recreate the container with create_container_if_not_exists

<details><summary>💡 Hint</summary>

Not found is an expected result for a cache miss. Handle it and compute the value.

</details>

<details><summary>✅ Answer</summary>

**C.** Catch the exception and compute the value as a fallback

- A: The item doesn't exist yet, so retrying won't help.
- B: A query won't find an item that doesn't exist, and it costs more.
- C: Correct. Handle the exception to compute an uncached value or return a default.
- D: The container exists; the item is just missing.

Point reads raise CosmosResourceNotFoundError for missing items; use it for fallback logic.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 18. `lp4m1-018`

For each statement, select Yes if the statement is true. Otherwise, select No. An app uses an account key in its CosmosClient.

| Statement | Yes / No |
|---|---|
| Anyone holding that key has full access to all resources in the account. | ☐ |
| Account keys support conditional access policies from Entra ID. | ☐ |
| The primary and secondary keys let you rotate a key without downtime. | ☐ |
| get_container_client confirms that the container exists by calling the service. | ☐ |

<details><summary>💡 Hint</summary>

An account key is full access to everything, and Entra ID features don't apply to it.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Anyone holding that key has full access to all resources in the account. | Yes | Account keys grant full access to everything in the account. |
| Account keys support conditional access policies from Entra ID. | No | Keys don't integrate with centralized identity management or conditional access. |
| The primary and secondary keys let you rotate a key without downtime. | Yes | Two keys allow rotation without downtime. |
| get_container_client confirms that the container exists by calling the service. | No | These methods make no network calls and don't verify existence. |

Keys are simple but all-powerful; Entra ID with RBAC is preferred for production.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 19. `lp4m1-019`

The same FastAPI code must authenticate to Cosmos DB with your Azure CLI login on your laptop and with a managed identity in Azure, with no code change. What should you use?

- **A.** DefaultAzureCredential
- **B.** A connection string per environment in local.settings.json
- **C.** ManagedIdentityCredential only
- **D.** The account's primary key from an environment variable

<details><summary>💡 Hint</summary>

One credential class tries several sign-in methods in order.

</details>

<details><summary>✅ Answer</summary>

**A.** DefaultAzureCredential

- A: Correct. It picks the right credential for the environment: developer sign-in locally, managed identity in Azure.
- B: That still uses keys and different values per environment.
- C: A managed identity doesn't exist on your laptop, so local runs would fail.
- D: That's key-based access, which skips Entra ID and RBAC.

DefaultAzureCredential selects the credential for the environment: Azure CLI or Visual Studio sign-in locally, managed identity when deployed.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 20. `lp4m1-020`

A reporting service must read items with Entra ID authentication and must not be able to write. Which built-in role should its identity get?

- **A.** Cosmos DB Built-in Data Reader
- **B.** Owner on the resource group
- **C.** Cosmos DB Account Reader Role
- **D.** Cosmos DB Built-in Data Contributor

<details><summary>💡 Hint</summary>

Grant only what's needed: data access, read-only.

</details>

<details><summary>✅ Answer</summary>

**A.** Cosmos DB Built-in Data Reader

- A: Correct. It allows read operations only.
- B: Owner is far too broad for reading items.
- C: That's a control-plane role for reading account settings, not item data.
- D: Contributor allows reads and writes, which is more than this service needs.

The built-in data roles include Cosmos DB Built-in Data Reader for read operations and Cosmos DB Built-in Data Contributor for read/write.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 21. `lp4m1-021`

A few writes have unusually high latency, and you plan to open a support case. Besides the RU charge, which value should your code log so that Microsoft support can find each request?

- **A.** The item's _etag
- **B.** The partition key value
- **C.** The client's process ID
- **D.** The activity ID from the response

<details><summary>💡 Hint</summary>

Each request gets a unique identifier in the response metadata.

</details>

<details><summary>✅ Answer</summary>

**D.** The activity ID from the response

- A: The etag tracks item versions for concurrency, not individual requests.
- B: The key routes data. It doesn't identify one request.
- C: Support can't map a local process ID to a service request.
- D: Correct. The activity ID uniquely identifies each request, which helps support diagnose it.

Log the activity ID alongside errors or high RU charges. It uniquely identifies each request when working with Azure support.

📘 Source: [Implement the Azure Cosmos DB for NoSQL SDK](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/3-implement-cosmos-db-sdk)

</details>

## 22. `lp4m1-022`

You need a plain JSON array of product names, such as ["Smart Speaker", "Laptop"], without wrapping objects. Which query should you use?

- **A.** SELECT COUNT(p.name) FROM products p
- **B.** SELECT VALUE p.name FROM products p
- **C.** SELECT * FROM products p
- **D.** SELECT p.name FROM products p

<details><summary>💡 Hint</summary>

One keyword returns the bare values instead of objects.

</details>

<details><summary>✅ Answer</summary>

**B.** SELECT VALUE p.name FROM products p

- A: This returns a count, not the names.
- B: Correct. VALUE returns the scalar values without the surrounding object.
- C: This returns whole documents.
- D: This returns objects such as {"name": "…"}.

SELECT VALUE unwraps results into scalars or custom shapes.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 23. `lp4m1-023`

A search box sends a category typed by users into a query. How should you build the query?

- **A.** Concatenate the user's text into the WHERE clause
- **B.** Use a parameter such as @category with a parameters array
- **C.** Run the query as a stored procedure with the user's text inline
- **D.** Wrap the user's text in UPPER() before concatenating it

<details><summary>💡 Hint</summary>

User input never goes into the query text itself.

</details>

<details><summary>✅ Answer</summary>

**B.** Use a parameter such as @category with a parameters array

- A: Concatenating user input invites injection.
- B: Correct. Parameters prevent injection and allow query plan caching.
- C: Inline user text is still unsafe.
- D: UPPER changes case but doesn't stop injection.

Always parameterize values that come from users or external sources.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 24. `lp4m1-024`

For each statement, select Yes if the statement is true. Otherwise, select No. The products container is partitioned by `/categoryId`.

| Statement | Yes / No |
|---|---|
| A query that filters on categoryId = @category can be routed to a single partition. | ☐ |
| A query that filters only on price needs enable_cross_partition_query=True. | ☐ |
| WHERE p.name = "speaker" matches an item named "Speaker". | ☐ |

<details><summary>💡 Hint</summary>

Filtering on the partition key routes to one partition. String comparison is case-sensitive.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| A query that filters on categoryId = @category can be routed to a single partition. | Yes | Including the partition key routes the query directly. |
| A query that filters only on price needs enable_cross_partition_query=True. | Yes | Without the partition key, the query fans out across partitions. |
| WHERE p.name = "speaker" matches an item named "Speaker". | No | String comparisons are case-sensitive by default. |

Design queries to include the partition key; remember case-sensitive string comparisons.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 25. `lp4m1-025`

Each product has a features array. You need one result row per matching feature, only for features "wifi" or "bluetooth". Which query does this?

- **A.** SELECT p.name FROM products p WHERE CONTAINS(p.features, "wifi")
- **B.** SELECT p.name FROM products p WHERE ARRAY_CONTAINS(p.features, "wifi") OR ARRAY_CONTAINS(p.features, "bluetooth")
- **C.** SELECT p.name, f AS feature FROM products p JOIN f IN p.features WHERE f IN ("wifi", "bluetooth")
- **D.** SELECT VALUE p.features FROM products p WHERE p.features = "wifi"

<details><summary>💡 Hint</summary>

To get one row per array element, the query has to iterate over the array itself.

</details>

<details><summary>✅ Answer</summary>

**C.** SELECT p.name, f AS feature FROM products p JOIN f IN p.features WHERE f IN ("wifi", "bluetooth")

- A: CONTAINS is a string function, not an array membership test.
- B: ARRAY_CONTAINS returns each matching product once; it doesn't flatten the array into one row per feature.
- C: Correct. JOIN … IN flattens the array so you can filter and return individual elements.
- D: Comparing an array to a string doesn't test membership.

Use ARRAY_CONTAINS for membership; JOIN with IN to flatten arrays and filter elements.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 26. `lp4m1-026`

A dashboard query costs hundreds of RUs. Which two changes match Learn's cost optimization list? (Select two.)

- **A.** Remove all WHERE filters and filter in the app
- **B.** Project only the properties the dashboard shows
- **C.** Add the partition key to the filter where possible
- **D.** Add ORDER BY to every query to speed it up

<details><summary>💡 Hint</summary>

Use the partition key in filters and return only the fields you need.

</details>

<details><summary>✅ Answer</summary>

**B.** Project only the properties the dashboard shows  
**C.** Add the partition key to the filter where possible

- A: Filtering early reduces cost; moving filters to the app does the opposite.
- B: Correct. Returning only needed fields reduces cost.
- C: Correct. Single-partition routing costs less than fan-out.
- D: Sorting adds overhead rather than reducing it.

Filter early, project needed fields, use partition keys, limit with TOP, and tune indexes.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 27. `lp4m1-027`

Besides preventing injection, why does Learn say a frequently run query should use @parameters instead of building a new query string for each value?

- **A.** Parameters make every query single-partition automatically
- **B.** Parameters convert the query into a stored procedure
- **C.** Cosmos DB can cache and reuse the query plan for different values
- **D.** Parameters halve the RU charge of the query

<details><summary>💡 Hint</summary>

The query text stays the same while the values change. What work can the service skip the next time?

</details>

<details><summary>✅ Answer</summary>

**C.** Cosmos DB can cache and reuse the query plan for different values

- A: Routing depends on the partition key filter, not on parameters.
- B: The query stays a query. Nothing is converted.
- C: Correct. Parameterized queries allow query plan caching, which improves performance for repeated queries.
- D: Learn doesn't make that claim. The benefit is plan reuse.

Parameterized queries separate structure from values, preventing injection and letting Cosmos DB cache and reuse query plans for repeated queries with different values.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>

## 28. `lp4m1-028`

A web API returns search results 50 at a time and lets the client ask for the next page later. How should it implement paging with the SDK?

- **A.** Run SELECT * and slice the full result list in memory
- **B.** Store each page in a new container for the client to read
- **C.** Set max_item_count to 50 and return the continuation token to the client
- **D.** Use OFFSET with the client's page number on each call

<details><summary>💡 Hint</summary>

The SDK pages for you. One setting sets the page size, and one value lets you resume.

</details>

<details><summary>✅ Answer</summary>

**C.** Set max_item_count to 50 and return the continuation token to the client

- A: That reads every result on every call, which wastes RUs and memory.
- B: That adds writes and storage for no benefit.
- C: Correct. The iterator pages with continuation tokens, and max_item_count sets the page size.
- D: Learn's paging guidance is continuation tokens, which keep query state between pages.

The SDK's query iterator pages through continuation tokens. Set max_item_count for page size, and return the continuation token so clients can request the next page.

📘 Source: [Query Azure Cosmos DB for NoSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-cosmos-db/4-query-cosmos-db-nosql)

</details>


---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
