# coding=utf-8
from redisco import models

from .base import RBase


class GroupSettings(RBase):
    id = models.Attribute(required=True)
    welcome_text = models.Attribute(default='')
    invite_text = models.Attribute(default='')
    group_tmpl = models.Attribute(default='')
    creators = models.ListField(str, default=[])
