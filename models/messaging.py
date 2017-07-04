from sqlalchemy.ext.hybrid import hybrid_property

from ext import db
from .mixin import BaseMixin
from .core import User, Group, MP
from libs.consts import ID_TO_TYPE_MAP, MP as _MP
from libs.utils import cached_hybrid_property


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
    url = db.Column(db.String(512), default='')
    file_ext = db.Column(db.String(20), default='')

    def __repr__(self):
        return '<Message %r>' % self.id

    @cached_hybrid_property
    def query(self):
        return db.session.query

    @hybrid_property
    def group(self):
        if not self.group_id:
            return {}
        group = self.query(Group).get(self.group_id)
        return group.to_dict() if group else {}

    @hybrid_property
    def sender(self):
        if not self.sender_id:
            return {}
        user = self.query(MP if self.type == _MP else User).get(self.sender_id)
        return user.to_dict() if user else {}

    @cached_hybrid_property
    def msg_type(self):
        return ID_TO_TYPE_MAP.get(self.type, 'Text')

    def to_dict(self):
        dct = super().to_dict()
        for p in ('sender', 'group', 'msg_type'):
            dct[p] = getattr(self, p)
        return dct
