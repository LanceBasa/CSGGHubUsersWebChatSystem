from flask_socketio import join_room, leave_room, emit
from . import socketio, db
from .models import Chat
from flask_login import current_user
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from . import socketio



# ... Rest of your Socket.IO code ...

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    join_room(message['room'])

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user issued a new message.
    The message is sent to all people in the room."""
    
    # Create a new Chat object with the user's message
    new_message = Chat(user_id=current_user.id, room_id=message['room'], text=message['msg'], created_at=datetime.utcnow())
    
    # Add the new message to the database
    db.session.add(new_message)
    
    # Commit the changes to the database
    db.session.commit()

    # Emit the message to all clients in the room
    socketio.emit('message', {
        'msg': message['msg'],
        'room': message['room'],
        'user': current_user.username
    }, room=message['room'])

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    leave_room(message['room'])