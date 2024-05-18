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


