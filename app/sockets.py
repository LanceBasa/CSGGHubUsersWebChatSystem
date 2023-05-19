from flask import session, request
from app import db, socketio
from app.models import Chat, User,Commands,FavMap,FavWeapon,Map,Weapon,Rank
from flask_socketio import emit, join_room, leave_room
import sys
from sqlalchemy import desc
from flask_login import current_user
from sqlalchemy.orm import joinedload






# for adding entered message in the chat to the database and emitting it back to chatbox
@socketio.on("new_message", namespace='/chat')
def handle_new_message(message):
    if current_user.is_authenticated:
        room = session.get("chat")
        # Create a new Chat object and store it in the database
        chat_message = Chat(text=message, user_id=current_user.id)

        db.session.add(chat_message)
        db.session.commit()

        if message[0]=='~':
            print('it is ~')
            comm=message[1:]
            comm=comm.split()
            item=""
            if(len(comm)>=2):
                item=comm[1]
            command = Commands.query.filter_by(command_name=comm[0]).first()
            comm=command.query_command
            comm=eval(comm)

            emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
            emit("chat", {"message": comm, "username": 'System'}, broadcast=True, room=room)
        else:
            print(f"New message: {message}", file=sys.stderr)
            emit("chat", {"message": message, "username": current_user.username}, broadcast=True, room=room)
    else:
        print("Error: Unauthenticated user tried to send a message", file=sys.stderr)



@socketio.on('connect', namespace='/chat')
def handle_connect(data):
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


@socketio.on('join', namespace='/chat')
def handle_user_join(data):
    # Retrieve the current room from the session
    # Join the room
    room = session.get("chat")

    # Join the room
    join_room(room)
    print('Client connected!', file=sys.stderr)

    username = current_user.username  # Assuming you have the username of the current user
    join_message = f"User '{username}' has joined the chat"
    emit('chat', {'message': join_message, 'username' :'System'}, room=room, broadcast=True)




#------- for special commands-----------------
def get_user_fav_weapons(username):
    user = User.query.filter_by(username=username).first()
    if user:
        fav_weapons = (
            FavWeapon.query
            .join(Weapon)
            .options(joinedload(FavWeapon.weapon))
            .filter_by(user_id=user.id)
            .all()
        )
        return [fav_weapon.weapon.weapon_name for fav_weapon in fav_weapons]
    return 'Username not found'

def get_all_weapon_names():
    weapon_names = Weapon.query.with_entities(Weapon.name).all()
    return [name for (name,) in weapon_names]

def get_weapons_by_category(category):
    weapons = Weapon.query.filter_by(category=category).all()
    return weapons


def get_all_maps():
    maps = Map.query.all()
    return maps

def get_weapon_by_name(name):
    weapon = Weapon.query.filter_by(weapon_name=name).first()
    if weapon:
        text = weapon.description
        return text
    return "No such weapon found"

def get_player_rank(name):
    users = User.query.filter_by(username=name).first()
    return users

def get_user_fav_maps(username):
    user = User.query.filter_by(username=username).first()
    if user:
        fav_maps = (
            FavMap.query
            .join(Map)
            .options(joinedload(FavMap.map))
            .filter_by(user_id=user.id)
            .all()
        )
        return [fav_map.map.map_name for fav_map in fav_maps]
    return 'Username not found'


def get_all_commands():
    commands = Commands.query.all()
    command_names = [command.command_name + command.command_desc for command in commands]
    commands_str = "\" </br> \"".join(command_names)
    return "Here are the available commands:" + commands_str

