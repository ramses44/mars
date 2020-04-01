import requests
from data import db_session, jobs, users

db_session.global_init("db/mars.sqlite")
ses = db_session.create_session()


def test_jobs():

    # GET
    print(requests.get('http://127.0.0.1:8080/api/v2/jobs').json())  # Корректный запрос получения всех работ
    print(requests.get('http://127.0.0.1:8080/api/v2/jobs/1').json())  # Корректный запрос получения одной работы
    print(requests.get('http://127.0.0.1:8080/api/v2/jobs/99').json())  # Некорректный запрос (неверный ID)
    print(requests.get('http://127.0.0.1:8080/api/v2/jobs/qwerty').json())  # Некорректный запрос (неверный параметр)
    print()

    # POST
    print(requests.post('http://127.0.0.1:8080/api/v2/jobs').json())  # Некорректный запрос (без параметров)
    print(requests.post('http://127.0.0.1:8080/api/v2/jobs', json=dict(
                job='qwerty',
                creator=1,
                team_leader=1
    )).json())  # Некорректный запрос (отсутствуют все необходимые параметры)
    print(requests.post('http://127.0.0.1:8080/api/v2/jobs', json=dict(
                job='qwerty__',
                creator=1,
                team_leader=1,
                work_size=3,
                category=2
    )).json())  # Корректный запрос
    if ses.query(jobs.Jobs).filter(jobs.Jobs.job == 'qwerty__'):
        print('All right!')
    else:
        print('Something went wrong!')
    print()

    # DELETE
    print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/990').json())  # Некорректный запрос (неверный ID)
    print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/qwerty').json())  # Неверный параметр (не число)
    print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/2').json())  # Корректный запрос (если id 2 существует)
    if not ses.query(jobs.Jobs).get(2):
        print('All right!')
    else:
        print('Something went wrong!')
    print()

    # PUT
    print(requests.put('http://127.0.0.1:8080/api/v2/jobs/990', json=dict(work_size=10)).json())  # Неверный ID
    print(requests.put('http://127.0.0.1:8080/api/v2/jobs/qwerty', json=dict(work_size=10)).json())  # Неверный параметр
    print(requests.put('http://127.0.0.1:8080/api/v2/jobs/3', json=dict(work_size=10, job='__qwerty__')
                       ).json())  # Корректный запрос (если id 2 существует)
    res = ses.query(jobs.Jobs).get(3)
    if res.work_size == 10 and res.job == '__qwerty__':
        print('All right')
    else:
        print('Smth went wrong')


def test_users():

    # GET
    print(requests.get('http://127.0.0.1:8080/api/v2/users').json())  # Корректный запрос получения всех пользователей
    print(requests.get('http://127.0.0.1:8080/api/v2/users/1').json())  # Корректный запрос получения одного пользователя
    print(requests.get('http://127.0.0.1:8080/api/v2/users/99').json())  # Некорректный запрос (неверный ID)
    print(requests.get('http://127.0.0.1:8080/api/v2/users/qwerty').json())  # Некорректный запрос (неверный параметр)
    print()

    # POST
    print(requests.post('http://127.0.0.1:8080/api/v2/users').json())  # Некорректный запрос (без параметров)
    print(requests.post('http://127.0.0.1:8080/api/v2/users', json=dict(
        login='qwerty__',
        surname='qwerty',
        password='12345'
    )).json())  # Некорректный запрос (отсутствуют все необходимые параметры)
    print(requests.post('http://127.0.0.1:8080/api/v2/users', json=dict(
        login='_qwerty__',
        surname='qwerty',
        name='qwert!',
        password='12345'
    )).json())  # Корректный запрос
    if ses.query(users.User).filter(users.User.login == '_qwerty__'):
        print('All right!')
    else:
        print('Something went wrong!')
    print()

    # DELETE
    print(requests.delete('http://127.0.0.1:8080/api/v2/users/990').json())  # Некорректный запрос (неверный ID)
    print(requests.delete('http://127.0.0.1:8080/api/v2/users/qwerty').json())  # Неверный параметр (не число)
    print(requests.delete('http://127.0.0.1:8080/api/v2/users/2').json())  # Корректный запрос (если id 2 существует)
    if not ses.query(users.User).get(2):
        print('All right!')
    else:
        print('Something went wrong!')
    print()

    # PUT
    print(requests.put('http://127.0.0.1:8080/api/v2/users/990', json=dict(age=23)).json())  # Неверный ID
    print(requests.put('http://127.0.0.1:8080/api/v2/users/qwerty', json=dict(age=23)).json())  # Неверный параметр
    print(requests.put('http://127.0.0.1:8080/api/v2/users/3', json=dict(age=23, login='__qwerty__')
                       ).json())  # Корректный запрос (если id 3 существует)
    res = ses.query(users.User).get(3)
    if res.age == 23 and res.login == '__qwerty__':
        print('All right')
    else:
        print('Smth went wrong')


if __name__ == '__main__':
    test_users()
