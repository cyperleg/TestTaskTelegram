from enum import Enum


class APIException(Exception):
    pass


class AuthException(Exception):
    pass


class FilterBy(Enum):
    WATCHED = "watched"
    UNWATCHED = "unwatched"


class TypeBy(Enum):
    CHANNEL = "channel"
    GROUP = "group"
    CHAT = "chat"
