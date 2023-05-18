from flask_socketio import emit, join_room, leave_room
from app import socketio
import sys
from flask import session

@socketio.on('connect', namespace='/chat')
def handle_connect():
    room=session.get("chat")
    join_room(room)
    print('Client connected!', file=sys.stderr)
    # emit('status', 'msg here')



@socketio.on("user_join", namespace='/chat')
def handle_user_join(username):
    print(f'User {username} joined!', file=sys.stderr)

@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    room=session.get("chat")
    print(f"New message: {message}", file=sys.stderr)
    emit("chat", {"message":message}, broadcast=True, room=room)
