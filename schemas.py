from pydantic import BaseModel, field_validator
import re

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def valid_username(cls, username):
        if not 2 < len(username) < 21:
            raise ValueError('Username must be 3 to 20 characters long')
        return username

    @field_validator('password')
    def strong_password(cls, password):
        error_message = "Password must contain more than seven characters with at least one lowercase letter, uppercase letter, digit, and special symbol"

        if len(password) < 8:
            raise ValueError(error_message)
        if not re.search(r'[A-Z]', password):
            raise ValueError(error_message)
        if not re.search(r'[a-z]', password):
            raise ValueError(error_message)
        if not re.search(r'\d', password):
            raise ValueError(error_message)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError(error_message)
        return password
