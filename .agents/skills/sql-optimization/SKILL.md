---
name: sql-optimization
description: Use when tuning SQL queries, indexes, pagination, batch operations, or database performance using execution plans and measurements. Supports MySQL, PostgreSQL, SQL Server, and Oracle by adapting guidance to the actual engine and version while preserving query results.
---

# SQL Optimization

Optimize the query, selection, or path specified by the user. If no scope is given, identify the slow query or affected feature before expanding the inspection. Adapt every example to the actual database engine and version.

## Scope, correctness, and measurement

- Identify the engine/version, schema, indexes, uniqueness and nullability constraints, collations, time-zone rules, data distribution, and representative workload.
- Preserve required output columns, row multiplicity, NULL behavior, comparisons, tenant/authorization filters, ordering, and pagination contracts. Compare baseline and candidate results before claiming an optimization.
- Treat the examples as candidates, not guaranteed improvements. Inspect execution plans and compare latency, rows processed, reads, memory, and write overhead under comparable conditions.
- Prefer a non-executing plan first. Runtime plans such as PostgreSQL `EXPLAIN ANALYZE` execute the statement and can have side effects; use an approved isolated environment for execution and load tests.
- Propose index/schema/configuration changes with compatibility, locking, storage, write-cost, and recovery considerations. Obtain authorization before applying database changes or production operations.

Syntax labels below are examples, not a portability guarantee: `YEAR()` is shown for MySQL/SQL Server; `LIMIT` for MySQL/PostgreSQL; expression/partial indexes and temporary tables have engine-specific rules. SQL Server and Oracle pagination and batch syntax must be adapted to the installed version.

## 🎯 Core Optimization Areas

### Query Performance Analysis

The join rewrite below assumes `customers.id` is unique. Without that constraint, preserve the membership semantics with `EXISTS` or another proven equivalent. Bind range boundaries using the original date/time and time-zone semantics.

```sql
-- Baseline: Date expression and membership filter
-- YEAR() example: MySQL 8.4 / SQL Server 2022.
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
WHERE YEAR(o.created_at) = 2024
  AND o.customer_id IN (
      SELECT c.id FROM customers c WHERE c.status = 'active'
  );

-- Candidate: Same required columns; measure the range predicate and join
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01'
  AND o.created_at < '2025-01-01'
  AND c.status = 'active';

-- Candidate indexes; inspect existing indexes and plans before choosing:
-- CREATE INDEX idx_orders_created_at ON orders(created_at);
-- CREATE INDEX idx_customers_status ON customers(status);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### Index Strategy Optimization

Choose column order from actual equality/range predicates and ordering. The larger index may be useful for another workload; avoid calling it unsuitable without plans and usage evidence. Full-text search requires the engine's full-text facilities.

```sql
-- Baseline: Wider composite index to evaluate
CREATE INDEX idx_user_data ON users(email, first_name, last_name, created_at);

-- Candidate: Alternative key order for the measured workload
-- For queries filtering by email first, then sorting by created_at
CREATE INDEX idx_users_email_created ON users(email, created_at);

-- For B-tree lookups/orderings by last_name, then first_name; not full-text search
CREATE INDEX idx_users_name ON users(last_name, first_name);

-- PostgreSQL 18 partial index / SQL Server 2022 filtered index example;
-- adapt for the actual engine (this WHERE syntax is not MySQL 8.4 CREATE INDEX).
-- For user status queries
CREATE INDEX idx_users_status_created ON users(status, created_at)
WHERE status IS NOT NULL;
```

### Subquery Optimization

The window alternative requires window-function support (for example MySQL 8.4, PostgreSQL 18, SQL Server 2022, or Oracle 19c). Preserve the original equality behavior for nullable category keys; measure both plans.

```sql
-- Baseline: Correlated subquery
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price)
    FROM products p2
    WHERE p2.category_id = p.category_id
);

-- Candidate: Window function approach
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) as avg_category_price
    FROM products
    WHERE category_id IS NOT NULL
) ranked
WHERE price > avg_category_price;
```

## 📊 Performance Tuning Techniques

### JOIN Optimization

Keep optional child rows and duplicate multiplicity. The customer join below can be inner because the baseline WHERE clause rejects missing/inactive customers; the order-item and product joins must remain left joins.

```sql
-- Baseline: Outer joins with a customer filter
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
  AND c.status = 'active';

