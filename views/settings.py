# coding=utf-8
from flask import request
from flask.views import MethodView
from flask.blueprints import Blueprint

from ext import db
import views.errors as errors
from views.exceptions import ApiException
from models.core import User, Group, friendship, group_relationship
from models.admin import GroupSettings
from libs.globals import current_bot

bp = Blueprint('settings', __name__, url_prefix='/settings')


class GroupAPI(MethodView):
    def get(self):
        uid = current_bot.self.puid
        query = db.session.query
        user = query(User).get(uid)
        users = user.friends
        total = users.count()
        users = users.all()

        data = {
            'total': total,
            'users': [user.to_dict() for user in users]
        }
        settings = GroupSettings.get(uid)
        data.update(settings.to_dict())
        return data

    def put(self):
        data = request.get_json()
        data['id'] = current_bot.self.puid
        creators = data.pop('creators', [])
        obj = GroupSettings.create(**data)
        if creators:
            obj.creators.clear()
            obj.creators.extend(creators)
            obj.save()
        return {}


bp.add_url_rule('/group', view_func=GroupAPI.as_view('group_settings'))
