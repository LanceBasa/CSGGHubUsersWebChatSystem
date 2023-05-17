from flask import render_template, flash, redirect, url_for, abort
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User, ChatRoom, Chat,RoomUser
from app import socketio, app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from datetime import datetime

@app.route('/')
def homePage():
    return render_template("homePage.html", title='Welcome to CSGGHub')


@app.route('/chat')
@login_required
def chat():
    user_rooms = ChatRoom.query.join(RoomUser).filter(RoomUser.user_id == current_user.id).all()
    return render_template("chat.html", title='chat_rooms - CSGGHub', user_rooms=user_rooms)

@app.route('/profile/<username>')
@login_required 
def profile(username):
    room_user = User.query.filter_by(username=current_user.username).first_or_404()
    if current_user.username != username:
        anotherUser = User.query.filter_by(username=username).first_or_404()
        if anotherUser.private:
            flash('This user profile is private. Viewing your profile')
        else:
            return render_template("profile.html", title='My Profile', user=anotherUser)
    return render_template("profile.html", title='My Profile', user=user)

@app.route('/button')
def button():
    return render_template("button.html", title="Button!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('profile', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homePage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.private = form.isPrivate.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/chat/<int:room_id>')
def chat_room(room_id):
    room = ChatRoom.query.get(room_id)
    if room is None:
        abort(404)

    last_messages = Chat.query.filter_by(room_id=room_id).order_by(Chat.created_at.desc()).limit(10)

    return render_template('chat_box.html', room_id=room_id, room=room, last_messages=last_messages)
