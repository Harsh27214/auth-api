from fastapi import FastAPI, HTTPException, Depends
from services import hash_password, valid_username, strong_password
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from database import get_db

app = FastAPI()

@app.post("/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if not valid_username(user.username):
        raise HTTPException(status_code=400, detail="Username must be 3 to 20 characters long")

    if not strong_password(user.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase, lowercase, digit, and special character and be at least 8 characters long")

    lowercase_username = user.username.lower()
    existing = db.query(User).filter_by(username=lowercase_username).first()

    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    new_user = User(username=lowercase_username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()

    return {"message": "User created", "username": user.username}
