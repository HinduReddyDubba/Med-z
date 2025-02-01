from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Function to initialize the SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Medications Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            frequency TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Reminders Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT NOT NULL,
            time TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# **User Registration**
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({'status': 'Registration successful!'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'status': 'Username already exists!'}), 400

# **User Login**
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['user_id'] = user[0]
        return jsonify({'status': 'Login successful!'})
    else:
        return jsonify({'status': 'Invalid credentials!'}), 401

# **Add Medication**
@app.route('/add_medication', methods=['POST'])
def add_medication():
    if 'user_id' not in session:
        return jsonify({'status': 'Unauthorized'}), 401

    data = request.get_json()
    name = data.get('name')
    dosage = data.get('dosage')
    frequency = data.get('frequency')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO medications (user_id, name, dosage, frequency) VALUES (?, ?, ?, ?)",
              (session['user_id'], name, dosage, frequency))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Medication added successfully!'})

# **Fetch Medications**
@app.route('/get_medications', methods=['GET'])
def get_medications():
    if 'user_id' not in session:
        return jsonify({'status': 'Unauthorized'}), 401

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT name, dosage, frequency FROM medications WHERE user_id = ?", (session['user_id'],))
    medications = c.fetchall()
    conn.close()

    return jsonify(medications)

# **Add Reminder**
@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    if 'user_id' not in session:
        return jsonify({'status': 'Unauthorized'}), 401

    data = request.get_json()
    message = data.get('message')
    time = data.get('time')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (user_id, message, time) VALUES (?, ?, ?)",
              (session['user_id'], message, time))
    conn.commit()
    conn.close()

    return jsonify({'status': 'Reminder added successfully!'})

# **Fetch Reminders**
@app.route('/get_reminders', methods=['GET'])
def get_reminders():
    if 'user_id' not in session:
        return jsonify({'status': 'Unauthorized'}), 401

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT message, time FROM reminders WHERE user_id = ?", (session['user_id'],))
    reminders = c.fetchall()
    conn.close()

    return jsonify(reminders)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)