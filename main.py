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


# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == "GET":
#         return render_template('register.html')
#     elif request.method == "POST":
#         if request.form['pwd'] == request.form['pwd2'] != "":
#             add_user(**request.form)
#             return "Register complited"
#         else:
#             return "Wrong answers"


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


def add_colonists():
    """Требуемая в задаче ф-ия"""
    session = db_session.create_session()

    users = [
        dict(surname='Scott', name='Ridley', age=21, position='captain',
             speciality='research engineer', address='module_1', email='scott_chief@mars.org'),
        dict(surname='Surname1', name='Name1', age=666, position='pos1',
             speciality='spec1', address='addr1', email='email1'),
        dict(surname='Surname2', name='Name2', age=2, position='pos2',
             speciality='spec2', address='addr2', email='email2'),
        dict(surname='Surname3', name='Name3', age=3, position='pos3',
             speciality='spec3', address='addr3', email='email3'),
    ]

    for udata in users:
        user = User(**udata)
        session.add(user)

    session.commit()


if __name__ == '__main__':
    db_session.global_init("db/mars.sqlite")
    add_colonists()
    # app.run(port=8080, host='127.0.0.1')
