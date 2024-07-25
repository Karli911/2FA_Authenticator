import bcrypt
from .database_manager import execute_query, fetch_one

def create_user(db_path, key, username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    query = "INSERT INTO users (username, password) VALUES (?, ?)"
    params = (username, hashed_password)
    execute_query(db_path, key, query, params)

def verify_user(db_path, key, username, password):
    query = "SELECT password FROM users WHERE username = ?"
    params = (username,)
    row = fetch_one(db_path, key, query, params)
    if row:
        stored_hashed_password = row[0]
        return bcrypt.checkpw(password.encode(), stored_hashed_password.encode())
    return False