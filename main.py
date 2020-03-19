from flask import Flask, request, render_template, redirect, flash
from data import db_session
from data.users import *
from data.__all_models import *
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

CAPTAIN_ID = 1

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


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
@app.route('/works_journal')
def works_journal():
    ses = db_session.create_session()
    return render_template('works_journal.html', works=ses.query(Jobs), current_user=current_user)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.pwd.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        flash("Неправильный логин или пароль")
        return render_template('login.html', form=form, current_user=current_user)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.pwd.data != form.pwd2.data:
            flash("Пароли не совпадают")
            return render_template('register.html', title='Registration', form=form, current_user=current_user)
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            flash("Такой пользователь уже есть")
            return render_template('register.html', title='Регистрация', form=form, current_user=current_user)
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
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/success')
def success():
    return redirect('/')


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    if not current_user.is_authenticated:
        flash("Ошибка доступа! Пожалуйста, авторизуйтесь, чтобы добавлять работы")
        return redirect("/")

    form = Adding_job()

    if form.validate_on_submit():
        ses = db_session.create_session()
        job = Jobs(
            job=form.title.data,
            creator=current_user.id,
            team_leader=int(form.teamlead.data),
            work_size=int(form.work_size.data),
            collaborators=form.collaborators.data,
            start_date=datetime.strptime(form.st_date.data, "%Y-%m-%dT%H:%M") if form.st_date.data else None,
            end_date=datetime.strptime(form.end_date.data, "%Y-%m-%dT%H:%M") if form.end_date.data else None,
            is_finished=form.is_finished.data
        )
        ses.add(job)
        ses.commit()

        return redirect('/')

    return render_template('adding_job.html', title='Добавление работы', form=form, current_user=current_user)


@app.route('/editjob/<job_id>', methods=['GET', 'POST'])
def editjob(job_id):
    if not current_user.is_authenticated:
        flash("Ошибка доступа! Пожалуйста, авторизуйтесь, чтобы добавлять работы")
        return redirect("/")

    ses = db_session.create_session()
    job = ses.query(Jobs).filter(Jobs.id == job_id).first()
    if current_user.id not in (job.creator, CAPTAIN_ID, job.team_leader):
        flash("Ошибка доступа! Вы не можете изменять информацию об этой работе")
        return redirect("/")

    form = Adding_job(
        title=job.job,
        tealead=job.team_leader,
        work_size=job.work_size,
        collaborators=job.collaborators,
        is_finished=job.is_finished
    )

    if form.validate_on_submit():
        job.job = form.title.data
        job.creator = current_user.id
        job.team_leader = int(form.teamlead.data)
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.start_date = datetime.strptime(form.st_date.data, "%Y-%m-%dT%H:%M") if form.st_date.data else job.start_date
        job.end_date = datetime.strptime(form.end_date.data, "%Y-%m-%dT%H:%M") if form.end_date.data else job.end_date
        job.is_finished = form.is_finished.data

        ses.add(job)
        ses.commit()

        flash("Сохранено")
        return redirect("/")

    return render_template('adding_job.html', title='Изменение работы', form=form, current_user=current_user)


@app.route('/deljob/<job_id>', methods=['GET', "POST"])
def deljob(job_id):
    """Т.к. условия задач сформулированы не совсем понятно,
    то удаление.изменение записей могут производить капитан, создатель и тимлид"""

    if not current_user.is_authenticated:
        flash("Ошибка доступа! Пожалуйста, авторизуйтесь, чтобы добавлять работы")
        return redirect("/")

    ses = db_session.create_session()
    job = ses.query(Jobs).filter(Jobs.id == job_id).first()
    if current_user.id not in (job.creator, CAPTAIN_ID, job.team_leader):
        flash("Ошибка доступа! Вы не можете изменять информацию об этой работе")
        return redirect("/")
    ses.delete(job)
    ses.commit()

    flash("Запись успешно удалена")
    return redirect("/")


if __name__ == '__main__':
    db_session.global_init("db/mars.sqlite")
    app.run(port=8080, host='127.0.0.1')
