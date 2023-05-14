from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))
    private = db.Column(db.Boolean, default=False)
    chat = db.relationship('Chat', backref='author', lazy='dynamic')
    created_rooms = db.relationship('ChatRoom', backref='creator', lazy='dynamic')
    fav_weapons = db.relationship('FavWeapon', backref='user', lazy='dynamic')
    fav_maps = db.relationship('FavMap', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class ChatRoom(db.Model):
    __tablename__ = 'chatroom'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(64), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat = db.relationship('Chat', backref='room', lazy='dynamic')

    def __repr__(self):
        return '<ChatRoom {}>'.format(self.room_name)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))

    def __repr__(self):
        return '<Chat {}>'.format(self.text)



class RoomUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('chatroom.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<RoomUser {}>'.format(self.id)

class FavWeapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapon.id'))

    def __repr__(self):
        return '<FavWeapon {}>'.format(self.id)

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weapon_name = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    description = db.Column(db.String(500))
    users = db.relationship('FavWeapon', backref='weapon', lazy='dynamic')

    def __repr__(self):
        return '<Weapon {}>'.format(self.weapon_name)

class FavMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    map_id = db.Column(db.Integer, db.ForeignKey('map.id'))

    def __repr__(self):
        return '<FavMap {}>'.format(self.id)

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(64), unique=True)
    users = db.relationship('FavMap', backref='map', lazy='dynamic')

    def __repr__(self):
        return '<Map {}>'.format(self.map_name)

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='rank', lazy='dynamic')

    def __repr__(self):
        return '<Rank {}>'.format(self.rank_name)