-- Candidate: Simplify the customer join; preserve optional children
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id AND c.status = 'active'
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

### Pagination Optimization

`LIMIT` syntax below is for MySQL 8.4 / PostgreSQL 18. Use the installed SQL Server/Oracle pagination syntax. The timestamp cursor assumes `created_at` is non-NULL and `id` is unique; bind both values from the last returned row using query parameters. Define snapshot/concurrent-update behavior for the API. An ID-only cursor uses a different sort contract.

```sql
-- Baseline: OFFSET pagination; inspect large-offset cost
SELECT * FROM products
ORDER BY created_at DESC, id DESC
LIMIT 20 OFFSET 10000;

-- Candidate: Cursor-based pagination
SELECT * FROM products
WHERE created_at < '2024-06-15 10:30:00'
   OR (created_at = '2024-06-15 10:30:00' AND id < 1003)
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Or using ID-based cursor
SELECT * FROM products
WHERE id > 1000
ORDER BY id
LIMIT 20;
```

### Aggregation Optimization

The candidate returns one row with three columns instead of three separate result sets. Preserve the caller's result mapping or obtain approval for the contract change. Compare counts on the same logical snapshot: separate statements may observe different concurrent changes depending on engine/isolation, and a READ COMMITTED transaction alone may not give all statements one snapshot. Validate the intended isolation and concurrent-write behavior on the target engine.

```sql
-- Baseline: Multiple separate aggregation queries
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- Candidate: Single query with conditional aggregation
SELECT
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
FROM orders;
```

## 🔍 Query Anti-Patterns

### SELECT Performance Issues

Select explicit columns when they preserve the caller's required output contract. Narrowing a result shape is not automatically a compatible rewrite.

```sql
-- Baseline: Full result projection
SELECT * FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- Candidate: Explicit column selection
SELECT lt.id, lt.name, at.value
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;
```

### WHERE Clause Optimization

Retain the original comparison and collation semantics. A raw lowercase equality is not equivalent to `UPPER()` under a case-sensitive collation. Keep the predicate and consider an expression/computed-column index supported by the engine; case-insensitive types/collations require a deliberate compatibility decision.

```sql
-- Baseline: Function calls in WHERE clause
SELECT * FROM orders
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- Candidate: Preserve the exact predicate; measure with a matching index.
SELECT * FROM orders
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- PostgreSQL 18 expression index; choose only after checking the plan:
CREATE INDEX idx_orders_email_upper ON orders(UPPER(customer_email));
-- MySQL 8.4 functional-key syntax: ON orders ((UPPER(customer_email))).
-- SQL Server: inspect a supported indexed computed column instead.
```

### OR vs UNION Optimization

Use `UNION ALL` only if the branches are disjoint (as these category values are), or preserve overlapping-row multiplicity explicitly. `UNION` deduplicates and can also change results. Benchmark rather than assuming OR is slower.

```sql
-- Baseline: Complex OR conditions
SELECT * FROM products
WHERE (category = 'electronics' AND price < 1000)
   OR (category = 'books' AND price < 50);

-- Candidate: Disjoint branches; compare plan and runtime
SELECT * FROM products WHERE category = 'electronics' AND price < 1000
UNION ALL
SELECT * FROM products WHERE category = 'books' AND price < 50;
```

## 📈 Batch and Intermediate-Result Optimization

### Batch Operations

The multi-row `VALUES` example fits MySQL 8.4, PostgreSQL 18, and SQL Server 2022. Use the installed Oracle version's supported batching syntax. Bound batch sizes, preserve transaction/failure semantics, and respect engine/driver parameter limits.

```sql
-- Baseline: Row-by-row operations
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- Candidate: Batch insert
INSERT INTO products (name, price) VALUES
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

### Temporary Table Usage

This `CREATE TEMPORARY TABLE ... AS SELECT` example is for MySQL 8.4 / PostgreSQL 18. SQL Server uses its temporary-table syntax; Oracle temporary-table definition and lifetime differ. Compare materialization overhead and transaction/session lifetime with CTEs or derived tables before choosing.

```sql
-- Candidate: Using temporary tables for complex operations
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id,
       SUM(total_amount) as total_spent,
       COUNT(*) as order_count
FROM orders
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

-- Use the temp table for further calculations
SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

## 🛠️ Index Management

