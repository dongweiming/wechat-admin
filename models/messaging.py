from ext import db


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer)
    operator_type = db.Column(db.SmallInteger)
    payload = db.Column(db.PickleType)

    def __init__(self, operator_id, operator_type, payload):
        self.operator_id = operator_id
        self.operator_type = operator_type
        self.payload = payload

    def __repr__(self):
        return '<Log %r>' % self.id


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, default=0, index=True)
    sender_id = db.Column(db.Integer, index=True)
    receiver_id = db.Column(db.Integer, index=True)
    content = db.Column(db.String(255))

    def __init__(self, group_id, sender_id, receiver_id, content):
        self.group_id = group_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id


    def __repr__(self):
        return '<Message %r>' % self.id
