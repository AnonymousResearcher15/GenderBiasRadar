import sqlite3
from contextlib import contextmanager
from typing import Iterator, Optional


class SqlLiteConnection:
	def __init__(self, db_path: str, timeout: float = 5.0) -> None:
		self.db_path = db_path
		self.timeout = timeout

	def _get_connection(self) -> sqlite3.Connection:
		"""Create and configure a SQLite connection."""
		connection = sqlite3.connect(self.db_path, timeout=self.timeout)
		connection.row_factory = sqlite3.Row
		connection.execute("PRAGMA foreign_keys = ON;")
		return connection

	@contextmanager
	def connection(self) -> Iterator[sqlite3.Connection]:
		"""Context-managed SQLite connection."""
		conn: Optional[sqlite3.Connection] = None
		try:
			conn = self._get_connection()
			yield conn
			conn.commit()
		except Exception:
			if conn is not None:
				conn.rollback()
			raise
		finally:
			if conn is not None:
				conn.close()

	def get_gender_list(self, term: str) -> list[dict]:
		"""Return all distinct word rows matching the given form (case-insensitive first letter)."""
		if len(term) == 0:
			return []
		
		# Use _ as wildcard for first character to handle case variations
		pattern = f"_{term[1:].lower()}" if len(term) > 1 else "_"
		query = "SELECT DISTINCT * FROM words WHERE LOWER(form) LIKE ?"
		with self.connection() as conn:
			rows = conn.execute(query, (pattern,)).fetchall()
		return [dict(row) for row in rows]
	
	def run_query(self, query: str, params: tuple = ()) -> list[dict]:
		"""Run a custom query and return results as a list of dictionaries."""
		with self.connection() as conn:
			rows = conn.execute(query, params).fetchall()
		return [dict(row) for row in rows]