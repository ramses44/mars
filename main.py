from flask import Flask, request, render_template, redirect
from data import db_session
from data.users import *
from data.jobs import *
from data.__all_models import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_user(login, pwd, name, sname, age, pos, spec, addr, **kwargs):
    user = User()
    user.name = name
    user.surname = sname
    user.login = login
    user.set_password(pwd)
    user.age = int(age) if age else -1
    user.speciality = spec
    user.address = addr
    user.position = pos

    session = db_session.create_session()
    session.add(user)
    session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        user = session.query(User).filter(User.login == form.login.data).first()
        return redirect('/success') if user and \
            user.check_password(form.pwd.data) else render_template('login.html',
                                                                    title='Log in',
                                                                    form=form,
                                                                    message="Wrong login/password")
    return render_template('login.html', title='Log in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.pwd.data != form.pwd2.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.sname.data,
            login=form.login.data,
            position=form.pos.data,
            age=form.age.data,
            speciality=form.spec.data,
            address=form.addr.data
        )
        user.set_password(form.pwd.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/success')
def success():
    return "You logged in successfully"


def first_work():
    """Требуемая в задаче ф-ия"""
    ses = db_session.create_session()
    data = dict(team_leader=1, job="deployment of residential modules 1 and 2",
                work_size=15, collaborators="2, 3", is_finished=False)
    work = Jobs(**data)
    ses.add(work)
    ses.commit()


if __name__ == '__main__':
    db_session.global_init("db/mars.sqlite")
    first_work()
    # app.run(port=8080, host='127.0.0.1')
