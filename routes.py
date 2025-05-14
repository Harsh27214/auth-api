from fastapi import HTTPException, Depends
from services import hash_password, valid_username, strong_password
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from database import create_session
from main import app

@app.post("/users", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(create_session)):
    if not valid_username(user.username):
        raise HTTPException(status_code=400, detail="Username must be 3 to 20 characters long")

    if not strong_password(user.password):
        raise HTTPException(status_code=400, detail="Password must contain more than seven characters with at least one lowercase letter, uppercase letter, digit, and special symbol")

    existing = session.query(User).filter_by(lowercase_username=user.username.lower()).first()

    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    new_user = User(lowercase_username=user.username.lower(), display_username=user.username, hashed_password=hash_password(user.password))
    session.add(new_user)
    session.commit()

    return {"message": "User created", "username": user.username}
