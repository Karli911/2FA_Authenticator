import os
import pysqlcipher3.dbapi2 as sqlite3

def initialize_database(db_path, key):
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA key = ?", (key,))
        cursor.execute("CREATE TABLE accounts (user_email TEXT PRIMARY KEY, secret_key TEXT, backup_codes TEXT)")
        cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)")
        conn.commit()
        conn.close()

def execute_query(db_path, key, query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key = ?", (key,))
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(db_path, key, query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key = ?", (key,))
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_one(db_path, key, query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA key = ?", (key,))
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return row