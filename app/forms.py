from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    # Login form with username, password, and remember me fields
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    # Registration form with username, email, password, and password confirmation fields
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Custom validation to check if the username already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

# Custom validation to check if the email address already exists in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfileForm(FlaskForm):
      # Edit profile form with username, about me, favorite maps, favorite weapons, and privacy fields
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=300)])
    fav_maps = SelectMultipleField('Favorite Maps', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    fav_weapons = SelectMultipleField('Favorite Weapons', coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    isPrivate = BooleanField('Keep Account Private?')
    submit = SubmitField('Submit')
