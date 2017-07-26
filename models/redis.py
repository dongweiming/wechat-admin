from walrus import Database, Model, ListField, SetField, HashField
from config import REDIS_URL

db = Database.from_url(REDIS_URL)
LISTENER_TASK_KEY = 'listener:task_id'


class RBase(Model):
    __database__ = db

    def to_dict(self):
        data = {}
        for name, field in self._fields.items():
            if name in self._data:
                val = self._data[name]
                data[name] = val if field._as_json else field.db_value(val)
            else:
                if isinstance(field, ListField):
                    type_func = list
                elif isinstance(field, SetField):
                    type_func = set
                elif isinstance(field, HashField):
                    type_func = dict
                else:
                    type_func = lambda x: x
                data[name] = type_func(getattr(self, name))
        return data

    @classmethod
    def get(cls, id):
        try:
            return super().get(cls.id == id)
        except ValueError:
            return cls.create(id=id)
