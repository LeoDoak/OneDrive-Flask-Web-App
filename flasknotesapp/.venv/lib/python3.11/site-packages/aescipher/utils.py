from omnitools import try_utf8e
from .ctr import AESCipherCTR


class AESCipherCTRFileBase:
    def __init__(self, *, fp: str, mode: str = "a", buffer: int = 8192, cb_before= None, cb_after = None, **kwargs):
        if type(self) is AESCipherCTRFileBase:
            raise NotImplementedError
        if isinstance(fp, str):
            self.fp = fp
            self.fo = open(fp, mode+"+b", buffer)
            self.name = self.fo.name
        else:
            self.fo = fp
            try:
                self.name = self.fo.name
                self.fp = self.fo.name
            except AttributeError:
                self.name = "cannot parse filename from {}".format(self.fo)
                self.fp = "cannot parse file path from {}".format(self.fo)
        self.cb_before = cb_before
        self.cb_after = cb_after
        self._cipher = lambda: AESCipherCTR(**kwargs)
        self.cipher = self._cipher()
        self.seek(0)

    def crypto(self, buf: bytes) -> bytes:
        raise NotImplementedError

    def cb_wrapper(self, buf: bytes) -> bytes:
        if buf:
            if self.cb_before:
                self.cb_before(buf)
            buf = try_utf8e(self.crypto(buf))
            if self.cb_after:
                self.cb_after(buf)
        return buf

    def _seek(self, n: int) -> int:
        return self.fo.seek(n)

    def _read(self, n: int = -1) -> bytes:
        return self.fo.read(n)

    def _write(self, s: bytes) -> int:
        return self.fo.write(s)

    def seek(self, n: int) -> int:
        raise NotImplementedError

    def read(self, n: int = -1) -> bytes:
        raise NotImplementedError

    def write(self, s: bytes) -> int:
        raise NotImplementedError

    def close(self):
        return self.fo.close()

    def tell(self):
        return self.fo.tell()

    def __del__(self):
        self.close()


class AESCipherCTRFileReader(AESCipherCTRFileBase):
    def __init__(self, *args, **kwargs):
        if type(self) is AESCipherCTRFileReader:
            raise NotImplementedError
        super().__init__(*args, **kwargs)

    def read(self, n: int = -1) -> bytes:
        return self.cb_wrapper(self._read(n))

    def seek(self, n: int) -> int:
        self.cipher = self._cipher()
        for i in range(0, n):
            self.cipher.decrypt(b"\x00")
        return self._seek(n)


class AESCipherCTRFileWriter(AESCipherCTRFileBase):
    def __init__(self, *args, **kwargs):
        if type(self) is AESCipherCTRFileWriter:
            raise NotImplementedError
        super().__init__(*args, mode="w", **kwargs)

    def write(self, s: bytes) -> int:
        return self.fo.write(self.cb_wrapper(s))


class AESCipherCTRFileEnc(AESCipherCTRFileBase):
    def __init__(self, *args, **kwargs):
        if type(self) is AESCipherCTRFileEnc:
            raise NotImplementedError
        super().__init__(*args, **kwargs)

    def seek(self, n: int) -> int:
        try:
            _ = super().seek(n)
        except NotImplementedError:
            _ = -1
        self.crypto = self.cipher.encrypt
        return _


class AESCipherCTRFileDec(AESCipherCTRFileBase):
    def __init__(self, *args, **kwargs):
        if type(self) is AESCipherCTRFileDec:
            raise NotImplementedError
        super().__init__(*args, **kwargs)

    def seek(self, n: int) -> int:
        try:
            _ = super().seek(n)
        except NotImplementedError:
            _ = -1
        self.crypto = self.cipher.decrypt
        return _


class AESCipherCTRFileEncReader(AESCipherCTRFileEnc, AESCipherCTRFileReader):
    pass


class AESCipherCTRFileEncWriter(AESCipherCTRFileEnc, AESCipherCTRFileWriter):
    pass


class AESCipherCTRFileDecReader(AESCipherCTRFileDec, AESCipherCTRFileReader):
    pass


class AESCipherCTRFileDecWriter(AESCipherCTRFileDec, AESCipherCTRFileWriter):
    pass




