import sqlalchemy
from sqlalchemy import orm
import sqlalchemy.ext.declarative as dec
from sqlalchemy import ForeignKey

SqlAlchemyBase = dec.declarative_base()


class Job(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = orm.relation(sqlalchemy.Integer, ForeignKey("users.id"))
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, default=8)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return " ".join(filter(bool, map(str, (self.team_leader, self.job, self.work_size,
                                               self.collaborators, self.is_finished))))
