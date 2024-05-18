import queue
import traceback
import threading
from .path import *
from ..xtype import str_or_bytes, key_pair_format
from ..xencode import utf8d, charenc
from ..xstdout import p
from ..xmisc import args
from easyrsa import *


__ALL__ = ["file_size", "read", "write", "WriterE", "WriterU"]


def file_size(path: str) -> int:
    if os.path.isdir(path):
        total_size = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size
    elif os.path.isfile(path):
        return os.path.getsize(path)
    else:
        raise


def read(file_path: str, encoding: str = None) -> str_or_bytes:
    if encoding:
        try:
            return open(file_path, "rb").read().decode(encoding=encoding)
        except UnicodeDecodeError:
            raise Exception("failed to readfile {} with encoding {}.".format(file_path, encoding))
    else:
        content = open(file_path, "rb").read()
        try:
            return utf8d(content)
        except UnicodeDecodeError:
            try:
                return content.decode(encoding=charenc(content))
            except UnicodeDecodeError:
                return content


class Writer:
    def worker(self) -> None:
        while not self.terminate:
            file_path, mode, content = self.fileq.get()
            if not os.path.isdir(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            if not os.path.isfile(file_path):
                open(file_path, "ab").close()
            try:
                fo = open(file_path, mode)
                fo.write(content)
                fo.flush()
                fo.close()
            except Exception as e:
                what = content
                p("cannot write {} to file {} using mode {} due to {}".format(what, file_path, mode, e))
                traceback.print_exc()
            self.fileq.task_done()

    def stop(self) -> None:
        self.terminate = True

    def __init__(self, server: bool = False) -> None:
        self.terminate = False
        self.fileq = None
        self.fileq_worker = None
        self.functions = None
        self.is_server = server
        self.sc = None
        if self.is_server:
            self.fileq = queue.Queue()
            self.fileq_worker = threading.Thread(target=self.worker)
            self.fileq_worker.daemon = True
            self.fileq_worker.start()
            self.functions = dict(write=self.fileq.put)

    def write(self, file_path: str, mode: str, content: str_or_bytes) -> bool:
        if mode not in ("w", "a", "wb", "ab"):
            raise Exception("mode {} is not 'w' or 'a' or 'wb' or 'ab'.".format(mode))
        if mode in ("w", "a") and isinstance(content, bytes):
            raise Exception("mode {} cannot write bytes".format(mode))
        if mode in ("wb", "ab") and isinstance(content, str):
            raise Exception("mode {} cannot write str".format(mode))
        _args = (file_path, mode, content)
        if self.is_server:
            self.fileq.put(_args)
        else:
            try:
                self.sc.request(command="write", data=args(_args))
            except ConnectionRefusedError:
                open(file_path, mode).write(content)
        return True


class WriterE(Writer):
    def __init__(self, host = "127.199.71.10", writer_port: int = None, key_pair: key_pair_format = None, **kwargs) -> None:
        super().__init__(**kwargs)
        port = writer_port if writer_port else 39293
        from encryptedsocket import SC, SS
        if self.is_server:
            if key_pair is None:
                key_pair = EasyRSA(bits=1024).gen_key_pair()
            self.ess = SS(key_pair=key_pair, functions=self.functions, host=host, port=port, silent=True)
            thread = threading.Thread(target=self.ess.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = SC(host=host, port=port)

    def stop(self):
        super().stop()
        self.ess.stop()


class WriterU(Writer):
    def __init__(self, host = "127.199.71.10", writer_port: int = None, **kwargs) -> None:
        super().__init__(**kwargs)
        port = writer_port if writer_port else 39293
        from unencryptedsocket import SC, SS
        if self.is_server:
            self.uss = SS(functions=self.functions, host=host, port=port, silent=True)
            thread = threading.Thread(target=self.uss.start)
            thread.daemon = True
            thread.start()
        else:
            self.sc = SC(host=host, port=port)

    def stop(self):
        super().stop()
        self.uss.stop()


