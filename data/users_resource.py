from flask_restful import abort, Resource
from data import db_session
from data.users import User
from flask import jsonify
from .users_reqparse import post_parser, put_parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):

    def get(self, uid):
        abort_if_user_not_found(uid)
        session = db_session.create_session()
        user = session.query(User).get(uid)
        return jsonify({'user': user.to_dict(only=('login', 'name', 'surname', 'age',
                                                   'position', 'speciality', 'created_date',))})

    def delete(self, uid):
        abort_if_user_not_found(uid)
        session = db_session.create_session()
        user = session.query(User).get(uid)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, uid):
        abort_if_user_not_found(uid)
        ses = db_session.create_session()
        res = ses.query(User).get(uid)
        args = put_parser.parse_args()

        if args['login']:
            res.login = args['login']
        if args['surname']:
            res.surname = args['surname']
        if args['name']:
            res.name = args['name']
        if args['age']:
            res.age = args['age']
        if args['position']:
            res.position = args['position']
        if args['speciality']:
            res.speciality = args['speciality']
        if args['address']:
            res.address = args['address']

        ses.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('login', 'surname', 'name', 'position')) for item in users]})

    def post(self):
        args = post_parser.parse_args()
        session = db_session.create_session()

        user = User(
            login=args['login'],
            password=args['password'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address']
        )

        user.set_password(args['password'])

        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
