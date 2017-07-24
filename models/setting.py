# coding=utf-8
from walrus import TextField, ListField, JSONField, IntegerField
from .redis import RBase
from config import welcome_text, invite_text, kick_text, group_patterns


class GroupSettings(RBase):
    id = TextField(primary_key=True)
    welcome_text = TextField(default=welcome_text)
    invite_text = TextField(default=invite_text)
    group_patterns = JSONField(default=group_patterns)
    creators = ListField()
    mp_forward = JSONField(default=[])
    kick_quorum_n = IntegerField(default=5)
    kick_period = IntegerField(default=5)
    kick_text = TextField(default=kick_text)
