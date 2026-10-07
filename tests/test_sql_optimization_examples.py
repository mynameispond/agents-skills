"""Execute portable SQL examples against in-memory semantic fixtures.

SQLite checks result preservation, not target-engine syntax or performance.
"""

from collections import Counter
from pathlib import Path
import re
import sqlite3
import unittest


skill_path = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "sql-optimization"
    / "SKILL.md"
)


def section_queries(heading):
    content = skill_path.read_text(encoding="utf-8")
    section = content.split(f"### {heading}\n", 1)[1]
    section = re.split(r"^#{1,3} ", section, maxsplit=1, flags=re.MULTILINE)[0]
    queries = []
    for block in re.findall(r"```sql\n(.*?)```", section, re.DOTALL):
        statement = ""
        for line in block.splitlines():
            if line.lstrip().startswith("--"):
                continue
            statement += line + "\n"
            if sqlite3.complete_statement(statement):
                queries.append(statement.strip())
                statement = ""
        if statement.strip():
            raise ValueError(f"Unterminated SQL in {heading}")
    return queries


def projected_rows(connection, query, columns):
    cursor = connection.execute(query)
    positions = {field[0]: index for index, field in enumerate(cursor.description)}
    return [tuple(row[positions[column]] for column in columns) for row in cursor]


class SqlOptimizationExampleTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)

    def test_date_range_preserves_year_boundaries_and_membership(self):
        self.connection.create_function("YEAR", 1, lambda value: int(value[:4]) if value else None)
        self.connection.executescript(
            """
            CREATE TABLE customers (id INTEGER PRIMARY KEY, status TEXT);
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY, customer_id INTEGER,
                total_amount INTEGER, created_at TEXT
            );
            INSERT INTO customers VALUES (1, 'active'), (2, 'inactive');
            INSERT INTO orders VALUES
                (1, 1, 10, '2023-12-31 23:59:59'),
                (2, 1, 20, '2024-01-01 00:00:00'),
                (3, 1, 30, '2024-12-31 23:59:59.999'),
                (4, 1, 40, '2025-01-01 00:00:00'),
                (5, 2, 50, '2024-06-01'), (6, 999, 60, '2024-06-01'),
                (7, 1, 70, NULL), (8, NULL, 80, '2024-06-01');
            """
        )
        baseline, candidate = section_queries("Query Performance Analysis")
        expected = self.connection.execute(baseline).fetchall()
        self.assertEqual({row[0] for row in expected}, {2, 3})
        self.assertEqual(Counter(self.connection.execute(candidate).fetchall()), Counter(expected))

    def test_join_preserves_unmatched_children_and_duplicate_rows(self):
        self.connection.executescript(
            """
            CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, status TEXT);
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY, customer_id INTEGER,
                total_amount INTEGER, created_at TEXT
            );
            CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER);
            CREATE TABLE products (id INTEGER PRIMARY KEY, product_name TEXT);
            INSERT INTO customers VALUES (1, 'Active', 'active'), (2, 'Inactive', 'inactive');
            INSERT INTO orders VALUES
                (1, 1, 10, '2024-02-01'), (2, 1, 20, '2024-02-01'),
                (3, 1, 30, '2024-02-01'), (4, 2, 40, '2024-02-01'),
                (5, 1, 50, '2023-12-01');
            INSERT INTO products VALUES (1, 'Widget');
            INSERT INTO order_items VALUES (1, 2, 999), (2, 3, 1), (3, 3, 1);
            """
        )
        baseline, candidate = section_queries("JOIN Optimization")
        columns = ("id", "total_amount", "name", "product_name")
        expected = Counter(projected_rows(self.connection, baseline, columns))
        self.assertEqual(
            expected,
            Counter([(1, 10, "Active", None), (2, 20, "Active", None),
                     (3, 30, "Active", "Widget"), (3, 30, "Active", "Widget")]),
        )
        self.assertEqual(Counter(projected_rows(self.connection, candidate, columns)), expected)

    def test_case_insensitive_lookup_preserves_mixed_case_matches(self):
        self.connection.executescript(
            """
            CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_email TEXT COLLATE BINARY);
            INSERT INTO orders VALUES
                (1, 'john@example.com'), (2, 'JOHN@EXAMPLE.COM'),
                (3, 'John@Example.Com'), (4, 'other@example.com'), (5, NULL);
            """
        )
        queries = section_queries("WHERE Clause Optimization")
        baseline = self.connection.execute(queries[0]).fetchall()
        candidate = self.connection.execute(queries[1]).fetchall()
        self.assertEqual({row[0] for row in baseline}, {1, 2, 3})
        self.assertEqual(Counter(candidate), Counter(baseline))

    def test_timestamp_cursor_keeps_rows_with_tied_timestamps(self):
        self.connection.executescript(
            """
            CREATE TABLE products (id INTEGER PRIMARY KEY, created_at TEXT NOT NULL);
            INSERT INTO products VALUES
                (1004, '2024-06-15 10:30:00'), (1003, '2024-06-15 10:30:00'),
                (1002, '2024-06-15 10:30:00'), (1001, '2024-06-15 10:30:00'),
                (999, '2024-06-14 10:30:00'), (998, '2024-06-13 10:30:00');
            """
        )
        timestamp_cursor = section_queries("Pagination Optimization")[1]
        rows = self.connection.execute(timestamp_cursor).fetchall()
        self.assertEqual([row[0] for row in rows], [1002, 1001, 999, 998])

    def test_window_rewrite_preserves_null_category_semantics(self):
        self.connection.executescript(
            """
            CREATE TABLE products (product_name TEXT, price INTEGER, category_id INTEGER);
            INSERT INTO products VALUES
                ('Cheap', 10, 1), ('Premium', 30, 1),
                ('Null low', 10, NULL), ('Null high', 40, NULL),
                ('Missing price', NULL, 1);
            """
        )
        baseline, candidate = section_queries("Subquery Optimization")
        expected = self.connection.execute(baseline).fetchall()
        self.assertEqual(expected, [("Premium", 30)])
        self.assertEqual(Counter(self.connection.execute(candidate).fetchall()), Counter(expected))

    def test_disjoint_union_preserves_rows_and_multiplicity(self):
        self.connection.executescript(
            """
            CREATE TABLE products (category TEXT, price INTEGER);
            INSERT INTO products VALUES
                ('electronics', 999), ('electronics', 999), ('electronics', 1000),
                ('books', 49), ('books', 50), ('other', 10), (NULL, 10), ('books', NULL);
            """
        )
        baseline, candidate = section_queries("OR vs UNION Optimization")
        expected = self.connection.execute(baseline).fetchall()
        self.assertEqual(expected.count(("electronics", 999)), 2)
        self.assertEqual(Counter(self.connection.execute(candidate).fetchall()), Counter(expected))

    def test_conditional_aggregation_handles_empty_and_populated_tables(self):
        # Compare numeric counts on a stable fixture. Caller mapping and target-engine
        # snapshot/isolation behavior need separate checks before a real rewrite.
        self.connection.execute("CREATE TABLE orders (status TEXT)")
        queries = section_queries("Aggregation Optimization")
        for states in ([], ["pending", "pending", "shipped", "delivered", None, "other"]):
            with self.subTest(states=states):
                self.connection.execute("DELETE FROM orders")
                self.connection.executemany("INSERT INTO orders VALUES (?)", [(state,) for state in states])
                expected = tuple(self.connection.execute(query).fetchone()[0] for query in queries[:3])
                self.assertEqual(self.connection.execute(queries[3]).fetchone(), expected)


if __name__ == "__main__":
    unittest.main()
