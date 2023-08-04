from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Security Issue 1: Insecure Direct Object References (IDOR)
# Any user can access any note by changing the 'id' parameter value.
@app.route('/note/<id>', methods=['GET'])
def get_note(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Security Issue 2: SQL Injection Vulnerability
    # The 'id' parameter is directly added to the SQL query without proper validation or escaping.
    query = f"SELECT content FROM notes WHERE id = {id}"
    cursor.execute(query)
    note = cursor.fetchone()
    conn.close()
    return note[0] if note else 'Note not found'

# Security Issue 3: Unsecured Password Storage
# Passwords are stored as plaintext in the database.
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return 'User registered successfully'

if __name__ == '__main__':
    app.run(debug=True)  # Security Issue 4: Debug Mode Enabled in Production
