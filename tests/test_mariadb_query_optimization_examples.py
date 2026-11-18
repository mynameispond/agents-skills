"""Check result semantics for portable examples from the MariaDB skill."""

from pathlib import Path
import re
import sqlite3
import unittest


skill_path = (
    Path(__file__).resolve().parents[1]
    / ".agents"
    / "skills"
    / "mariadb-query-optimization"
    / "SKILL.md"
)


def sql_blocks(heading):
    content = skill_path.read_text(encoding="utf-8")
    section = content.split(f"\n{heading}\n", 1)[1]
    section = re.split(r"^#+ ", section, maxsplit=1, flags=re.MULTILINE)[0]
    return re.findall(r"```sql\n(.*?)```", section, re.DOTALL)


class MariaDBQueryOptimizationExampleTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)

    def test_date_range_includes_start_and_excludes_next_year(self):
        self.connection.executescript(
            """
            CREATE TABLE orders (id INTEGER PRIMARY KEY, created_at TEXT);
            INSERT INTO orders VALUES
                (1, '2024-12-31 23:59:59.999999'),
                (2, '2025-01-01'),
                (3, '2025-12-31 23:59:59.999999'),
                (4, '2026-01-01'),
                (5, NULL);
            """
        )
        date_range, = sql_blocks("### Functions on Indexed Columns")
        rows = self.connection.execute(
            f"SELECT id FROM orders {date_range.strip()} ORDER BY id"
        ).fetchall()
        self.assertEqual(rows, [(2,), (3,)])

    def test_cursor_pages_keep_each_row_once_in_descending_order(self):
        self.connection.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT)")
        posts = [(2 * number, f"Post {number}") for number in range(1, 24)]
        self.connection.executemany("INSERT INTO posts VALUES (?, ?)", posts)

        pagination, _ = sql_blocks("## Pagination: Cursor-Based Instead of OFFSET")
        _, first_page, next_page = re.findall(r"^SELECT\b[^;]*;", pagination, re.MULTILINE)

        first = self.connection.execute(first_page).fetchall()
        second = self.connection.execute(next_page, {"last_id": first[-1][0]}).fetchall()
        third = self.connection.execute(next_page, {"last_id": second[-1][0]}).fetchall()

        self.assertEqual([len(first), len(second), len(third)], [10, 10, 3])
        self.assertEqual(first + second + third, posts[::-1])


if __name__ == "__main__":
    unittest.main()
