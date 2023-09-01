import sqlite3

def get_user(username):
    # Potential SQL Injection
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()

SECRET_KEY = "my_super_secret_key"  # Hardcoded secrets that Gitleaks will catch
