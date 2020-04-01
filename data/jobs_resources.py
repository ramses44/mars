from flask_restful import abort, Resource
from data import db_session
from data.jobs import Jobs
from data.categories import Category
from flask import jsonify
from .jobs_reqparse import post_parser, put_parser
from datetime import datetime


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):

    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(only=('job', 'team_leader', 'creator', 'work_size',
                                                 'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        job.category = list()
        session.commit()
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        ses = db_session.create_session()
        res = ses.query(Jobs).get(job_id)
        args = put_parser.parse_args()

        try:
            if args['team_leader']:
                res.team_leader = args['team_leader']
            if args['job']:
                res.job = args['job']
            if args['work_size']:
                res.work_size = args['work_size']
            if args['collaborators']:
                res.collaborators = args['collaborators']
            if args['start_date']:
                res.start_date = datetime.strptime(args['start_date'], "%Y-%m-%dT%H:%M")
            if args['end_date']:
                res.end_date = datetime.strptime(args['end_date'], "%Y-%m-%dT%H:%M")
            if args['is_finished']:
                res.is_finished = args['is_finished']
            if args['category']:
                res.category.append(ses.query(Category).filter(Category.id == args['category']).first())

            ses.commit()
            return jsonify({'success': 'OK'})

        except ValueError:
            abort(400, message='Please, send the data in the correct format')


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('job', 'team_leader', 'collaborators', 'is_finished')) for item in news]})

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()
        try:
            job = Jobs(
                job=args['job'],
                team_leader=args['team_leader'],
                work_size=args['work_size'],
                collaborators=args['collaborators'],
                is_finished=args['is_finished'],
                start_date=datetime.strptime(args['start_date'], "%Y-%m-%dT%H:%M") if args['start_date'] else None,
                end_date=datetime.strptime(args['end_date'], "%Y-%m-%dT%H:%M") if args['end_date'] else None
            )
            job.category.append(session.query(Category).filter(Category.id == args['category']).first())

            session.add(job)
            session.commit()
            return jsonify({'success': 'OK'})
        except ValueError:
            abort(400, message='Please, send the data in the correct format')
