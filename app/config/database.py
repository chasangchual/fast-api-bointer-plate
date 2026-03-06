import os
from urllib.parse import quote_plus
from typing import Any, Generator, Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import ArgumentError, NoSuchModuleError, OperationalError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Database DSN used by SQLAlchemy to connect to the local Postgres instance.
database_url = os.getenv("DATABASE_URL")
if database_url:
    SQLALCHEMY_DATABASE_URL = database_url
else:
    db_user = os.getenv("DB_USER", "USER")
    db_password = quote_plus(os.getenv("DB_DB_USER_PASSWORD", "PASSWORD"))
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "DB")
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )


# Shared engine and session factory for request-scoped DB sessions.
try:
    # Validates URL format/dialect at startup; DB connectivity is checked on first use.
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
except (ArgumentError, NoSuchModuleError) as exc:
    raise RuntimeError(
        f'Invalid SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL!r}',
    ) from exc

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models; `metadata` is reused for table creation/migrations.
Base = declarative_base()
metadata = Base.metadata

def get_session() -> Generator[Session, Any, None]:
    # Yield one session per request and always close it after use.
    session = sessionLocal()
    try:
        yield session
    except OperationalError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Database is not ready. Please try again shortly.',
        ) from exc
    finally:
        session.close()

# Type alias for FastAPI dependency injection in route handlers.
db_session = Annotated[Session, Depends(get_session)]
