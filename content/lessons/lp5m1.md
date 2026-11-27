# LP5 · M1: Build and query with Azure Database for PostgreSQL

> **Learning path 5:** Develop AI solutions with Azure Database for PostgreSQL · **Skill area 2:** Develop AI solutions with Azure data services · about 89 min on Microsoft Learn  
> Study it interactively at [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200/lp-5/build-query-azure-database-postgresql)

Azure Database for PostgreSQL is managed PostgreSQL with a rich extension ecosystem. This module covers the service, connecting securely, schema design, SQL queries, and using it from Python.

**In this lesson**

1. [Explore Azure Database for PostgreSQL](#explore-azure-database-for-postgresql)
2. [Connect to PostgreSQL](#connect-to-postgresql)
3. [Create and manage schemas](#create-and-manage-schemas)
4. [Query data](#query-data)
5. [Integrate SDKs and applications](#integrate-sdks-and-applications)

## Explore Azure Database for PostgreSQL

📘 Microsoft Learn: [Explore Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/2-explore-azure-database-postgresql)

Azure Database for PostgreSQL is **community PostgreSQL that Microsoft runs for you**: patching, backups and high availability are handled. Pick a size class (Burstable for dev, General Purpose for steady production, Memory Optimized for big in-memory work) and add superpowers with **extensions** such as pgvector.

**Key facts**

- Fully managed, based on the **community edition** of PostgreSQL. Microsoft manages hardware, patching, backups and HA; you control maintenance windows, HA options and compute.
- Compute and storage are separate: the engine runs on a **Linux VM**; data lives on Azure managed storage with locally redundant replicas.
- Tiers: **Burstable** (B-series; dev, small or intermittent), **General Purpose** (D-series; balanced production), **Memory Optimized** (E-series; high memory-to-vCPU, caching-heavy, analytical, in-memory AI work). Change tiers later with a **brief restart**.
- Backups: automatic, on **zone-redundant** storage where zones exist (else locally redundant). Retention **7 days by default, up to 35**. Full snapshots + transaction logs → **point-in-time restore** to any second; AES 256-bit encryption (platform- or customer-managed keys).
- Point-in-time restore creates a **new server** at the chosen timestamp.
- Built-in **PgBouncer** connection pooler: enable in server configuration, connect on **port 6432** (not 5432). **Not available on Burstable**.
- Extensions add types, functions, operators and index types: **pgvector** (vectors and similarity search), **pg_trgm** (trigram fuzzy text matching, autocomplete), **hstore** (key-value type). Enable with `CREATE EXTENSION`.

| Tier | VM series | Fits |
|---|---|---|
| Burstable | B | Dev, test, proof of concept, intermittent load (no PgBouncer) |
| General Purpose | D | Typical production web apps and backends |
| Memory Optimized | E | Large in-memory sets, analytics, in-memory AI computations |

> [!WARNING]
> **Exam traps**
>
> - PgBouncer: port **6432**, General Purpose or Memory Optimized only.
> - Backup retention: 7 days default, max **35**.
> - PITR restores to a **new** server.

## Connect to PostgreSQL

📘 Microsoft Learn: [Connect to PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/3-connect-to-postgresql)

To connect you need the server address (`name.postgres.database.azure.com`), port, database, user and a password. With **Entra ID**, the "password" is a short-lived token. Always encrypt; in production also **verify the certificate and hostname** (sslmode=verify-full).

**Key facts**

- Endpoint: `<server-name>.postgres.database.azure.com`; resolves to a public IP (public access) or private IP (VNet integration).
- Parameters: host, port (**5432** direct, **6432** PgBouncer), database, username (Entra: `username@servername`), password or token, SSL mode.
- **Microsoft Entra authentication**: OAuth 2.0 tokens, no stored passwords, managed identities, audit in Entra sign-in logs. Configure an **Entra administrator** on the server; request tokens for `https://ossrdbms-aad.database.windows.net` and use the token **as the password**.
- **PostgreSQL native authentication**: for legacy apps, identities outside your tenant, or no Azure connectivity. Store passwords in **Key Vault**, rotate, use strong random passwords, limit permissions. The server admin created at provisioning uses native auth.
- TLS is required by default; **TLS 1.2 and 1.3** supported; older versions rejected.
- sslmode: **disable** (rejected by Azure), allow, prefer, **require** (encrypt, no cert check), **verify-ca** (validate CA), **verify-full** (validate CA and hostname; use in production). Root CAs: DigiCert and Microsoft.
- Enable PgBouncer: `az postgres flexible-server parameter set --name pgbouncer.enabled --value true`, then use port 6432.
- Networking: **public access** with firewall rules (add your client IP) or **private access** with VNet integration (reach only from the VNet, peered networks, VPN or ExpressRoute).

| sslmode | Encrypts | Validates CA | Validates hostname |
|---|---|---|---|
| require | Yes | No | No |
| verify-ca | Yes | Yes | No |
| verify-full | Yes | Yes | Yes |

> [!WARNING]
> **Exam traps**
>
> - Entra token resource: **https://ossrdbms-aad.database.windows.net**.
> - sslmode=disable is rejected by Azure.
> - Can't connect from your laptop on public access? Check the **firewall rules**.

## Create and manage schemas

📘 Microsoft Learn: [Create and manage schemas](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/4-create-manage-schemas)

Server → databases → schemas → tables. Pick types that fit: **JSONB** for flexible metadata, **TIMESTAMPTZ** for times, **BIGSERIAL** for busy auto-numbered tables. Foreign keys keep relationships honest; indexes speed reads but slow writes.

**Key facts**

- Hierarchy: server → **databases** (isolated; can't query across them) → **schemas** (namespaces; default **public**) → tables. Separate databases for full isolation or independent backup; schemas for FK references and cross-namespace joins.
- Primary keys: **SERIAL** (32-bit) / **BIGSERIAL** (64-bit, for tables that may exceed two billion rows), **UUID** with `gen_random_uuid()` (generate outside the DB or merge sources), composite keys.
- Constraints: NOT NULL, DEFAULT, **CHECK** (e.g. `status IN ('pending','completed')`), UNIQUE.
- Types: **JSONB** (binary JSON, indexable), TEXT vs VARCHAR(n) (no performance difference; VARCHAR enforces a max), **TIMESTAMPTZ** (stored in UTC), BYTEA (small binary; large files in Blob Storage).
- Foreign keys: one-to-many with a FK in the "many" table; many-to-many with a **junction table** and composite primary key.
- Referential actions: **RESTRICT (default)**, CASCADE, SET NULL, SET DEFAULT. Use ON DELETE CASCADE carefully.
- **B-tree** is the default index type (equality and ranges). Composite index column order matters: it serves filters on the **leading** columns. PKs and UNIQUE constraints get indexes automatically.
- ALTER TABLE ADD COLUMN with a default is efficient (default stored in the catalog). DROP TABLE is blocked by referencing FKs unless CASCADE. Most **DDL is transactional**: BEGIN … COMMIT or ROLLBACK.

| Need | Type |
|---|---|
| Variable metadata, nested objects | JSONB |
| Times across time zones | TIMESTAMP WITH TIME ZONE |
| Auto-numbered ID, billions of rows | BIGSERIAL |
| ID generated outside the database | UUID DEFAULT gen_random_uuid() |
| Enforce a maximum string length | VARCHAR(n) |

> [!WARNING]
> **Exam traps**
>
> - Default referential action is **RESTRICT**.
> - An index on (conversation_id, created_at) doesn't serve a filter on created_at alone.

## Query data

📘 Microsoft Learn: [Query data](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/5-query-data)

PostgreSQL adds handy tools: **ILIKE** for case-insensitive search, **->>** to pull text out of JSONB, **@>** to test what JSONB contains, **keyset pagination** that stays fast on page 1,000, **RETURNING** to get new IDs back, and **ON CONFLICT** for upserts.

**Key facts**

- Logical order: FROM → WHERE → GROUP BY → HAVING → **SELECT** → ORDER BY → LIMIT/OFFSET. Aliases defined in SELECT work in **ORDER BY** but **not in WHERE**.
- **ILIKE** = case-insensitive pattern match. **NULLS FIRST / NULLS LAST** control NULL placement (default: NULLs sort as if larger). **COALESCE** returns the first non-null value.
- JSONB: **->** returns JSON, **->>** returns text; **#>** / **#>>** for nested paths. **?** = key exists; **@>** = contains. These can use **GIN** indexes. `jsonb_array_elements` expands arrays.
- **Keyset pagination**: filter from the last seen values (`WHERE (created_at, id) < (…)`) instead of OFFSET, which scans and discards skipped rows. Include **id** to break ties.
- **CTEs** (WITH) build queries step by step; **recursive CTEs** walk trees (task hierarchies, threads); always add a depth limit.
- **RETURNING** gets generated IDs and defaults in one round trip.
- **INSERT … ON CONFLICT**: DO UPDATE (with **EXCLUDED** for the proposed values) or DO NOTHING. `(xmax = 0)` in RETURNING is true for **inserted** rows.

| Need | PostgreSQL feature |
|---|---|
| Match 'Error' or 'error' | ILIKE '%error%' |
| Status field from JSONB as text | metadata->>'status' |
| Rows whose JSONB contains {"status":"completed"} | @> |
| Fast deep pagination | Keyset (WHERE on last seen values) |
| Insert or update in one statement | ON CONFLICT … DO UPDATE SET … EXCLUDED |

> [!WARNING]
> **Exam traps**
>
> - Aliases can't be used in WHERE.
> - OFFSET gets slower the deeper you page.
> - xmax = 0 → the row was inserted, not updated.

## Integrate SDKs and applications

📘 Microsoft Learn: [Integrate SDKs and applications](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/6-integrate-sdks-apps)

In Python use **psycopg 3**. Always pass values as **parameters** (never glue strings together), use `with` blocks so connections close, set timeouts, retry only **transient** errors, and borrow connections from a **pool**.

**Key facts**

- **psycopg (version 3)** is the recommended Python adapter: sync and async, pooling, full PostgreSQL support. `pip install "psycopg[binary]"` for the simplest setup.
- `psycopg.connect()` with a connection string or individual parameters; context managers (`with`) close connections and cursors even on exceptions.
- Parameterized queries with **%s** or **%(name)s**; never string formatting with user input.
- fetchone() for one row, fetchall() for small sets, iterate the cursor for large results.
- Timeouts: `connect_timeout` and `statement_timeout` (web apps typically 5–30 s).
- Retry with exponential backoff on **OperationalError** (connection or timeout); **don't retry** constraint violations or syntax errors.
- Catch **UniqueViolation**, **ForeignKeyViolation**, **CheckViolation** and roll back. On **DeadlockDetected**, roll back and retry; acquire locks in a consistent order. Handle LockNotAvailable similarly.
- Batch inserts (`executemany` for hundreds to a few thousand rows); **COPY** for 10,000+ rows (often 2–10× faster). Drivers usually prepare parameterized statements.
- Use a pool: `ConnectionPool(connection_string, min_size=1, max_size=10)` from psycopg_pool.

| Error | What to do |
|---|---|
| OperationalError (network, timeout) | Retry with exponential backoff |
| UniqueViolation / ForeignKeyViolation / CheckViolation | Roll back; give meaningful feedback; don't retry |
| DeadlockDetected | Roll back and retry; lock in a consistent order |
| Syntax error | Fix the code; don't retry |

> [!WARNING]
> **Exam traps**
>
> - COPY for 10,000+ rows; executemany for hundreds to a few thousand.
> - Never build SQL with f-strings from user input.

## Check yourself

- **Practice questions:** [lp5m1 on GitHub](../../practice/lp5m1.md), or [on the site](https://aryantripathi.dev/ai-200/lp-5/build-query-azure-database-postgresql) with hints and saved progress
- **Cheat sheet:** [Learning path 5](../cheatsheets/lp5.md)
- **Microsoft Learn exercise:** [Build an agent tool backend on Azure Database for PostgreSQL](https://learn.microsoft.com/en-us/training/modules/build-query-azure-database-postgresql/7-exercise-build-agent-tool-backend)
- **Hands-on lab:** [labs/](../../labs/README.md) has a lab for this learning path

---

Part of **AI-200 Prep**, a free course by Aryan Tripathi · [aryantripathi.dev/ai-200](https://aryantripathi.dev/ai-200) · Written from the public Microsoft Learn course AI-200T00. Not affiliated with Microsoft.
