from datetime import datetime

from flask_sse import sse  # noqa
from sqlalchemy import Column, DateTime
from flask_sqlalchemy import SQLAlchemy, Model


class BaseModel(Model):
    create_at = Column(DateTime, default=datetime.utcnow())

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}


db = SQLAlchemy(model_class=BaseModel)
