"""Enterprise Database Utility for MySQL and PostgreSQL.

Provides database connection pooling, parameterized query execution, dictionary mapping,
data integrity verification, and UI-to-DB record assertions.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.utils.logger import get_logger

logger = get_logger("DBUtility")


class DBUtility:
    """Database connection and query execution helper supporting MySQL and PostgreSQL."""

    def __init__(self, db_type: str = "mysql", host: str = "localhost", port: int = 3306,
                 database: str = "saucedemo_db", username: str = "root", password: str = "root") -> None:
        """Initialize Database Engine based on dialect and connection parameters."""
        self.db_type = db_type.lower()
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.engine: Optional[Engine] = None
        self._initialize_engine()

    def _initialize_engine(self) -> None:
        """Construct SQLAlchemy connection string and engine."""
        if self.db_type == "mysql":
            conn_str = f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            engine_kwargs = {"pool_pre_ping": True, "pool_size": 5, "max_overflow": 10}
        elif self.db_type in ("postgresql", "postgres"):
            conn_str = f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            engine_kwargs = {"pool_pre_ping": True, "pool_size": 5, "max_overflow": 10}
        elif self.db_type == "sqlite":
            conn_str = f"sqlite:///{self.database}"
            engine_kwargs = {}
        else:
            raise ValueError(f"Unsupported database type '{self.db_type}'. Supported: mysql, postgresql, sqlite")

        logger.info("Initializing SQLAlchemy DB Engine for '%s' database at %s", self.db_type, self.host)
        self.engine = create_engine(conn_str, **engine_kwargs)

    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT SQL query and return results as a list of dictionary rows."""
        if not self.engine:
            raise RuntimeError("Database Engine is not initialized.")

        logger.info("Executing DB Query: %s | Params: %s", query, params)
        with self.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            rows = result.mappings().all()
            return [dict(row) for row in rows]

    def execute_update(self, query: str, params: Optional[Dict[str, Any]] = None) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return affected row count."""
        if not self.engine:
            raise RuntimeError("Database Engine is not initialized.")

        logger.info("Executing DB Update Statement: %s | Params: %s", query, params)
        with self.engine.begin() as connection:
            result = connection.execute(text(query), params or {})
            return result.rowcount

    @staticmethod
    def verify_ui_against_db(ui_data: Dict[str, Any], db_data: Dict[str, Any], keys_to_compare: List[str]) -> bool:
        """Verify that specific keys in UI data strictly match records returned from Database query."""
        mismatches = []
        for key in keys_to_compare:
            ui_val = str(ui_data.get(key, "")).strip()
            db_val = str(db_data.get(key, "")).strip()
            if ui_val != db_val:
                mismatches.append(f"Key '{key}' Mismatch -> UI: '{ui_val}' vs DB: '{db_val}'")

        if mismatches:
            err_msg = "UI vs DB Data Verification Failed!\n" + "\n".join(mismatches)
            logger.error(err_msg)
            raise AssertionError(err_msg)

        logger.info("UI vs DB Verification PASSED for keys: %s", keys_to_compare)
        return True
