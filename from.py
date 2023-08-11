from flask import Flask, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# TODO: Implement authentication and session management for better security

@app.route('/note/<id>', methods=['GET'])
def get_note(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Use a parameterized query to prevent SQL injections
    cursor.execute("SELECT content FROM notes WHERE id = ?", (id,))
    note = cursor.fetchone()
    conn.close()
    return note[0] if note else 'Note not found'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    
    # Hash the password before storing
    hashed_password = generate_password_hash(request.form['password'], method='sha256')
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()
    return 'User registered successfully'

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode for production
