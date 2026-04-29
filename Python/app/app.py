from flask import Flask, render_template, request, redirect, url_for, jsonify
import socket
from datetime import datetime
import mysql.connector
import os

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'my-mysql'),
        user=os.getenv('MYSQL_USER', 'user'),
        password=os.getenv('MYSQL_PASSWORD', 'password'),
        database=os.getenv('MYSQL_DATABASE', 'guestbook')
    )

def init_db():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        cursor.close()
        db.close()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database init error: {e}")

init_db()

visit_counter = 0

@app.route('/')
def index():
    global visit_counter
    visit_counter += 1
    return render_template('index.html', visits=visit_counter)

@app.route('/about')
def about():
    return render_template('about.html', container_name=socket.gethostname())

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        name = request.form.get('name', 'Аноним')
        message = request.form.get('message', '')
        
        if message:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO messages (name, message) VALUES (%s, %s)",
                    (name, message)
                )
                db.commit()
                cursor.close()
                db.close()
                print(f"✅ Message saved")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return redirect(url_for('guestbook'))
    
    messages = []
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, message, created_at FROM messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"❌ Error loading: {e}")
    
    return render_template('guestbook.html', messages=messages)

@app.route('/api/status')
def api_status():
    return jsonify({'status': 'ok', 'container': socket.gethostname()})

@app.route('/api/messages')
def api_messages():
    messages = []
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT name, message, created_at FROM messages ORDER BY created_at DESC")
        messages = cursor.fetchall()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"❌ Error: {e}")
    return jsonify({'messages': messages})

@app.route('/api/ping')
def api_ping():
    return jsonify({'status': 'pong'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)