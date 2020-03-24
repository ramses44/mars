from flask import Blueprint, jsonify, request
from data import db_session, jobs

blueprint = Blueprint('mars_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    js = session.query(jobs.Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')) for item in js]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>',  methods=['GET'])
def get_job(job_id):
    session = db_session.create_session()
    js = session.query(jobs.Jobs).get(job_id)
    if not js:
        return jsonify({'error': 'Not found'})
    return jsonify(js.to_dict(only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished')))


@blueprint.route('/api/jobs/',  methods=['POST'])
def create_job():
    ses = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['team_leader', 'job', 'work_size',
                                                 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    elif ses.query(jobs.Jobs).get(request.json.get('id', -1)):
        return jsonify({'error': 'Id already exists'})
    job = jobs.Jobs(**request.json)
    ses.add(job)
    ses.commit()
    return jsonify({'success': 'OK'})




