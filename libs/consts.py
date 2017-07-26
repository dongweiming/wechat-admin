from wxpy.api.consts import *  # noqa

MP = 'MP'

ID_TO_TYPE_MAP = {
    1: TEXT,
    2: SHARING,
    3: PICTURE,
    4: VIDEO,
    5: CARD,
    6: MP,
    0: 'Default'
}

TYPE_TO_ID_MAP = {v: k for k, v in ID_TO_TYPE_MAP.items()}
