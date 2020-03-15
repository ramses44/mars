from . import users, jobs
from wtforms import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    pwd = PasswordField('Passwoed', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    login = StringField('Login/Email', validators=[DataRequired()])
    pwd = PasswordField('Password', validators=[DataRequired()])
    pwd2 = PasswordField('Repeat password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    sname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    spec = StringField("Speciality", validators=[DataRequired()])
    addr = StringField("Address")
    pos = TextAreaField("Position")
    submit = SubmitField('Submit')

