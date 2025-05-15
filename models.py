from database import Base
from sqlalchemy import Column, String, LargeBinary

class User(Base):
    __tablename__ = "users"

    lowercase_username = Column(String, primary_key=True)
    display_username = Column(String, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
