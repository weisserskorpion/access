from flask import Flask, request, session, render_template_string
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect("data.db")
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Create tables if they don't exist
query_db("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)""")

query_db("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT NOT NULL
)""")

@app.route('/')
def home():
    return render_template_string(open('templates/home.html').read())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Security Issue: Passwords are compared in plaintext and sent over unsecured connection
        user = query_db("SELECT * FROM users WHERE username = ? AND password = ?", [request.form['username'], request.form['password']], one=True)
        if user:
            session['user_id'] = user[0]
            return 'Logged in successfully'
        else:
            return 'Invalid credentials'
    return render_template_string(open('templates/login.html').read())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Security Issue: Passwords are stored in plaintext in the database
        query_db("INSERT INTO users (username, password) VALUES (?, ?)", [request.form['username'], request.form['password']])
        return 'User registered successfully'
    return render_template_string(open('templates/register.html').read())

@app.route('/note', methods=['POST'])
def add_note():
    if 'user_id' in session:
        query_db("INSERT INTO notes (user_id, content) VALUES (?, ?)", [session['user_id'], request.form['content']])
        return 'Note added successfully'
    return 'Login required'

@app.route('/mynotes', methods=['GET'])
def view_notes():
    if 'user_id' in session:
        # Security Issue: Insecure Direct Object References (IDOR)
        notes = query_db("SELECT content FROM notes WHERE user_id = ?", [session['user_id']])
        return '<br>'.join(note[0] for note in notes)
    return 'Login required'

if __name__ == '__main__':
    app.run(debug=True)  # Security Issue: Debug Mode Enabled in Production
