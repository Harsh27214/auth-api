from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_port_string = os.getenv("POSTGRES_PORT")
database_port = int(database_port_string) if database_port_string else None

database_url = URL.create(
    drivername = "postgresql+psycopg",
    database = os.getenv("POSTGRES_DATABASE"),
    username = os.getenv("POSTGRES_USER"),
    password = os.getenv("POSTGRES_PASSWORD"),
    host = os.getenv("POSTGRES_HOST"),
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
