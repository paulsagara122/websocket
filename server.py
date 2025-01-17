from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

log_directory = 'logs'
log_file_prefix = 'log_'
max_lines_per_log = 10

def get_latest_log_file():
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_files = sorted([f for f in os.listdir(log_directory) if f.startswith(log_file_prefix)])
    if log_files:
        return os.path.join(log_directory, log_files[-1])
    return os.path.join(log_directory, f"{log_file_prefix}1.txt")

def append_to_log(message):
    log_file = get_latest_log_file()
    with open(log_file, 'a') as f:
        f.write(f"{message}\n")
    with open(log_file, 'r') as f:
        lines = f.readlines()
    if len(lines) > max_lines_per_log:
        new_log_file = os.path.join(log_directory, f"{log_file_prefix}{int(log_file.split('_')[-1].split('.')[0]) + 1}.txt")
        with open(new_log_file, 'w') as f:
            f.writelines(lines[max_lines_per_log:])
        with open(log_file, 'w') as f:
            f.writelines(lines[:max_lines_per_log])

def get_latest_messages():
    log_file = get_latest_log_file()
    with open(log_file, 'r') as f:
        lines = f.readlines()
    return lines[-5:]

@app.route('/')
def home():
    messages = get_latest_messages()
    return render_template('messages.html', messages=messages)

@socketio.on('message')
def handle_message(msg):
    print(f"Received: {msg}")
    append_to_log(msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    socketio.run(app, debug=True)
