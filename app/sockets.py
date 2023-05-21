from flask import session, request
from app import db, socketio
from app.models import Chat, User
from flask_socketio import emit, join_room, leave_room
import sys
from sqlalchemy import desc
from flask_login import current_user

def chat_to_dict(chat):
    return {
        "id": chat.id,
        "text": chat.text,
        "username": chat.user.username,  # Assuming the user is linked with a relationship
        "created_at": chat.created_at.isoformat(),  # Convert datetime to string
        # Add other fields as needed...
    }

@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    if current_user.is_authenticated:
        room = session.get("chat")
        chat_message = Chat(text=message, user_id=current_user.id)
        db.session.add(chat_message)
        db.session.commit()
        print(f"New message: {message}", file=sys.stderr)
        emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
    else:
        print("Error: Unauthenticated user tried to send a message", file=sys.stderr)

@socketio.on('connect', namespace='/chat')
def handle_connect(data):
    room = session.get("chat")
    join_room(room)
    print('Client connected!', file=sys.stderr)

    messages = Chat.query.order_by(desc(Chat.created_at)).limit(20).all()
    messages = [chat_to_dict(msg) for msg in messages]  # Use chat_to_dict function
    emit('load_messages', messages)

    emit('status', {'msg': 'New client connected!'}, room=room)

@socketio.on('join', namespace='/chat')
def handle_user_join(data):
    room = session.get("chat")
    join_room(room)
    print('Client connected!', file=sys.stderr)

    username = current_user.username  
    join_message = f"User '{username}' has joined the chat"
    emit('chat', {'message': join_message, 'username' :'System'}, room=room, broadcast=True)

@socketio.on("search_message", namespace='/chat')
def handle_search_message(query):
    room = request.sid
    join_room(room)
    page = query.get('page', 1)
    results = Chat.query.filter(Chat.text.contains(query)).paginate(page=page, per_page=10)
    results_list = [chat_to_dict(result) for result in results.items]
    emit("search_results", results_list, room=room)
    leave_room(room)
