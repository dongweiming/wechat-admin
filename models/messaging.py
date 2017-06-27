from ext import db
from .mixin import BaseMixin


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_id = db.Column(db.Integer)
    operator_type = db.Column(db.SmallInteger)
    payload = db.Column(db.PickleType)

    def __init__(self, operator_id, operator_type, payload):
        self.operator_id = operator_id
        self.operator_type = operator_type
        self.payload = payload

    def __repr__(self):
        return '<Log %r>' % self.id


class Message(BaseMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.String(20), default=0, index=True)
    sender_id = db.Column(db.String(20), index=True)
    receiver_id = db.Column(db.String(20), index=True)
    content = db.Column(db.String(255))
    receive_time = db.Column(db.DateTime)
    type = db.Column(db.SmallInteger)
    url = db.Column(db.String(255), default='')

    def __repr__(self):
        return '<Message %r>' % self.id
