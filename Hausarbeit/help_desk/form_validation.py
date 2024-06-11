from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators, IntegerField

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.Length(min=5, max=25),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class UserStoryForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=5, max=50)])
    story_points = IntegerField('Story Points', [validators.NumberRange(min=1, max=2)])
    status = StringField('Status', [validators.Length(min=4, max=10)])
    created_by = StringField('Created By', [validators.Length(min=4, max=25)])

class UserStoryDeleteForm(FlaskForm):
    submit = SubmitField('Delete User Story')

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=5, max=25)])