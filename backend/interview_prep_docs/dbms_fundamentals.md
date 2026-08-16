# DBMS Interview Q&A

## Question: What is the difference between DBMS and RDBMS?
DBMS is general software for storing and managing data, not necessarily in tabular form (may lack relationships, constraints, or normalization). RDBMS specifically stores data in tables with rows/columns, enforces relationships via primary/foreign keys, and supports ACID-compliant transactions and normalization. MySQL, PostgreSQL, and Oracle are RDBMS; some NoSQL stores are DBMS but not RDBMS.

## Question: What is the difference between SQL and NoSQL databases?
SQL databases are relational, use structured schemas with tables, enforce ACID properties, and scale vertically. NoSQL databases (document, key-value, column-family, graph) are schema-flexible, better suited for unstructured/semi-structured data, generally scale horizontally, and often trade strict consistency for availability/partition tolerance (per the CAP theorem) — e.g., MongoDB (document), Redis (key-value), Cassandra (column-family).

## Question: Explain the CAP theorem.
CAP theorem states a distributed data store can only guarantee two of three properties simultaneously: Consistency (every read gets the most recent write), Availability (every request gets a response, even if not the latest data), and Partition Tolerance (the system continues operating despite network partitions). Since network partitions are unavoidable in distributed systems, real systems choose between CP (consistency over availability) or AP (availability over consistency).

## Question: What is a transaction and what are its properties?
A transaction is a sequence of database operations treated as a single logical unit of work — either all operations succeed or none do. Its properties are ACID: Atomicity, Consistency, Isolation, Durability (explained in more detail in the SQL doc). Transactions are essential for maintaining data integrity in concurrent, multi-user systems.

## Question: What are database indexes and what are their trade-offs?
An index is a data structure (commonly a B-Tree or hash table) that speeds up data retrieval by avoiding full table scans. Trade-off: indexes speed up SELECT/read queries but slow down INSERT/UPDATE/DELETE operations since the index also needs to be updated, and they consume additional storage. Indexes should be added on columns frequently used in WHERE, JOIN, or ORDER BY clauses.

## Question: What is database sharding?
Sharding is a horizontal partitioning technique that splits a large database into smaller, independent pieces (shards) distributed across multiple servers, typically based on a shard key (e.g., user ID ranges). It improves scalability and performance for very large datasets, but adds complexity for cross-shard queries, joins, and maintaining consistency.

## Question: What is the difference between OLTP and OLAP?
OLTP (Online Transaction Processing) systems handle frequent, short, real-time transactions like inserts/updates (e.g., an e-commerce checkout system) — optimized for write speed and normalized schemas. OLAP (Online Analytical Processing) systems handle complex analytical queries over large historical datasets (e.g., business intelligence dashboards) — optimized for read/aggregation speed, often using denormalized star/snowflake schemas.

## Question: What is a deadlock in a database context and how is it handled?
A database deadlock occurs when two transactions each hold a lock the other needs, blocking each other indefinitely. Most RDBMSs handle this via automatic deadlock detection — periodically checking for a wait-for cycle and forcibly rolling back one of the transactions (the "victim") to break the cycle, allowing the other to proceed.

## Question: What is the difference between a view and a materialized view?
A view is a virtual table defined by a stored SQL query — it doesn't store data itself and is recomputed each time it's queried, always reflecting current underlying data. A materialized view stores the actual query result physically on disk, offering faster read performance but requiring periodic refresh to stay in sync with underlying table changes.
