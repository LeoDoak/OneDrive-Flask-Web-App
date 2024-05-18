import json
from typing import *
import textwrap
from .xencode import b64e, utf8e


def jd(o: Any, **kwargs) -> str:
    return json.dumps(o, **kwargs)


def jd_and_b64e(o: Any, **kwargs) -> str:
    return b64e(jd(o, **kwargs))


def jd_and_utf8e(o: Any, **kwargs) -> bytes:
    return utf8e(jd(o, **kwargs))


def jl(s: str, **kwargs) -> Any:
    return json.loads(s, **kwargs)


def _dumpobj(obj: Any, isObj: bool = False, indent: int = -1, indent_scale: int = 4) -> str:
    do_indent = True if indent >= 0 else False
    if indent >= 0 and indent % indent_scale != 0:
        raise Exception("indent {} is not multiples of indent_scale {}".format(indent, indent_scale))
    try:
        if not isinstance(obj, (tuple, list, dict, bool)):
            return jd(obj)
        raise
    except:
        from .xtype import Obj
        if isinstance(obj, (bytes, bool)):
            return str(obj)
        elif isinstance(obj, (tuple, list)):
            tmp = "[" if isinstance(obj, list) else "("
            if do_indent:
                tmp += "\n"
                indent += indent_scale
            for i, item in enumerate(obj):
                if i:
                    tmp += ","
                    if do_indent:
                        tmp += "\n"
                    else:
                        tmp += " "
                if do_indent:
                    if not isinstance(item, Obj):
                        tmp += " "*indent
                tmp += _dumpobj(item, indent=indent, indent_scale=indent_scale)
            if do_indent:
                tmp += "\n"
                tmp += " "*(indent-indent_scale)
            tmp += "]" if isinstance(obj, list) else ")"
            return tmp
        elif isinstance(obj, dict):
            col = ": "
            tmp = "Obj({" if isObj else "{"
            tmp += "\n"
            if do_indent:
                indent += indent_scale
            else:
                tmp = "{"
            for i, (k, v) in enumerate(obj.items()):
                if i:
                    tmp += ","
                    if do_indent:
                        tmp += "\n"
                    else:
                        tmp += " "
                if do_indent:
                    tmp += " "*indent
                nextisObj = True if isinstance(v, Obj) else False
                v = _dumpobj(v, indent=indent, indent_scale=indent_scale)
                if nextisObj:
                    import re
                    v = v.replace(re.search(r"([ ]+)", v)[0], "", 1).replace(re.search(r"([ ]+)", v)[0][:-2], "")
                tmp += '''{}{}{}'''.format(_dumpobj(k), col, v)
            if do_indent:
                tmp += "\n"
                tmp += " "*(indent-indent_scale)
            tmp += "}"
            if isObj:
                tmp += ")"
            return tmp
        elif isinstance(obj, Obj):
            return obj.dump(indent_scale=indent_scale)
        else:
            return '''{}({})'''.format(type(obj).__name__, str(obj))


def dumpobj(obj: Any, isObj: bool = False, indent_scale: int = 0) -> str:
    import inspect
    stack = [a[3] for a in inspect.stack()]
    dumpobjsize = len([_ for _ in stack if _ == inspect.stack()[1][3]])
    dumpsize = len([_ for _ in stack if _ == "dump"])
    indent = -1 if indent_scale <= 0 else 0
    dumps = _dumpobj(obj, isObj, indent, indent_scale)
    if dumpobjsize >= 2 and dumpobjsize == dumpsize:
        dumpobjsize += 1
        dumps = textwrap.indent(dumps, " "*(dumpobjsize)*indent_scale)
        return dumps
    elif dumpobjsize-1 >= 2 and dumpobjsize > dumpsize:
        dumps = textwrap.indent(dumps, " "*dumpobjsize*indent_scale)
        return dumps
    else:
        return dumps


