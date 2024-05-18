from omnitools import sha3_256d, str_or_bytes, b64e, b64d, try_utf8e, try_utf8d
from Crypto.Cipher import AES
from Crypto import Random


class AESCipherGCM_Base:
    _cipher = None

    def __del__(self):
        self.destroy()

    def destroy(self):
        self._cipher = None

    def encrypt(self, raw: str_or_bytes) -> str:
        raise Exception("use encrypt_and_digest instead")

    def decrypt(self, enc: str) -> str_or_bytes:
        raise Exception("use decrypt_and_verify instead")

    def digest(self) -> bytes:
        raise NotImplementedError

    def verify(self, mac: bytes) -> None:
        raise NotImplementedError

    def encrypt_and_digest(self, raw: str_or_bytes) -> tuple:
        raise NotImplementedError

    def decrypt_and_verify(self, enc: str, mac: bytes) -> str_or_bytes:
        raise NotImplementedError


class AESCipherGCMwIV_Base(AESCipherGCM_Base):
    def encrypt_and_digest(self, raw: str_or_bytes) -> tuple:
        raw = try_utf8e(raw)
        iv = Random.new().read(AES.block_size)
        _ = self._cipher(iv)
        return b64e(iv + _.encrypt(raw)), _.digest()

    def decrypt_and_verify(self, enc: str, mac: bytes) -> str_or_bytes:
        enc = b64d(enc)
        iv = enc[:AES.block_size]
        _ = self._cipher(iv)
        __ = _.decrypt(enc[AES.block_size:])
        _.verify(mac)
        return try_utf8d(__)


class AESCipherGCMwoIV_Base(AESCipherGCM_Base):
    def encrypt_and_digest(self, raw: str_or_bytes) -> tuple:
        raw = try_utf8e(raw)
        _ = self._cipher()
        return b64e(_.encrypt(raw)), _.digest()

    def decrypt_and_verify(self, enc: str, mac: bytes) -> str_or_bytes:
        enc = b64d(enc)
        _ = self._cipher()
        __ = _.decrypt(enc)
        _.verify(mac)
        return try_utf8d(__)


class AESCipherGCM(AESCipherGCMwIV_Base):
    def __init__(self, *, key: str_or_bytes, assoc_data: bytes) -> None:
        self._cipher = lambda iv: AES.new(key=sha3_256d(key), mode=AES.MODE_GCM, nonce=iv).update(assoc_data)


class AESCipherGCMnoHASH(AESCipherGCMwIV_Base):
    def __init__(self, *, key: bytes, assoc_data: bytes) -> None:
        self._cipher = lambda iv: AES.new(key=key, mode=AES.MODE_GCM, nonce=iv).update(assoc_data)


class AESCipherGCMwoIV(AESCipherGCMwoIV_Base):
    def __init__(self, *, key: str_or_bytes, iv: bytes, assoc_data: bytes) -> None:
        self._cipher = lambda: AES.new(key=sha3_256d(key), mode=AES.MODE_GCM, nonce=iv).update(assoc_data)


class AESCipherGCMnoHASHwoIV(AESCipherGCMwoIV_Base):
    def __init__(self, *, key: bytes, iv: bytes, assoc_data: bytes) -> None:
        self._cipher = lambda: AES.new(key=key, mode=AES.MODE_GCM, nonce=iv).update(assoc_data)


class AESCipherGCMSTREAM_Base(AESCipherGCM_Base):
    def encrypt_and_digest(self, raw: str_or_bytes) -> tuple:
        raise NotImplementedError

    def decrypt_and_verify(self, enc: str, assoc_data: bytes) -> str_or_bytes:
        raise NotImplementedError

    def digest(self) -> bytes:
        return self._cipher.digest()

    def verify(self, mac: bytes) -> None:
        return self._cipher.verify(mac)

    def encrypt(self, raw: str_or_bytes) -> bytes:
        raw = try_utf8e(raw)
        return self._cipher.encrypt(raw)

    def decrypt(self, raw: bytes) -> str_or_bytes:
        return try_utf8d(self._cipher.decrypt(raw))


class AESCipherGCMSTREAM(AESCipherGCMSTREAM_Base, AESCipherGCM):
    _iv: bytes = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iv = Random.new().read(AES.block_size)
        self._cipher = self._cipher(self._iv)


class AESCipherGCMSTREAMnoHASH(AESCipherGCMSTREAM_Base, AESCipherGCMnoHASH):
    _iv: bytes = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iv = Random.new().read(AES.block_size)
        self._cipher = self._cipher(self._iv)


class AESCipherGCMSTREAMwoIV(AESCipherGCMSTREAM_Base, AESCipherGCMwoIV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cipher = self._cipher()


class AESCipherGCMSTREAMnoHASHwoIV(AESCipherGCMSTREAM_Base, AESCipherGCMnoHASHwoIV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cipher = self._cipher()



