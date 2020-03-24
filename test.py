import requests
from data import db_session, jobs

# print(requests.get('http://127.0.0.1:8080/api/jobs').json())
#
# print(requests.get('http://127.0.0.1:8080/api/jobs/1').json())
#
# print(requests.get('http://127.0.0.1:8080/api/jobs/99').json())
#
# print(requests.get('http://127.0.0.1:8080/api/jobs/qwerty').json())

print(requests.post('http://127.0.0.1:8080/api/jobs').json())

print(requests.post('http://127.0.0.1:8080/api/jobs', json=dict(
            job='qwerty',
            creator=1,
            team_leader=1
)).json())

print(requests.post('http://127.0.0.1:8080/api/jobs', json=dict(
            id=1,
            job='qwerty',
            creator=1,
            team_leader=1,
            work_size=3,
            collaborators=None,
            start_date=None,
            end_date=None,
            is_finished=False
)).json())

print(requests.post('http://127.0.0.1:8080/api/jobs', json=dict(
            job='qwerty__',
            creator=1,
            team_leader=1,
            work_size=3,
            collaborators=None,
            start_date=None,
            end_date=None,
            is_finished=False
)).json())

db_session.global_init("db/mars.sqlite")
ses = db_session.create_session()
if ses.query(jobs.Jobs).filter(jobs.Jobs.job == 'qwerty__'):
    print('All right!')
else:
    print('Something went wrong!')
