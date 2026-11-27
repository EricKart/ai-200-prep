# Practice: LP5 · M1 Build and query with Azure Database for PostgreSQL

> 28 questions · try each one before opening the hint, then the answer · [lesson](../content/lessons/lp5m1.md) · [interactive version](https://aryantripathi.dev/ai-200/lp-5/build-query-azure-database-postgresql)

## 1. `lp5m1-001`

Your AI API makes many short-lived database calls and you enable the built-in PgBouncer. Which port should the app connect to?

- **A.** 443
- **B.** 6432
- **C.** 5432
- **D.** 1433

<details><summary>💡 Hint</summary>

PgBouncer listens on a different port from PostgreSQL itself.

</details>

<details><summary>✅ Answer</summary>

**B.** 6432

- A: 443 is HTTPS, not a PostgreSQL port.
- B: Correct. PgBouncer connections use port 6432.
- C: 5432 is the standard direct PostgreSQL port.
- D: 1433 is the SQL Server port.

Enable PgBouncer in server configuration and connect on 6432.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 2. `lp5m1-002`

Which PostgreSQL extension provides trigram-based fuzzy text matching for autocomplete?

- **A.** pg_trgm
- **B.** hstore
- **C.** pgvector
- **D.** PostGIS

<details><summary>💡 Hint</summary>

Fuzzy matching splits text into groups of three characters.

</details>

<details><summary>✅ Answer</summary>

**A.** pg_trgm

- A: Correct. pg_trgm provides trigram text similarity.
- B: hstore adds a key-value data type.
- C: pgvector adds vector types and similarity search.
- D: PostGIS is for geospatial capabilities.

pgvector for embeddings, pg_trgm for fuzzy text, hstore for key-value pairs.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 3. `lp5m1-003`

For each statement, select Yes if the statement is true. Otherwise, select No. A team runs a Burstable-tier Azure Database for PostgreSQL server for a proof of concept.

| Statement | Yes / No |
|---|---|
| They can enable the built-in PgBouncer on this tier. | ☐ |
| They can move to General Purpose later with a brief restart. | ☐ |
| Backups are kept for 35 days unless they change it. | ☐ |
| A point-in-time restore creates a new server instance. | ☐ |

<details><summary>💡 Hint</summary>

Burstable is for dev and doesn't get every feature. Backups default to a week, and a restore makes a new server.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| They can enable the built-in PgBouncer on this tier. | No | PgBouncer isn't available on the Burstable tier. |
| They can move to General Purpose later with a brief restart. | Yes | Compute tiers can be changed after deployment with a brief restart. |
| Backups are kept for 35 days unless they change it. | No | Default retention is seven days; you can extend it up to 35. |
| A point-in-time restore creates a new server instance. | Yes | Restore creates a new server at the chosen timestamp. |

Know the tier limits, backup defaults and how restores work.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 4. `lp5m1-004`

An AI service keeps large working sets in memory and runs complex analytical queries alongside vector operations. Which compute tier fits best?

- **A.** General Purpose (D-series)
- **B.** Memory Optimized (E-series)
- **C.** Burstable (B-series)
- **D.** Any tier, because storage scales separately

<details><summary>💡 Hint</summary>

Large in-memory working sets point to the tier named after memory.

</details>

<details><summary>✅ Answer</summary>

**B.** Memory Optimized (E-series)

- A: General Purpose is balanced, not memory-heavy.
- B: Correct. High memory-to-vCPU ratios suit large in-memory sets and analytical queries.
- C: Burstable suits dev and intermittent workloads.
- D: Storage scaling doesn't provide the memory this workload needs.

Memory Optimized for in-memory and analytical work; General Purpose for steady production.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 5. `lp5m1-005`

Yesterday a script dropped the conversations table on a production server. Backups use the default settings. How do you recover the data?

- **A.** Point-in-time restore, which rolls the existing server back in place
- **B.** You can't: backups are kept for 24 hours
- **C.** Point-in-time restore into a new server
- **D.** Open a support ticket, because backups must be requested in advance

<details><summary>💡 Hint</summary>

Automatic backups allow recovery to a point in time. Where does the restored data end up?

</details>

<details><summary>✅ Answer</summary>

**C.** Point-in-time restore into a new server

- A: A restore creates a new server instance. It doesn't overwrite the existing one.
- B: The default retention is seven days.
- C: Correct. PITR recovers to any moment within retention (seven days by default) into a new server.
- D: Backups are automatic, so you can restore yourself.

Backups are automatic, with seven days' retention by default (configurable up to 35). Point-in-time restore recovers to any moment in that window and creates a new server instance.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 6. `lp5m1-006`

Two applications share one Azure Database for PostgreSQL server. They must never see each other's data, and each needs its own backup and restore. How should you organize them?

- **A.** Put both applications in one database, with a table prefix per app
- **B.** Use one database and give each application its own schema
- **C.** Create one table per application inside the postgres system database
- **D.** Give each application its own database on the server

<details><summary>💡 Hint</summary>

A server can host several databases. When does Learn say to separate them?

</details>

<details><summary>✅ Answer</summary>

**D.** Give each application its own database on the server

- A: Prefixes don't isolate data or give independent restores.
- B: Schemas organize objects inside a database. Learn suggests separate databases for full isolation and independent restore.
- C: The system database isn't meant for application data, and this doesn't isolate anything.
- D: Correct. Separate databases give complete isolation and independent backup and restore.

A server can host multiple databases, each isolated. Use separate databases for complete isolation between applications or independent backup and restore.

📘 Source: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

</details>

## 7. `lp5m1-007`

Production code must make sure it's talking to the genuine Azure PostgreSQL server, checking both the certificate authority and the hostname. Which sslmode should it use?

- **A.** require
- **B.** prefer
- **C.** verify-full
- **D.** verify-ca

<details><summary>💡 Hint</summary>

There's an sslmode that checks both the certificate chain and the host name.

</details>

<details><summary>✅ Answer</summary>

**C.** verify-full

- A: require encrypts but doesn't validate certificates.
- B: prefer doesn't validate certificates.
- C: Correct. verify-full validates the CA and confirms the hostname.
- D: verify-ca validates the CA but not the hostname.

Use verify-full in production.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 8. `lp5m1-008`

An Azure-hosted app uses a managed identity to connect with Microsoft Entra authentication. Which resource should it request a token for?

- **A.** `https://vault.azure.net/.default`
- **B.** `https://ossrdbms-aad.database.windows.net`
- **C.** `https://management.azure.com/.default`
- **D.** `https://database.windows.net/postgres`

<details><summary>💡 Hint</summary>

Entra tokens for Azure's open-source databases come from one specific resource URL.

</details>

<details><summary>✅ Answer</summary>

**B.** `https://ossrdbms-aad.database.windows.net`

- A: That's Key Vault.
- B: Correct. Entra identities obtain tokens from this resource and use them as the password.
- C: That's the Azure Resource Manager audience.
- D: That isn't the PostgreSQL token resource Learn names.

credential.get_token("`https://ossrdbms-aad.database.windows.net/.default`")

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 9. `lp5m1-009`

Put the Microsoft Entra connection flow in order.

- Entra validates the identity and returns a token
- PostgreSQL validates the token against the configured Entra administrator
- The application connects to PostgreSQL using the token as the password
- The application requests an access token from Microsoft Entra ID

<details><summary>💡 Hint</summary>

Get a token, Entra issues it, connect with it as the password, and the server checks it.

</details>

<details><summary>✅ Answer</summary>

1. The application requests an access token from Microsoft Entra ID
2. Entra validates the identity and returns a token
3. The application connects to PostgreSQL using the token as the password
4. PostgreSQL validates the token against the configured Entra administrator

Tokens are short-lived, so no password is stored.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 10. `lp5m1-010`

For each statement, select Yes if the statement is true. Otherwise, select No. A developer can't connect from a laptop to a server that uses **private access** with VNet integration.

| Statement | Yes / No |
|---|---|
| Adding the laptop's IP to firewall rules is the fix Learn describes for private access. | ☐ |
| Connecting through a VPN into the virtual network is a valid path. | ☐ |
| A client using sslmode=disable would be rejected even on the right network. | ☐ |
| TLS 1.0 connections are accepted for older clients. | ☐ |

<details><summary>💡 Hint</summary>

Private access means connecting from inside the network. TLS is always required.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| Adding the laptop's IP to firewall rules is the fix Learn describes for private access. | No | Firewall rules apply to public access; private access is reachable only from the VNet, peered networks or VPN/ExpressRoute. |
| Connecting through a VPN into the virtual network is a valid path. | Yes | Private access works through VPN or ExpressRoute. |
| A client using sslmode=disable would be rejected even on the right network. | Yes | Azure rejects unencrypted connections. |
| TLS 1.0 connections are accepted for older clients. | No | Only TLS 1.2 and 1.3 are supported. |

Know the two networking models and the TLS requirements.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 11. `lp5m1-011`

A legacy reporting tool can only connect with TLS 1.0, and its connections to Azure Database for PostgreSQL are rejected. What does the server enforce?

- **A.** TLS by default, with TLS 1.2 and 1.3 supported
- **B.** Plain TCP unless a certificate is installed on the server
- **C.** Encryption for connections from outside Azure, plain TCP inside
- **D.** TLS 1.0 for Burstable-tier servers

<details><summary>💡 Hint</summary>

Which TLS versions does the managed service accept?

</details>

<details><summary>✅ Answer</summary>

**A.** TLS by default, with TLS 1.2 and 1.3 supported

- A: Correct. Older TLS versions are rejected, so the tool needs an upgrade.
- B: The managed server already requires TLS. You don't install certificates on it.
- C: All connections must use TLS, wherever they come from.
- D: The tier doesn't change the TLS versions accepted.

Azure Database for PostgreSQL encrypts all connections with TLS. It requires TLS by default, supports TLS 1.2 and 1.3, and rejects older versions.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 12. `lp5m1-012`

Security asks why the team should move the AI API from a database password to Microsoft Entra authentication with a managed identity. Which benefit does Learn give?

- **A.** Connections no longer need TLS
- **B.** No stored password: tokens are short-lived, and identity is managed centrally
- **C.** Queries run faster because tokens skip permission checks
- **D.** The app no longer needs PgBouncer

<details><summary>💡 Hint</summary>

Think about what the app no longer has to keep secret.

</details>

<details><summary>✅ Answer</summary>

**B.** No stored password: tokens are short-lived, and identity is managed centrally

- A: TLS is still required for every connection.
- B: Correct. Entra uses OAuth 2.0 tokens instead of passwords, which removes password storage.
- C: Tokens authenticate the identity. Database permissions still apply.
- D: Authentication and connection pooling are separate concerns.

Microsoft Entra authentication uses short-lived OAuth 2.0 tokens instead of passwords, giving centralized identity management and removing password storage.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 13. `lp5m1-013`

Your server uses public access. A new developer can't connect from home, although the same code works for teammates in the office. What should you check first?

- **A.** Whether the developer uses sslmode=disable
- **B.** Whether the server has VNet integration enabled
- **C.** Whether PgBouncer is enabled on port 6432
- **D.** Whether the developer's IP address is allowed in the firewall rules

<details><summary>💡 Hint</summary>

The code works from one network and not from another. What controls which clients can connect?

</details>

<details><summary>✅ Answer</summary>

**D.** Whether the developer's IP address is allowed in the firewall rules

- A: TLS is required, but the difference here is location, which points to the firewall.
- B: Public access servers use firewall rules, not VNet integration.
- C: Pooling doesn't explain why one location fails and another works.
- D: Correct. With public access, firewall rules control which client IPs can connect.

With public access, the server has a public IP and firewall rules control which client IPs can connect. If your machine can't connect, check that its IP is allowed.

📘 Source: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

</details>

## 14. `lp5m1-014`

A messages table will receive billions of inserts and needs a simple auto-incrementing key. Which type fits?

- **A.** VARCHAR(255)
- **B.** SERIAL
- **C.** BYTEA
- **D.** BIGSERIAL

<details><summary>💡 Hint</summary>

Billions of rows outgrow a 32-bit counter.

</details>

<details><summary>✅ Answer</summary>

**D.** BIGSERIAL

- A: Strings aren't auto-incrementing keys.
- B: SERIAL is 32-bit and can run out above about two billion rows.
- C: BYTEA stores binary data.
- D: Correct. BIGSERIAL is 64-bit, for tables that may exceed two billion rows.

Use BIGSERIAL for high-volume tables; UUIDs when IDs are generated outside the database.

📘 Source: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

</details>

## 15. `lp5m1-015`

You delete a conversation that still has messages referencing it, and the messages FK has no ON DELETE clause. What happens?

- **A.** The messages are deleted too
- **B.** The messages' conversation_id becomes NULL
- **C.** The messages get the column's default value
- **D.** The delete is prevented

<details><summary>💡 Hint</summary>

Without ON DELETE, a referenced parent can't be removed.

</details>

<details><summary>✅ Answer</summary>

**D.** The delete is prevented

- A: That's CASCADE, which you must specify.
- B: That's SET NULL.
- C: That's SET DEFAULT.
- D: Correct. RESTRICT is the default and blocks the delete when referencing rows exist.

RESTRICT is the default referential action.

📘 Source: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

</details>

## 16. `lp5m1-016`

For each statement, select Yes if the statement is true. Otherwise, select No. A table has a composite index on `(conversation_id, created_at)`.

| Statement | Yes / No |
|---|---|
| The index helps WHERE conversation_id = 42. | ☐ |
| The index helps WHERE created_at > '2024-01-01' with no conversation_id filter. | ☐ |
| Every extra index adds overhead to inserts, updates and deletes. | ☐ |

<details><summary>💡 Hint</summary>

A composite index helps filters that start with its leading column. Every index costs on writes.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| The index helps WHERE conversation_id = 42. | Yes | The index serves filters on its leading column. |
| The index helps WHERE created_at > '2024-01-01' with no conversation_id filter. | No | It can't serve filters on trailing columns alone. |
| Every extra index adds overhead to inserts, updates and deletes. | Yes | Indexes speed reads but cost storage and write work. |

Column order in composite indexes matters; be selective on write-heavy tables.

📘 Source: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

</details>

## 17. `lp5m1-017`

You must add a category column and an index on it together, so that either both changes apply or neither does. What should you do?

- **A.** Run both statements inside BEGIN … COMMIT
- **B.** Use DROP TABLE … CASCADE and recreate the table
- **C.** Run them separately; DDL can't be rolled back in PostgreSQL
- **D.** Add the column with ON DELETE CASCADE

<details><summary>💡 Hint</summary>

Group the changes so they succeed or fail together.

</details>

<details><summary>✅ Answer</summary>

**A.** Run both statements inside BEGIN … COMMIT

- A: Correct. Most DDL in PostgreSQL is transactional, so you can ROLLBACK if a statement fails.
- B: Dropping the table loses data.
- C: PostgreSQL DDL is mostly transactional, unlike some databases.
- D: ON DELETE CASCADE is a foreign key action, not a transaction.

Wrap related schema changes in a transaction.

📘 Source: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

</details>

## 18. `lp5m1-018`

A tasks table has a status column that may only hold 'pending', 'completed' or 'failed'. You want the database itself to reject any other value. What should you add?

- **A.** NOT NULL
- **B.** An index on status
- **C.** DEFAULT 'pending'
- **D.** CHECK (status IN ('pending', 'completed', 'failed'))

<details><summary>💡 Hint</summary>

Which constraint validates a value against a condition?

</details>

<details><summary>✅ Answer</summary>

**D.** CHECK (status IN ('pending', 'completed', 'failed'))

- A: NOT NULL stops nulls, but any other text would still be accepted.
- B: Indexes speed up queries. They don't validate values.
- C: A default fills in a missing value. It doesn't reject other values.
- D: Correct. A CHECK constraint validates values against a condition.

Constraints enforce rules on data: NOT NULL prevents nulls, DEFAULT provides a value, and CHECK validates values against a condition such as status IN (…).

📘 Source: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

</details>

## 19. `lp5m1-019`

You need the status field from a JSONB column as text, to compare with 'active'. Which expression should you use?

- **A.** metadata->'status'
- **B.** metadata ? 'status'
- **C.** metadata @> 'status'
- **D.** metadata->>'status'

<details><summary>💡 Hint</summary>

One arrow returns JSON, and the double arrow returns text.

</details>

<details><summary>✅ Answer</summary>

**D.** metadata->>'status'

- A: -> returns JSON, not text.
- B: ? checks that the key exists.
- C: @> tests containment of a JSON value.
- D: Correct. ->> extracts the element as text.

-> for JSON, ->> for text, ? for key existence, @> for containment.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 20. `lp5m1-020`

This query fails with "column msg_date does not exist": `SELECT DATE(created_at) AS msg_date FROM messages WHERE msg_date > '2024-01-01'`. Why?

- **A.** WHERE runs before SELECT, so the alias isn't defined yet
- **B.** Aliases can't contain an underscore in PostgreSQL
- **C.** The column has to be cast to TIMESTAMPTZ first
- **D.** DATE() isn't a supported function in PostgreSQL

<details><summary>💡 Hint</summary>

Clauses don't run in the order you write them.

</details>

<details><summary>✅ Answer</summary>

**A.** WHERE runs before SELECT, so the alias isn't defined yet

- A: Correct. Repeat the expression in WHERE, or use the alias in ORDER BY.
- B: Underscores are fine in aliases; the problem is when WHERE runs.
- C: Casting doesn't create the alias for WHERE.
- D: DATE() works; the alias is the problem.

Only clauses after SELECT (ORDER BY, LIMIT/OFFSET) can use SELECT aliases.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 21. `lp5m1-021`

An API pages through millions of messages 20 at a time, and page 1,000 has become very slow with OFFSET. What should you use instead?

- **A.** Keyset pagination on (created_at, id) from the last row
- **B.** A recursive CTE that walks the messages in order
- **C.** ORDER BY created_at NULLS LAST with the same OFFSET
- **D.** A larger OFFSET with LIMIT 200 to cut round trips

<details><summary>💡 Hint</summary>

OFFSET reads and discards every skipped row.

</details>

<details><summary>✅ Answer</summary>

**A.** Keyset pagination on (created_at, id) from the last row

- A: Correct. Keyset pagination filters from the last seen values and stays fast at any depth; id breaks ties.
- B: Recursive CTEs are for hierarchies.
- C: NULL ordering doesn't fix deep pagination.
- D: Bigger pages still scan and discard skipped rows.

OFFSET scans and discards skipped rows; keyset pagination doesn't.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 22. `lp5m1-022`

For each statement, select Yes if the statement is true. Otherwise, select No. A checkpoint write uses `INSERT … ON CONFLICT (task_id, step_number) DO UPDATE SET checkpoint_data = EXCLUDED.checkpoint_data RETURNING id, (xmax = 0) AS is_new`.

| Statement | Yes / No |
|---|---|
| EXCLUDED refers to the values that would have been inserted. | ☐ |
| is_new is true when the row was updated rather than inserted. | ☐ |
| RETURNING gives back the id in the same round trip. | ☐ |
| Using DO NOTHING instead would update the existing checkpoint. | ☐ |

<details><summary>💡 Hint</summary>

EXCLUDED is the row you tried to insert, and RETURNING saves a round trip.

</details>

<details><summary>✅ Answer</summary>

| Statement | Answer | Why |
|---|---|---|
| EXCLUDED refers to the values that would have been inserted. | Yes | EXCLUDED is the pseudo-table of proposed values. |
| is_new is true when the row was updated rather than inserted. | No | xmax = 0 is true for newly inserted rows. |
| RETURNING gives back the id in the same round trip. | Yes | RETURNING avoids a separate query. |
| Using DO NOTHING instead would update the existing checkpoint. | No | DO NOTHING skips the conflicting row. |

Upserts make checkpoint writes idempotent; RETURNING tells you what happened.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 23. `lp5m1-023`

A dashboard must list every conversation with its message count, including conversations that have no messages yet. Which join keeps the conversations with zero messages?

- **A.** conversations INNER JOIN message_stats
- **B.** conversations CROSS JOIN message_stats
- **C.** message_stats WHERE conversation_id IS NOT NULL
- **D.** conversations LEFT JOIN message_stats

<details><summary>💡 Hint</summary>

You need every row from one side, whether or not the other side matches.

</details>

<details><summary>✅ Answer</summary>

**D.** conversations LEFT JOIN message_stats

- A: An inner join drops conversations that have no matching messages.
- B: A cross join pairs every row with every row, which isn't a count per conversation.
- C: This only returns conversations that have messages.
- D: Correct. A LEFT JOIN keeps every row from the left table, even with no match.

A LEFT JOIN returns every row from the left table with matching rows from the right, filling non-matches with NULL, so conversations with zero messages stay in the result.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 24. `lp5m1-024`

You need only the conversations that have more than 100 messages, using GROUP BY conversation_id and COUNT(*). Where does the condition COUNT(*) > 100 go?

- **A.** In the ORDER BY clause
- **B.** In a LIMIT 100 clause
- **C.** In the WHERE clause before GROUP BY
- **D.** In a HAVING clause after GROUP BY

<details><summary>💡 Hint</summary>

Rows are filtered before grouping. Groups are filtered after.

</details>

<details><summary>✅ Answer</summary>

**D.** In a HAVING clause after GROUP BY

- A: ORDER BY sorts results. It doesn't filter them.
- B: LIMIT caps how many rows come back. It doesn't test counts.
- C: WHERE filters rows before grouping, so the count doesn't exist yet.
- D: Correct. HAVING filters groups after aggregation.

WHERE filters rows before GROUP BY; HAVING filters groups after aggregation. Aliases from SELECT are visible only to ORDER BY and LIMIT/OFFSET.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 25. `lp5m1-025`

A search box should find messages that contain "azure" whatever the capitalization, such as "Azure" or "AZURE". Which operator does Learn suggest?

- **A.** ILIKE '%azure%'
- **B.** SIMILAR TO 'Azure'
- **C.** LIKE '%azure%'
- **D.** = 'azure'

<details><summary>💡 Hint</summary>

There's a case-insensitive version of LIKE.

</details>

<details><summary>✅ Answer</summary>

**A.** ILIKE '%azure%'

- A: Correct. ILIKE does case-insensitive pattern matching without LOWER().
- B: This is case-sensitive pattern matching, and it needs the whole string to match.
- C: LIKE is case-sensitive, so "Azure" wouldn't match.
- D: Equality needs the whole value to match exactly.

The ILIKE operator provides case-insensitive pattern matching without functions like LOWER(), which suits user-facing search.

📘 Source: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

</details>

## 26. `lp5m1-026`

A nightly job loads 2 million chat messages into PostgreSQL from Python. Which approach does Learn say is fastest?

- **A.** One INSERT per row in a loop
- **B.** executemany with all 2 million rows
- **C.** The COPY command through cursor.copy()
- **D.** An INSERT … ON CONFLICT for each row

<details><summary>💡 Hint</summary>

Bulk loads have a dedicated protocol that's much faster than INSERT statements.

</details>

<details><summary>✅ Answer</summary>

**C.** The COPY command through cursor.copy()

- A: Individual inserts maximize round trips.
- B: executemany suits hundreds to a few thousand rows.
- C: Correct. COPY is often 2–10 times faster for 10,000+ rows.
- D: Per-row upserts are slower still.

Batch with executemany for moderate sizes; use COPY for large loads.

📘 Source: [Integrate SDKs and applications](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/6-integrate-sdks-apps)

</details>

## 27. `lp5m1-027`

Match each psycopg error to the handling Learn recommends.

Choices: **Retry with exponential backoff** · **Roll back; don't retry** · **Roll back and retry**

- OperationalError from a dropped connection
- UniqueViolation on an email column
- DeadlockDetected

<details><summary>💡 Hint</summary>

Transient errors are worth retrying. Data errors aren't.

</details>

<details><summary>✅ Answer</summary>

- OperationalError from a dropped connection → **Retry with exponential backoff**. Transient connection failures are retry candidates.
- UniqueViolation on an email column → **Roll back; don't retry**. Constraint violations need code or data changes, not retries.
- DeadlockDetected → **Roll back and retry**. PostgreSQL terminates one transaction; roll back and retry.

Retry transient failures and deadlocks; don't retry constraint or syntax errors.

📘 Source: [Integrate SDKs and applications](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/6-integrate-sdks-apps)

</details>

## 28. `lp5m1-028`

A FastAPI service opens a new PostgreSQL connection per request and builds queries with f-strings. Which two changes follow Learn's guidance? (Select two.)

- **A.** Borrow connections from a psycopg_pool ConnectionPool
- **B.** Use %s placeholders with a parameters tuple
- **C.** Retry UniqueViolation errors with backoff
- **D.** Raise statement_timeout to several hours for safety

<details><summary>💡 Hint</summary>

Reuse connections, and never build SQL from strings.

</details>

<details><summary>✅ Answer</summary>

**A.** Borrow connections from a psycopg_pool ConnectionPool  
**B.** Use %s placeholders with a parameters tuple

- A: Correct. Pools avoid the cost of creating connections for every request.
- B: Correct. Parameterized queries prevent SQL injection.
- C: Constraint violations shouldn't be retried.
- D: Web apps typically use short timeouts (5–30 seconds).

Pool connections, parameterize queries, set sensible timeouts, and retry only transient errors.

📘 Source: [Integrate SDKs and applications](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/6-integrate-sdks-apps)

</details>

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Practice questions written from the public Microsoft Learn course AI-200T00. Not real exam questions. Not affiliated with Microsoft.
