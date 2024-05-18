from omnitools import args, utf8d
from .utils import recv_all
from io import BytesIO
from typing import *
import socket
import pickle
import json


class SC:
    def __init__(self, *, host: str = "127.199.71.10", port: int = 39291) -> None:
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((host, int(port)))

    def request(self, *, command: str, data: Tuple[Tuple, Dict] = args()):
        request = dict(command=command, data=data)
        try:
            request = json.dumps(request).encode()
        except:
            request = pickle.dumps(request, protocol=2)
        import struct
        self.__s.send(struct.pack('>I', len(request)) + request)
        response = recv_all(self.__s)
        try:
            return json.loads(utf8d(response))
        except UnicodeDecodeError:
            return pickle.loads(response)
        except json.decoder.JSONDecodeError:
            return pickle.load(BytesIO(response), encoding='latin1')

    def close(self):
        self.__s.close()

