from flask import Flask, render_template, request, redirect, url_for, jsonify
import socket
from datetime import datetime
import mysql.connector
import os

app = Flask(__name__)

# Хранилище для сообщений (в реальном проекте использовали бы базу данных)
messages = []
visit_counter = 0

@app.route('/')
def index():
    global visit_counter
    visit_counter += 1
    return render_template('index.html', visits=visit_counter)

@app.route('/about')
def about():
    container_name = socket.gethostname()
    return render_template('about.html', container_name=container_name)

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        name = request.form.get('name', 'Аноним')
        message = request.form.get('message', '')
        
        if message:
            messages.append({
                'name': name,
                'message': message,
                'date': datetime.now().strftime('%d.%m.%Y %H:%M')
            })
        return redirect(url_for('guestbook'))
    
    return render_template('guestbook.html', messages=messages)

# API эндпоинты
@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'ok',
        'container': socket.gethostname(),
        'messages_count': len(messages),
        'visits': visit_counter
    })

@app.route('/api/messages')
def api_messages():
    return jsonify({'messages': messages})

@app.route('/api/ping')
def api_ping():
    return jsonify({'status': 'pong'})

@app.route('/api/hello')
def api_hello():
    return jsonify({
        'message': 'Hello from Python container!',
        'container': socket.gethostname()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)