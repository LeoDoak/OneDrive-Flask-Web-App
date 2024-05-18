from omnitools import machd, jl, str_or_bytes
from aescipher import AESCipherCBCnoHASH
from typing import *
import pickle
import struct
import socket


def recv_all(conn: socket.socket) -> bytes:
    length = conn.recv(4)
    if length == b"":
        return b""
    length = struct.unpack('>I', length)[0]
    content = b""
    while len(content) < length:
        content += conn.recv(length-len(content))
        if not content:
            break
    return content


def encrypt(key: bytes, plaintext: str_or_bytes) -> bytes:
    ciphertext = AESCipherCBCnoHASH(key=key).encrypt(plaintext)
    hash = machd(key=key, content=ciphertext)
    return "{} {}".format(hash, ciphertext).encode()


def decrypt(key: bytes, ciphertext: str) -> Any:
    hash, ciphertext = ciphertext.split(" ")
    if hash == machd(key=key, content=ciphertext):
        ciphertext = AESCipherCBCnoHASH(key=key).decrypt(ciphertext)
        try:
            return jl(ciphertext)
        except:
            return pickle.loads(ciphertext)
    else:
        raise Exception("current connection might be spoofed due to different hmac.")




