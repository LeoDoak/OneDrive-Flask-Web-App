from ..xtype import *


def utf8e(s: str) -> bytes:
    return s.encode("utf-8")


def utf8d(b: bytes) -> str:
    return b.decode("utf-8")


def try_utf8d(b: str_or_bytes) -> str:
    try:
        return utf8d(b)
    except:
        return b


def try_utf8e(s: str_or_bytes) -> bytes:
    try:
        return utf8e(s)
    except:
        return s


FULL2HALF = {}
HALF2FULL = {}


def _update_width_map():
    _ = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
    _[0x3000] = 0x20
    HALF2FULL.update(_)
    _ = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
    _[0x20] = 0x3000
    HALF2FULL.update(_)


def f2h_width(s):
    if not FULL2HALF:
        _update_width_map()
    return str(s).translate(FULL2HALF)


def h2f_width(s):
    if not HALF2FULL:
        _update_width_map()
    return str(s).translate(HALF2FULL)


