from omnitools import sha3_256d, str_or_bytes, b64e, b64d, try_utf8e, try_utf8d
from Crypto.Cipher import AES
from Crypto import Random


def pad(s: str_or_bytes) -> str_or_bytes:
    gap = AES.block_size - len(s) % AES.block_size
    if isinstance(s, bytes):
        char = bytes([gap])
    else:
        char = chr(gap)
    s = s + char * gap
    return s


def unpad(s: str_or_bytes) -> str_or_bytes:
    s = s[:-ord(s[len(s) - 1:])]
    return s


class AESCipherCBC_Base:
    _cipher = None

    def __del__(self):
        self.destroy()

    def destroy(self):
        self._cipher = None


class AESCipherCBCwIV_Base(AESCipherCBC_Base):
    def encrypt(self, raw: str_or_bytes) -> str:
        raw = try_utf8e(pad(try_utf8e(raw)))
        iv = Random.new().read(AES.block_size)
        return b64e(iv + self._cipher(iv).encrypt(raw))

    def decrypt(self, enc: str) -> str_or_bytes:
        enc = b64d(enc)
        iv = enc[:AES.block_size]
        return try_utf8d(unpad(self._cipher(iv).decrypt(enc[AES.block_size:])))


class AESCipherCBCwoIV_Base(AESCipherCBC_Base):
    def encrypt(self, raw: str_or_bytes) -> str:
        raw = try_utf8e(pad(try_utf8e(raw)))
        return b64e(self._cipher().encrypt(raw))

    def decrypt(self, enc: str) -> str_or_bytes:
        enc = b64d(enc)
        return try_utf8d(unpad(self._cipher().decrypt(enc)))


class AESCipherCBC(AESCipherCBCwIV_Base):
    def __init__(self, *, key: str_or_bytes) -> None:
        self._cipher = lambda iv: AES.new(key=sha3_256d(key), mode=AES.MODE_CBC, iv=iv)


class AESCipherCBCnoHASH(AESCipherCBCwIV_Base):
    def __init__(self, *, key: bytes) -> None:
        self._cipher = lambda iv: AES.new(key=key, mode=AES.MODE_CBC, iv=iv)


class AESCipherCBCwoIV(AESCipherCBCwoIV_Base):
    def __init__(self, *, key: str_or_bytes, iv: bytes) -> None:
        self._cipher = lambda: AES.new(key=sha3_256d(key), mode=AES.MODE_CBC, iv=iv)


class AESCipherCBCnoHASHwoIV(AESCipherCBCwoIV_Base):
    def __init__(self, *, key: bytes, iv: bytes) -> None:
        self._cipher = lambda: AES.new(key=key, mode=AES.MODE_CBC, iv=iv)



