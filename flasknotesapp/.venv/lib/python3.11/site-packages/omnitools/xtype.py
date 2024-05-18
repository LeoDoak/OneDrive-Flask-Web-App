from typing import *
import re


str_or_bytes = Union[str, bytes]
list_or_dict = Union[list, dict]
list_or_tuple = Union[list, tuple]
bytes_or_list = Union[bytes, list]
key_pair_format = Dict[str, bytes]
color_value = Tuple[int, int, int]
encryptedsocket_function = Dict[str, Callable[[Any], Any]]


# class obj(object):
#     def __init__(self, ref):
#         self.__ref = ref
#
#     def __setattr__(self, key, value):
#         if isinstance(value, self.type):
#             object.__setattr__(self, key, value)
#         else:
#             self.__ref.__setattr__(key, value)
#
#     def __getattr__(self, item):
#         try:
#             return object.__getattribute__(self, item)
#         except:
#             try:
#                 return self.type.__getattribute__(self.__ref, item)
#             except:
#                 raise AttributeError


class Obj(object):
    def __init__(self, d: dict=None):
        if d is not None:
            if isinstance(d, dict):
                self.update(d)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def update(self, d):
        for k in d:
            self.__setitem__(k, d[k])

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def pop(self, key):
        v = self.__getitem__(key)
        self.__delitem__(key)
        return v

    def get(self, k):
        return self.__getitem__(k)


class HeadersDict(Obj):
    def __getitem__(self, key):
        return self.__dict__[self.rkey(key)]

    def __setitem__(self, key, value):
        self.__dict__[self.rkey(key)] = value

    def __delitem__(self, key):
        del self.__dict__[self.rkey(key)]

    def __contains__(self, key):
        return self.rkey(key) in self.__dict__

    def rkey(self, key):
        return "-".join(_[0].upper()+_[1:] if len(_) > 1 else _.upper() for _ in key.lower().replace(" ", "-").replace("_", "-").split("-"))


class ApacheHeadersDict(HeadersDict):
    def __setitem__(self, key, value):
        key = self.rkey(key)
        if key.startswith("Http-"):
            self.__dict__[key[5:]] = value
        self.__dict__[key] = value

    def __delitem__(self, key):
        key = self.rkey(key)
        if "Http-"+key in self.__dict__:
            del self.__dict__["Http-"+key]
        del self.__dict__[key]



