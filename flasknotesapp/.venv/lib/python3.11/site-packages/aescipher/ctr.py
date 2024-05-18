from Crypto.Cipher import AES
from Crypto.Util import Counter
from omnitools import sha3_256d, str_or_bytes, try_utf8e, try_utf8d


class AESCipherCTR_Base:
    mode: str = None
    _cipher = None

    def encrypt(self, raw: str_or_bytes) -> bytes:
        mode = "encryption"
        if not self.mode:
            self.mode = mode
        elif self.mode != mode:
            raise Exception("this cipher is currently in '{}' mode. create a new object instead.".format(self.mode))
        return self._cipher.encrypt(try_utf8e(raw))

    def decrypt(self, raw: bytes) -> str_or_bytes:
        mode = "decryption"
        if not self.mode:
            self.mode = mode
        elif self.mode != mode:
            raise Exception("this cipher is currently in '{}' mode. create a new object instead.".format(self.mode))
        return try_utf8d(self._cipher.decrypt(raw))

    def __del__(self):
        self.destroy()

    def destroy(self):
        self._cipher = None


class AESCipherCTR(AESCipherCTR_Base):
    def __init__(self, *, key: str_or_bytes, iv: bytes = b"\x00"*8, initial_value: int = 1):
        self._cipher = AES.new(key=sha3_256d(key), mode=AES.MODE_CTR, counter=Counter.new(nbits=64, prefix=iv, initial_value=initial_value))


class AESCipherCTRnoIV(AESCipherCTR_Base):
    def __init__(self, *, key: str_or_bytes):
        self._cipher = AES.new(key=sha3_256d(key), mode=AES.MODE_CTR, counter=Counter.new(nbits=64, prefix=b"\x00"*8))


class AESCipherCTRnoHASH(AESCipherCTR_Base):
    def __init__(self, *, key: bytes, iv: bytes = b"\x00"*8, initial_value: int = 1):
        self._cipher = AES.new(key=key, mode=AES.MODE_CTR, counter=Counter.new(nbits=64, prefix=iv, initial_value=initial_value))


class AESCipherCTRnoHASHnoIV(AESCipherCTR_Base):
    def __init__(self, *, key: bytes):
        self._cipher = AES.new(key=key, mode=AES.MODE_CTR, counter=Counter.new(nbits=64, prefix=b"\x00"*8))



