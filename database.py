from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_url = URL.create(
    port = 5432,
    drivername = "postgresql+psycopg",
    database = os.getenv("POSTGRES_DATABASE"),
    username = os.getenv("POSTGRES_USER"),
    password = os.getenv("POSTGRES_PASSWORD"),
    host = os.getenv("POSTGRES_HOST")
)

engine = create_engine(database_url)
Base = declarative_base()
SessionFactory = sessionmaker(engine)

def create_session():
    session = SessionFactory()
    try:
        yield session

    finally:
        session.close()
