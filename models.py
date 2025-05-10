from database import Base
from sqlalchemy import Column, String, LargeBinary

class User(Base):
    __tablename__ = "users"

    username = Column(String(255), primary_key=True)
    hashed_password = Column(LargeBinary, nullable=False)
