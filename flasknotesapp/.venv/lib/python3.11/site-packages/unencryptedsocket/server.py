from omnitools import encryptedsocket_function, p, utf8d, dt2yyyymmddhhmmss, debug_info
from .utils import recv_all
import threading
import socket
import struct
import pickle
import json


class SS:
    def __init__(
            self, *, functions: encryptedsocket_function = None,
            host: str = "127.199.71.10", port: int = 39291,
            silent: bool = False, backlog: int = 5
    ):
        self.terminate = False
        self.silent = silent
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__s.bind((host, int(port)))
        self.__s.listen(backlog)
        self.functions = functions or {}

    def handler(self, conn: socket.socket, addr: tuple) -> None:
        uid = "{}:{}".format(*addr)
        if not self.silent:
            p("{}\tconnected\t{}".format(dt2yyyymmddhhmmss(), uid))
        try:
            while True:
                request = recv_all(conn)
                if not request:
                    break
                try:
                    request = json.loads(utf8d(request))
                except:
                    request = pickle.loads(request)
                try:
                    if request["command"] in self.functions:
                        response = self.functions[request["command"]](*request["data"][0], **request["data"][1])
                    else:
                        raise Exception("request command '{}' is not in socket functions".format(request["command"]))
                except:
                    response = debug_info()[0]
                try:
                    response = json.dumps(response).encode()
                except TypeError:
                    response = pickle.dumps(response, protocol=2)
                conn.sendall(struct.pack('>I', len(response))+response)
        except:
            p(debug_info()[0])
        finally:
            conn.close()
            if not self.silent:
                p("{}\tdisconnected\t{}".format(dt2yyyymmddhhmmss(), uid))

    def start(self) -> None:
        try:
            while not self.terminate:
                conn, addr = self.__s.accept()
                threading.Thread(target=self.handler, args=(conn, addr)).start()
        except Exception as e:
            if not self.terminate:
                raise e

    def stop(self) -> bool:
        self.terminate = True
        self.__s.close()
        return True

