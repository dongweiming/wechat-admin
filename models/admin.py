# coding=utf-8
from ext import store

GROUP_CREATOR_MC_KEY = 'group:creators'


class GroupSettings():
    @staticmethod
    def get_creators():
        return store.lrange(GROUP_CREATOR_MC_KEY, 0, -1)

    @staticmethod
    def set_creators(creators):
        store.delete(GROUP_CREATOR_MC_KEY)
        return store.rpush(GROUP_CREATOR_MC_KEY, *creators)
