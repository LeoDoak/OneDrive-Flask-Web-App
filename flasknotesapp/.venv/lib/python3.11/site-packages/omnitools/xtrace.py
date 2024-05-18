import os
import sys
import inspect
from .xinspect import qualname, FrameType


def errorstacks() -> tuple:
    exc_info = sys.exc_info()
    e = exc_info[1]
    tb = exc_info[2]
    stacks = []
    while True:
        try:
            lineno = tb.tb_lineno
            filename = os.path.basename(tb.tb_frame.f_code.co_filename)
            info = str(e)
            stacks.append((type(e).__name__, _qualname(tb.tb_frame) + "@" + filename + ":" + str(lineno), info + "\n"))
            tb = tb.tb_next
        except:
            return tuple(stacks)


def successstacks() -> tuple:
    stacks = []
    for stack in inspect.stack():
        lineno = stack[2]
        filename = os.path.basename(stack[1])
        frame = stack[0]
        stacks.append(_qualname(frame, stack[3]) + "@" + filename + ":" + str(lineno))
    return tuple(stacks)


def _qualname(frame: FrameType, where: str = "") -> str:
    try:
        return "'{}'".format(qualname(frame))
    except:
        return "'{}'".format(where)


