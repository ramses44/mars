from flask import Flask, request, render_template
from data import db_session
from data.users import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_user(login, pwd, name, sname, age, pos, spec, addr, **kwargs):

    user = User()
    user.name = name
    user.surname = sname
    user.login = login
    user.password = pwd
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


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        if request.form['pwd'] == request.form['pwd2'] != "":
            add_user(**request.form)
            return "Register complited"
        else:
            return "Wrong answers"


if __name__ == '__main__':
    db_session.global_init("db/mars.sqlite")
    app.run(port=8080, host='127.0.0.1')