### Index Design Principles
```sql
-- Candidate: Covering index design
CREATE INDEX idx_orders_covering
ON orders(customer_id, created_at)
INCLUDE (total_amount, status);  -- SQL Server 2022 / PostgreSQL 18 syntax
-- MySQL 8.4 candidate: ON orders(customer_id, created_at, total_amount, status).
-- Extra key columns differ from INCLUDE payload columns; inspect size/write cost.
-- Adapt Oracle covering strategies to the actual engine/version.
```

### Partial Index Strategy

The following predicate index is PostgreSQL 18 partial-index / SQL Server 2022 filtered-index syntax. MySQL 8.4 does not support this `CREATE INDEX ... WHERE` form. Verify that workload predicates can use the index; adapt other engines rather than copying this syntax.

```sql
-- Candidate: Partial indexes for specific conditions
CREATE INDEX idx_orders_active
ON orders(created_at)
WHERE status IN ('pending', 'processing');
```

## 📊 Performance Monitoring Queries

### Query Performance Analysis
```sql
-- Generic approach to identify slow queries
-- (Specific syntax varies by database)

-- MySQL 8.4: requires slow-query logging with TABLE output and authorized access.
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- PostgreSQL 18: requires configured pg_stat_statements and authorized visibility.
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC;

-- SQL Server 2022: requires appropriate server-state visibility permissions.
SELECT
    qs.total_elapsed_time / NULLIF(qs.execution_count, 0) as avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

## 🎯 Optimization Checklist

### Query Structure
- [ ] Choosing explicit columns when the output contract allows it
- [ ] Using appropriate JOIN types (INNER vs LEFT/RIGHT)
- [ ] Filtering early in WHERE clauses
- [ ] Using EXISTS instead of IN for subqueries when appropriate
- [ ] Checking sargability or matching expression indexes without changing comparison semantics

### Index Strategy
- [ ] Creating indexes on frequently queried columns
- [ ] Using composite indexes in the right column order
- [ ] Avoiding over-indexing (impacts INSERT/UPDATE performance)
- [ ] Using covering indexes where beneficial
- [ ] Considering partial/filtered indexes only on supported engines and matching workloads

### Data Types and Schema
- [ ] Using appropriate data types for storage efficiency
- [ ] Normalizing appropriately (3NF for OLTP, denormalized for OLAP)
- [ ] Using constraints to help query optimizer
- [ ] Partitioning large tables when appropriate

### Query Patterns
- [ ] Using LIMIT/TOP for result set control
- [ ] Using a stable unique cursor order and defining concurrent-update behavior
- [ ] Using batch operations for bulk data changes
- [ ] Avoiding N+1 query problems
- [ ] Using prepared statements for repeated queries

### Performance Testing
- [ ] Verifying equivalent results, NULLs, duplicate rows, collation, and pagination boundaries
- [ ] Testing queries with realistic data volumes
- [ ] Analyzing query execution plans
- [ ] Monitoring query performance over time
- [ ] Setting up alerts for slow queries
- [ ] Regular index usage analysis

## 📝 Optimization Methodology

1. **Identify**: Use database-specific tools to find slow queries
2. **Analyze**: Examine execution plans and identify bottlenecks
3. **Optimize**: Propose engine/version-specific candidates that preserve the result contract
4. **Test**: Verify result equivalence first, then measure performance under comparable workloads
5. **Monitor**: Continuously track performance metrics
6. **Iterate**: Regular performance review and optimization

Report the inspected scope, engine/version, baseline and candidate results, measured plan/performance differences, and skipped checks. Without target-engine execution, report the candidate and validation limits rather than claiming a speedup.

### Engine documentation

Consult only the sources relevant to the detected engine/version:

- [PostgreSQL 18 JOIN semantics](https://www.postgresql.org/docs/18/queries-table-expressions.html), [expression indexes](https://www.postgresql.org/docs/18/indexes-expressional.html), and [partial indexes](https://www.postgresql.org/docs/18/indexes-partial.html).
- [PostgreSQL 18 EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html) and [pg_stat_statements](https://www.postgresql.org/docs/18/pgstatstatements.html), and [transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html).
- [MySQL 8.4 CREATE INDEX](https://dev.mysql.com/doc/refman/8.4/en/create-index.html).
- [SQL Server CREATE INDEX](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-index-transact-sql?view=sql-server-ver16).
- [Oracle 19c analytic functions](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/Analytic-Functions.html); check the installed release's SQL reference for pagination, temporary-table, index, and batch syntax.
