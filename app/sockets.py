from flask import session, request
from app import db, socketio
from app.models import Chat, User
from flask_socketio import emit, join_room, leave_room
import sys
from sqlalchemy import desc
from flask_login import current_user



@socketio.on("user_join", namespace='/chat')
def handle_user_join(username):
    print(f'User {username} joined!', file=sys.stderr)

@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    # Assuming that you're using flask_login, you can access the currently authenticated user with current_user
    if current_user.is_authenticated:
        room = session.get("chat")
        # Create a new Chat object and store it in the database
        chat_message = Chat(text=message, user_id=current_user.id)
        #if len(chat_message==1):
            #if chat_message[1] == '~':
                #print(the commands)
            #if second field == player name:
                #query.special.table.messages which have sql query using the name of player
        db.session.add(chat_message)
        db.session.commit()
        print(f"New message: {message}", file=sys.stderr)
        emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
    else:
        print("Error: Unauthenticated user tried to send a message", file=sys.stderr)



@socketio.on('connect', namespace='/chat')
def handle_connect():
    # Retrieve the current room from the session
    room = session.get("chat")
    # Join the room
    join_room(room)
    print('Client connected!', file=sys.stderr)

    # Retrieve the last 20 chat messages from the database
    messages = Chat.query.order_by(desc(Chat.created_at)).limit(20).all()

    # Convert the messages to a format that can be sent over the socket
    messages = [{'text': msg.text, 'username': msg.author.username} for msg in reversed(messages)]

    # Send the messages to the client
    emit('load_messages', messages)

    # This assumes that you want to send a status message every time a client connects
    emit('status', {'msg': 'New client connected!'}, room=room)