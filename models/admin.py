# coding=utf-8
from walrus import TextField, ListField
from .redis import RBase
from config import group_tmpl, welcome_text, invite_text


class GroupSettings(RBase):
    id = TextField(primary_key=True)
    welcome_text = TextField(default=welcome_text)
    invite_text = TextField(default=invite_text)
    group_tmpl = TextField(default=group_tmpl)
    creators = ListField()
