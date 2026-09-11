"""
Database connection layer.

Supports both PostgreSQL (production) and SQLite (development/testing).
The DATABASE_URL environment variable controls which engine is used:
  - postgres://... or postgresql://...  → PostgreSQL
  - sqlite:///path/to/file.db           → SQLite
  - (unset)                             → SQLite in-memory (for tests)
"""

import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from dotenv import load_dotenv

# Load .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aqi_tracker.db")

# SQLite needs check_same_thread=False for FastAPI's async usage
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    """Synchronous DB session context manager (used by ingestion/analytics)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables from schema.sql if they don't exist."""
    schema_path = os.path.join(os.path.dirname(__file__), "data", "schema.sql")
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    with engine.connect() as conn:
        # SQLite can only execute one statement at a time, so split
        # the schema into individual statements.
        statements = [s.strip() for s in schema_sql.split(";") if s.strip()]
        for stmt in statements:
            conn.execute(text(stmt))
        conn.commit()

    # Create TimescaleDB hypertable if using PostgreSQL with timescaledb
    if not DATABASE_URL.startswith("sqlite"):
        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT 1 FROM pg_extension WHERE extname = 'timescaledb'"
                ))
                if result.fetchone():
                    conn.execute(text(
                        "SELECT create_hypertable('daily_readings', 'date', if_not_exists => TRUE)"
                    ))
                    conn.commit()
                    print("Created TimescaleDB hypertable on daily_readings.")
        except Exception as e:
            print(f"Hypertable creation skipped: {e}")

    # Seed districts if the table is empty
    inspector = inspect(engine)
    if "districts" in inspector.get_table_names():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM districts"))
            count = result.scalar()
            if count == 0:
                seed_path = os.path.join(os.path.dirname(__file__), "data", "seed_districts.sql")
                with open(seed_path, "r") as f:
                    seed_sql = f.read()
                # Split seed SQL into individual statements for SQLite
                seed_statements = [s.strip() for s in seed_sql.split(";") if s.strip()]
                for stmt in seed_statements:
                    conn.execute(text(stmt))
                conn.commit()
                print(f"Seeded districts from seed_districts.sql")
            else:
                print(f"Districts table already has {count} rows, skipping seed.")
    else:
        print("Districts table not found — schema may not have been created.")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
