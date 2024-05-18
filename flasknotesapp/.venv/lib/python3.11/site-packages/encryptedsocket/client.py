from omnitools import jd_and_utf8e, utf8d, args, randb, b64d, b64e, jl
from .utils import encrypt, recv_all, decrypt
from easyrsa import EasyRSA
from typing import *
import socket
import pickle
import struct


class SC(object):
    def __init__(self, *, host: str = "127.199.71.10", port: int = 39291):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((host, int(port)))
        self.__key = None
        hash, public_key = self.request(command="get_pkey")
        public_key = b64d(public_key)
        rsa = EasyRSA(public_key=public_key)
        if rsa.verify(msg=public_key, sig=b64d(hash)):
            key = randb(32)
            self.request(command="set_key", data=args(b64e(rsa.encrypt(key))))
            self.__key = key
        else:
            raise Exception("current connection is under MITM attack")

    def request(self, *, command: str, data: Tuple[Tuple, Dict] = args()) -> Any:
        request = dict(command=command, data=data)
        try:
            request = jd_and_utf8e(request)
        except:
            request = pickle.dumps(request)
        if self.__key:
            request = encrypt(self.__key, request)
        self.__s.sendall(struct.pack('>I', len(request)) + request)
        response = utf8d(recv_all(self.__s))
        if self.__key:
            return decrypt(self.__key, response)
        else:
            return jl(response)

    def __del__(self):
        self.close()

    def close(self):
        self.__s.close()


