import inspect
import gc
from types import FrameType


def qualname(frame: FrameType) -> str:
    return where(frame).__qualname__


def classname(frame: FrameType) -> str:
    try:
        return frame.f_locals["self"].__class__.__name__
    except:
        if "." in qualname(frame):
            return qualname(frame).split(".")[0]
        else:
            raise Exception("frame is not in a class")


def where(frame: FrameType) -> object:
    return [obj for obj in gc.get_referrers(frame.f_code) if inspect.isfunction(obj)][0]

