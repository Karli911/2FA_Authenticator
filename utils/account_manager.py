from .database_manager import execute_query, fetch_all, fetch_one

def add_account(db_path, key, user_email, secret_key, backup_codes):
    query = "INSERT INTO accounts (user_email, secret_key, backup_codes) VALUES (?, ?, ?)"
    params = (user_email, secret_key, ','.join(backup_codes))
    execute_query(db_path, key, query, params)

def get_account(db_path, key, user_email):
    query = "SELECT secret_key, backup_codes FROM accounts WHERE user_email = ?"
    params = (user_email,)
    row = fetch_one(db_path, key, query, params)
    if row:
        secret_key, backup_codes = row
        return secret_key, backup_codes.split(',')
    return None, None

def get_all_accounts(db_path, key):
    query = "SELECT user_email FROM accounts"
    rows = fetch_all(db_path, key, query)
    return [row[0] for row in rows]

def update_backup_codes(db_path, key, user_email, backup_codes):
    query = "UPDATE accounts SET backup_codes = ? WHERE user_email = ?"
    params = (','.join(backup_codes), user_email)
    execute_query(db_path, key, query, params)

def delete_account(db_path, key, user_email):
    query = "DELETE FROM accounts WHERE user_email = ?"
    params = (user_email,)
    execute_query(db_path, key, query, params)