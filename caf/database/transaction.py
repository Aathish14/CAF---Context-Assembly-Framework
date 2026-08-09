"""Transaction context manager for CAF database operations."""

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Literal

from caf.database.db import get_db


class _ConnectionWrapper:
    """Wrapper around sqlite3.Connection that suppresses commit/rollback."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def __getattr__(self, name: str) -> Any:
        """Delegate all attribute access to the wrapped connection."""
        return getattr(self._connection, name)

    def commit(self) -> None:
        """Suppress commit - will be handled by Transaction."""
        pass

    def rollback(self) -> None:
        """Suppress rollback - will be handled by Transaction."""
        pass


class Transaction:
    """Context manager for database transactions.

    Ensures atomic operations by wrapping multiple repository writes
    in a single database transaction. Automatically rolls back on
    any exception and commits on successful completion.

    Example:
        with Transaction():
            instruction_repo.save(instruction)
            version_repo.save(version)
            variant_repo.save(variant)
    """

    def __init__(self) -> None:
        """Initialize the transaction context manager."""
        self._original_connection: sqlite3.Connection | None = None
        self._wrapper: _ConnectionWrapper | None = None

    def __enter__(self) -> _ConnectionWrapper:
        """Begin a new transaction.

        Returns:
            Connection wrapper that suppresses commit/rollback.
        """
        # Get the shared database connection
        self._original_connection = get_db().connect()
        # Disable autocommit to manage transaction manually
        self._original_connection.isolation_level = None
        # Create wrapper that suppresses commit/rollback
        self._wrapper = _ConnectionWrapper(self._original_connection)
        # Begin transaction on the real connection
        self._original_connection.execute("BEGIN")
        # Replace the database's internal connection with our wrapper
        db = get_db()
        db._connection = self._wrapper  # type: ignore[assignment]
        return self._wrapper

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: Any,
    ) -> Literal[False]:
        """Commit or rollback transaction based on exception state.

        Args:
            exc_type: Exception type if an exception occurred.
            _exc_val: Exception value if an exception occurred (unused).
            _exc_tb: Exception traceback if an exception occurred (unused).

        Returns:
            False to propagate exceptions, True to suppress.
        """
        if self._original_connection is None:
            return False

        try:
            if exc_type is None:
                # No exception - commit the transaction
                self._original_connection.commit()
            else:
                # Exception occurred - rollback
                self._original_connection.rollback()
        finally:
            # Restore the original connection in the database
            db = get_db()
            db._connection = self._original_connection
            # Restore isolation level
            if self._original_connection is not None:
                self._original_connection.isolation_level = None
        # Return False to propagate any exception
        return False


# Convenience function for simpler usage
@contextmanager
def transaction() -> Generator[None, None, None]:
    """Context manager for database transactions.

    Example:
        with transaction():
            instruction_repo.save(instruction)
            version_repo.save(version)
    """
    with Transaction():
        yield
