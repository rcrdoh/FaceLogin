from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """Login form to access writing and settings pages"""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    #id = ObjectField()
#    image = 
    remember_me=BooleanField('Remember Me')
    submit = SubmitField('Sign In')