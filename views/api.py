# coding=utf-8
from flask import Flask, request
from flask.views import MethodView
from sqlalchemy import and_
from itchat.signals import scan_qr_code, confirm_login, logged_in

import config
import views.errors as errors
from views.utils import ApiResult
from views.exceptions import ApiException
import views.settings as settings
from libs.tasks import async_retrieve_data
from libs.globals import current_bot, _wx_ctx_stack
from libs.wx import get_logged_in_user
from ext import db, sse

from models.core import User, Group, friendship, group_relationship

PER_PAGE = 20


class ApiFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, dict):
            if 'r' not in rv:
                rv['r'] = 0
            rv = ApiResult(rv)
        if isinstance(rv, ApiResult):
            return rv.to_response()
        return Flask.make_response(self, rv)


def create_app():
     app = ApiFlask(__name__)
     app.config.from_object(config)
     db.init_app(app)

     app.register_blueprint(settings.bp)

     return app


json_api = create_app()


# For local test env
@json_api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@json_api.errorhandler(ApiException)
def api_error_handler(error):
    return error.to_result()


@json_api.errorhandler(403)
@json_api.errorhandler(404)
@json_api.errorhandler(500)
def error_handler(error):
    if hasattr(error, 'name'):
        msg = error.name
        code = error.code
    else:
        msg = error.message
        code = 500
    return ApiResult({'message': msg}, status=code)


@json_api.route('/login', methods=['post'])
def login():
    user = get_logged_in_user(current_bot)
    sse.publish({'type': 'logged_in', 'user': user}, type='login')
    async_retrieve_data(current_bot)
    return {'msg': ''}


@json_api.route('/logout', methods=['post'])
def logout():
    _wx_ctx_stack.pop()
    return {'msg': ''}


class UsersAPI(MethodView):
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        type = request.args.get('type', 'contact')
        q = request.args.get('q', '')
        uid = current_bot.self.puid
        query = db.session.query
        if type == 'contact':
            user = query(User).get(uid)
            if q:
                users = query(User).outerjoin(
                    friendship, friendship.c.user_id==User.id).filter(and_(
                        User.nick_name.like('%{}%'.format(q)),
                        friendship.c.friend_id==user.id)
                    )
            else:
                users = user.friends
            total = users.count()
            users = users.offset((page-1)*page_size).limit(page_size).all()
            group = ''
        elif type == 'group':
            group_id = request.args.get('gid', '')
            group = query(Group).get(group_id)
            if q:
                users = query(User).outerjoin(
                    group_relationship,
                    group_relationship.c.user_id==User.id).filter(and_(
                        User.nick_name.like('%{}%'.format(q)),
                        group_relationship.c.group_id==group.id)
                    )
                total = users.count()
                users = users.offset((page-1)*page_size).limit(page_size).all()
            else:
                users = group.members[(page-1)*page_size:page*page_size]
                total = group.count
            group = group.to_dict()
        return {
            'total': total,
            'group': group,
            'users': [user.to_dict() for user in users]
        }
    def put(self):
        verify_content = request.args.get('verifyContent', '')
        ids = set(request.args.getlist('wxid[]'))
        users = [u for u in sum([g.members for g in current_bot.groups()], [])
                if u.puid in ids]
        if users is None:
            raise ApiException(errors.not_found)
        for user in users:
            pass
            # current_bot.add_friend(user, verify_content)
        unexpected = ids.difference(set([u.id for u in users]))
        if unexpected:
            raise ApiException(
                errors.not_found,
                '如下puid用户未找到: {}'.format(','.join(unexpected)))
        return {}

    def delete(self):
        type = request.args.get('type')
        if type == 'contact':
            raise ApiException(errors.unimplemented_error,
                               'ItChat不支持删除好友')
        elif type == 'group':
            group_id = request.args.get('gid')
            ids = request.args.get('ids')
            group = current_bot.groups().search(puid=group_id)
            if not group:
                raise ApiException(errors.not_found)
            group = group[0]
            for uid in ids:
                group.remove_members(group.members.search(puid=uid))
            return {}

@json_api.route('/groups')
def groups():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    q = request.args.get('q', '')
    uid = current_bot.self.puid
    query = db.session.query
    if q:
        groups = query(Group).filter(Group.nick_name.like('%{}%'.format(q)))
        total = groups.count()
    else:
        groups = query(Group)
        total = groups.count()
    groups = groups.offset((page-1)*page_size).limit(page_size).all()
    return {
        'total': total,
        'groups': [group.to_dict() for group in groups]
    }


class UserAPI(MethodView):

    def delete(self, id):
        type = request.args.get('type')
        if type == 'contact':
            raise ApiException(errors.unimplemented_error,
                               'ItChat不支持删除好友')
        elif type == 'group':
            group_id = request.args.get('gid')
            group = current_bot.groups().search(puid=group_id)
            if not group:
                raise ApiException(errors.not_found)
            group = group[0]
            group.remove_members(group.members.search(puid=id))
            return {}

    def put(self, id):
        verify_content = request.args.get('verifyContent', '')
        user = next((u for u in sum([g.members for g in current_bot.groups()], [])
                     if u.puid == id), None)
        if user is None:
            raise ApiException(errors.not_found)
        current_bot.add_friend(user, verify_content)
        return {}


@json_api.route('/all_users')
def all_users():
    all_ids = set([u.puid for u in sum(
        [g.members for g in current_bot.groups()], [])])
    friend_ids = set([u.puid for u in current_bot.friends()])
    # ids = all_ids.difference(friend_ids)
    ids = [u.id for u in db.session.query(User).all()]
    users = [u.to_dict() for u in db.session.query(User).filter(
        User.id.in_(ids)).all()]
    return {'users': users}


json_api.add_url_rule('/user/<id>', view_func=UserAPI.as_view('user'))
json_api.add_url_rule('/users', view_func=UsersAPI.as_view('users'))
