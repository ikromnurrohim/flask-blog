from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        print(username.data) # is value
        print(username) # is input html
        user = User.query.filter_by(username=username.data).first() # first() if this return large data, it can limit 1. ex data[0]
        if user:
            raise ValidationError('Your username is Taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() # first() if this return large data, it can limit 1. ex data[0]
        if user:
            raise ValidationError('Your email is Taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm): 
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            print(username.data) # is value
            print(username) # is input html
            user = User.query.filter_by(username=username.data).first() # first() if this return large data, it can limit 1. ex data[0]
            if user:
                raise ValidationError('Username is Taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() # first() if this return large data, it can limit 1. ex data[0]
            if user:
                raise ValidationError('Email is Taken. Please choose a different one.')
            

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')