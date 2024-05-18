from base64 import b64decode, b64encode
from ..xtype import *
from .utf8 import *


def b64e(s: str_or_bytes) -> str:
    if isinstance(s, str):
        return b64e(utf8e(s))
    return utf8d(b64encode(s))


def b64d(s: str) -> bytes:
    return b64decode(s)


def b64d_and_utf8d(s: str) -> str:
    return utf8d(b64d(s))


def try_b64d(s: str) -> str_or_bytes:
    try:
        return b64d(s)
    except:
        return s


def b64d_or_utf8e(v: str) -> bytes:
    try:
        return b64d(v)
    except:
        return utf8e(v)

