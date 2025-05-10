import re
import bcrypt

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password

def valid_username(username):
    return 2 < len(username) < 21

def strong_password(password):
        if len(password) < 8:
            return False
        if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True
