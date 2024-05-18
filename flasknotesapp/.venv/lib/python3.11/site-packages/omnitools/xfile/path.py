import os
import sys
import inspect


def temp_dir() -> str:
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    raise Exception("py script has no temp dir")


def abs_main_dir(depth: int = 1, if_py: str = "", if_bundled: str = "") -> str:
    if getattr(sys, 'frozen', False):
        exe_dir = abs_dir(sys.executable)
        exe_dir = join_path(exe_dir, if_bundled)
        return exe_dir
    else:
        py_dir = abs_dir(inspect.stack()[int(depth)][1])
        py_dir = join_path(py_dir, if_py)
        return py_dir


def abs_dir(fn: str) -> str:
    return os.path.dirname(os.path.abspath(fn))


def join_path(*paths: str) -> str:
    return os.path.normpath(os.path.join(*paths))


def get_cwd() -> str:
    return os.getcwd()


