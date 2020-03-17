from . import users
from .jobs import Jobs
from wtforms import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    pwd = PasswordField('Password', validators=[DataRequired()])
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


class Adding_job(FlaskForm):
    title = StringField("Название работы", validators=[DataRequired()])
    teamlead = IntegerField("ID тимлида", validators=[DataRequired()])
    work_size = IntegerField("Время работы")
    collaborators = StringField("ID работников")
    st_date = StringField("Дата начала работы")
    end_date = StringField("Дата окончания работы")
    is_finished = BooleanField("Завершена ли работа")
    add = SubmitField("Добавить")

