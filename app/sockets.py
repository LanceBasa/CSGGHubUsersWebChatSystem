from flask_socketio import emit
from app import socketio

@socketio.on('connect')
def handle_connect():
    print('Client connected!')


@socketio.on("user_join")
def handle_user_join(username):
    print(f'User {username} joined!')

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    emit("chat", {"message":message}, broadcast=True)
