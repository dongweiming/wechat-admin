# coding=utf-8
from flask import request
from flask.views import MethodView
from flask.blueprints import Blueprint

from ext import db
from models.core import User
from models.setting import GroupSettings
from libs.globals import current_bot

bp = Blueprint('settings', __name__, url_prefix='/settings')


class GroupAPI(MethodView):

    def get(self):
        uid = current_bot.self.puid
        query = db.session.query
        user = query(User).get(uid)

        data = {
            'users': [u.to_dict() for u in user.friends],
            'groups': [group.to_dict() for group in user.groups],
            'mps': [mp.to_dict() for mp in user.mps]

        }
        settings = GroupSettings.get(uid)
        data.update(settings.to_dict())
        data['creators'] = list(set(u['id'] for u in data['users']) &
                                set(str(u, 'u8') for u in data['creators']))
        return data

    def put(self):
        data = request.get_json()
        data['id'] = current_bot.self.puid
        creators = data.pop('creators', [])
        mp_forward = data.pop('mp_forward', [])
        obj = GroupSettings.create(**data)
        if creators:
            obj.creators.clear()
            obj.creators.extend(creators)
            obj.save()
        if mp_forward:
            obj.mp_forward.clear()
            obj.mp_forward.extend(mp_forward)
            obj.save()
        return {}


bp.add_url_rule('/group', view_func=GroupAPI.as_view('group_settings'))
