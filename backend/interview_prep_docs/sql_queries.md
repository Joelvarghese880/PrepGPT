# SQL Interview Q&A

## Question: What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN?
INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table plus matched rows from the right (unmatched right columns are NULL). FULL OUTER JOIN returns all rows from both tables, with NULLs where there's no match on either side. RIGHT JOIN is the mirror of LEFT JOIN.

## Question: What is the difference between WHERE and HAVING?
WHERE filters individual rows before any grouping/aggregation happens, and cannot use aggregate functions like COUNT() or SUM() directly. HAVING filters groups after a GROUP BY has been applied, and is used specifically to filter based on aggregate function results, e.g., `HAVING COUNT(*) > 5`.

## Question: Write a query to find the second highest salary from an Employee table.
```sql
SELECT MAX(salary) AS second_highest
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```
Alternative using DENSE_RANK for the Nth highest generically:
```sql
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM Employee
) ranked
WHERE rnk = 2;
```

## Question: What is a primary key vs a foreign key?
A primary key uniquely identifies each row in a table — it cannot be NULL and must be unique. A foreign key is a column (or set of columns) in one table that references the primary key of another table, enforcing referential integrity between the two tables.

## Question: Explain the difference between DELETE, TRUNCATE, and DROP.
DELETE removes rows based on a WHERE condition (or all rows if no condition), is logged row-by-row, and can be rolled back. TRUNCATE removes all rows at once, resets auto-increment counters, is faster since it's minimally logged, but generally cannot be rolled back in most databases. DROP removes the entire table structure along with its data from the database.

## Question: What are database normalization forms (1NF, 2NF, 3NF)?
1NF requires atomic (indivisible) column values with no repeating groups. 2NF requires 1NF plus every non-key column being fully dependent on the entire primary key (relevant for composite keys, eliminating partial dependency). 3NF requires 2NF plus no transitive dependency — non-key columns shouldn't depend on other non-key columns. Normalization reduces data redundancy and improves data integrity.

## Question: Write a query to find duplicate emails in a Person table.
```sql
SELECT email, COUNT(*) as count
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

## Question: What is the difference between a clustered and non-clustered index?
A clustered index determines the physical storage order of table data — there can only be one per table since data rows can only be sorted one way. A non-clustered index is a separate structure that stores a pointer back to the actual data row — a table can have multiple non-clustered indexes. Clustered indexes are generally faster for range queries; non-clustered are useful for lookups on non-key columns.

## Question: What are window functions and when would you use them?
Window functions (like ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD()) perform calculations across a set of rows related to the current row without collapsing rows the way GROUP BY does. Useful for ranking within partitions, running totals, comparing a row to the previous/next row (LAG/LEAD), and computing moving averages.

## Question: Explain ACID properties in the context of transactions.
Atomicity ensures a transaction is all-or-nothing — if any part fails, the whole transaction rolls back. Consistency ensures a transaction brings the database from one valid state to another, respecting constraints. Isolation ensures concurrent transactions don't interfere with each other's intermediate states. Durability ensures once a transaction is committed, it survives system failures (persisted to disk/log).

## Question: Write a query to find employees who earn more than their manager.
```sql
SELECT e.name AS Employee
FROM Employee e
JOIN Employee m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```
This is a self-join, joining the Employee table to itself to compare each employee's salary against their manager's row.

## Question: What is the difference between UNION and UNION ALL?
UNION combines result sets from two queries and removes duplicate rows (requires an internal sort/dedup, so it's slower). UNION ALL combines result sets and keeps all rows including duplicates, making it faster since no deduplication step is needed. Both require the queries to have the same number of columns with compatible data types.
