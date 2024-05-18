from pyftpdlib.handlers import RetryError, _FileReadWriteError, logger
from ssl import SSLSocket as _SSLSocket, SSLError
from pyftpdlib.servers import ThreadedFTPServer
from omnitools.xpip import REQUIRE
from ftplib import Error, B_CRLF
from omnitools import randstr
import pyftpdlib.authorizers
import pyftpdlib.handlers
import ftplib
import socket
# type hints
from omnitools.xtype import *


class FTPMS_Exception(Exception):
    pass


class FTP_ThrottledDTPHandler(pyftpdlib.handlers.ThrottledDTPHandler):
    transfer_limit = 10*1024*1024

    def alter_send(self, data: bytes):
        return data

    def alter_recv(self, chunk: bytes):
        return chunk

    def send(self, data):
        if self.file_obj and self.file_obj.name:
            data = self.alter_send(data)
        return super().send(data)

    def handle_read(self):
        try:
            chunk = self.recv(self.ac_in_buffer_size)
            if chunk:
                try:
                    chunk = self.alter_recv(chunk)
                    if not chunk:
                        raise ValueError
                except ValueError:
                    return self.close()
                except FTPMS_Exception:
                    return self.close()
        except RetryError:
            pass
        except socket.error:
            self.handle_error()
        else:
            self.tot_bytes_received += len(chunk)
            if not chunk:
                self.transfer_finished = True
                return
            if self._data_wrapper is not None:
                chunk = self._data_wrapper(chunk)
            try:
                self.file_obj.write(chunk)
            except OSError as err:
                raise _FileReadWriteError(err)

    handle_read_event = handle_read


def FTP_ThrottledDTPHandler_wrapper(dtp_handler: Type[FTP_ThrottledDTPHandler]):
    class FTP_ThrottledDTPHandler_tmp(dtp_handler):
        clients_transferring = []

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.transfer_id = [id(self), self.cmd_channel.username]
            FTP_ThrottledDTPHandler_tmp.clients_transferring.append(self.transfer_id)

        def handle_read(self):
            super().handle_read()
            if self.transfer_finished:
                FTP_ThrottledDTPHandler_tmp.clients_transferring.remove(self.transfer_id)

    return FTP_ThrottledDTPHandler_tmp


class FTPS_Base:
    handler = None
    server = None
    s = None

    def __init__(self, host: str = "127.0.0.1", port: int = 8021):
        if type(self) is FTPS_Base:
            raise NotImplementedError
        self.host = host
        self.port = port
        self.server = type("ThreadedFTPServer_"+randstr(16), (ThreadedFTPServer,), {})

    def configure(self):
        self.s = self.server((self.host, self.port), self.handler)

    def start(self):
        self.s.serve_forever()

    def __del__(self):
        self.stop()

    def stop(self):
        self.s.close()
        self.s.close_all()

    def safe_stop(self):
        self.s.close_when_done()
        self.s.close_all()


class FTPS(FTPS_Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = type("FTP_FTPHandler", (pyftpdlib.handlers.FTPHandler,), dict(
            authorizer=(type("FTP_DummyAuthorizer", (pyftpdlib.authorizers.DummyAuthorizer,), {}))(),
            dtp_handler=FTP_ThrottledDTPHandler_wrapper(FTP_ThrottledDTPHandler),
        ))
        self.handler.passive_ports = range(50100, 51100)


class FTPC_Base(ftplib.FTP):
    trust_server_pasv_ipv4_address = True

    def __init__(self, *args, unwrap_sslsocket_after_completed_transfer: bool = True, **kwargs):
        self.unwrap_sslsocket_after_completed_transfer = unwrap_sslsocket_after_completed_transfer
        super().__init__(*args, **kwargs)

    def storlines(self, cmd, fp, callback=None):
        self.voidcmd('TYPE A')
        with self.transfercmd(cmd) as conn:
            while 1:
                buf = fp.readline(self.maxline + 1)
                if len(buf) > self.maxline:
                    raise Error("got more than %d bytes" % self.maxline)
                if not buf:
                    break
                if buf[-2:] != B_CRLF:
                    if buf[-1] in B_CRLF: buf = buf[:-1]
                    buf = buf + B_CRLF
                try:
                    conn.sendall(buf)
                except SSLError:
                    pass
                except ConnectionResetError:
                    pass
                if callback:
                    callback(buf)
            if self.unwrap_sslsocket_after_completed_transfer:
                try:
                    if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                        conn.unwrap()
                except SSLError:
                    pass
                except ConnectionResetError:
                    pass
                except FileNotFoundError:
                    pass
        return self.voidresp()

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        with self.transfercmd(cmd, rest) as conn:
            while 1:
                buf = fp.read(blocksize)
                if not buf:
                    break
                try:
                    conn.sendall(buf)
                except SSLError:
                    pass
                except ConnectionResetError:
                    pass
                if callback:
                    callback(buf)
            if self.unwrap_sslsocket_after_completed_transfer:
                try:
                    if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                        conn.unwrap()
                except SSLError:
                    pass
                except ConnectionResetError:
                    pass
                except FileNotFoundError:
                    pass
        return self.voidresp()

    def retrbinary(self, cmd, callback, blocksize=8192, rest=None):
        if not callable(callback):
            if isinstance(callback, str):
                pass
            def _callback(x):
                pass
        else:
            _callback = callback
        super().retrbinary(cmd, _callback, blocksize, rest)


class FTPESC(FTPC_Base, ftplib.FTP_TLS):
    pass


class FTPSC(FTPC_Base, ftplib.FTP_TLS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sock = None

    @property
    def sock(self):
        return self._sock

    @sock.setter
    def sock(self, value):
        if value is not None and not isinstance(value, _SSLSocket):
            value = self.context.wrap_socket(value)
        self._sock = value

    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        conn = self.sock.context.wrap_socket(
            conn, server_hostname=self.host, session=self.sock.session
        )
        return conn, size


class FTPC(FTPC_Base):
    pass


if REQUIRE("pyopenssl"):
    class FTPS_ThrottledDTPHandler(FTP_ThrottledDTPHandler, pyftpdlib.handlers.TLS_DTPHandler):
        pass


    class FTPESS(FTPS_Base):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.handler = type("FTPES_TLS_FTPHandler", (pyftpdlib.handlers.TLS_FTPHandler,), dict(
                authorizer=(type("FTPES_DummyAuthorizer", (pyftpdlib.authorizers.DummyAuthorizer,), {}))(),
                dtp_handler=FTP_ThrottledDTPHandler_wrapper(FTPS_ThrottledDTPHandler),
            ))
            self.handler.passive_ports = range(50100, 51100)

