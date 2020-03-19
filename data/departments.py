import sqlalchemy
from .db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    creator_ = orm.relation('User', foreign_keys=[creator])
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    chief_ = orm.relation('User', foreign_keys=[chief])
    job = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id"))
    job_ = orm.relation('Jobs', foreign_keys=[job])
    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return "<Department> " + str(self.id) + str(self.title)
