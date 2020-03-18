import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    chief_obj = orm.relation('User')
    job = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id"))
    job_obj = orm.relation('Jobs')
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "<Department> " + str(self.id) + str(self.title)
