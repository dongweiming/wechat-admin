import redisco
from redisco import models
from redis import Redis

from config import REDIS_URL

redisco.connection = Redis.from_url(REDIS_URL)


class RBase(models.Model):

    @classmethod
    def create_or_update(cls, **kw):
        id = kw.get('id', None)
        if id is None:
            return False
        obj = cls.objects.get_by_id(id)
        if not obj:
            return cls.objects.get_or_create(**kw)
        obj.update_attributes(save=True, **kw)
        obj.save()
        return obj

    def to_dict(self):
        return self.attributes_dict

    @classmethod
    def get(cls, id):
        obj = cls.objects.get_by_id(id)
        if obj:
            return obj.to_dict()
        dct = {
            column: cls._attributes[column].default or ''
            for column in cls._attributes.keys()
        }
        dct.update({
            column: cls._lists[column].default or []
            for column in cls._lists.keys()
        })
        if 'id' in dct and not dct['id']:
            dct['id'] = id
        return dct
