from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_port_string = os.getenv("PGPORT")
database_port = int(database_port_string) if database_port_string else None

database_url = URL.create(
    drivername = "postgresql+psycopg",
    database = os.getenv("PGDATABASE"),
    username = os.getenv("PGUSER"),
    password = os.getenv("PGPASSWORD"),
    host = os.getenv("PGHOST"),
    port = database_port
)

Base = declarative_base()
engine = create_engine(database_url)
SessionFactory = sessionmaker(bind=engine)

def create_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
