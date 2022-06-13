import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def sqlalchemy_engine():
    """Create sqlalchemy engine."""
    return create_engine(get_database_uri())

def sqlalchemy_session():
    """Create sqlalchemy session."""
    session = Session(sqlalchemy_engine(), future=True)
    return session

def get_database_uri():
    """Return database config parameters."""
    return (
        "postgresql://"
        + os.environ.get("POSTGRES_USER", "postgres")
        + ":"
        + os.environ.get("POSTGRES_PASSWORD", "root")
        + "@"
        + os.environ.get("POSTGRES_HOST", "localhost")
        + ":5432/"
        + os.environ.get("POSTGRES_DB", "postgres")
    )
