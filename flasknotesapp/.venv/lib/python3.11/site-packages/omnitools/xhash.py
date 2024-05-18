from .xsys.pyver import PYTHON3_6
from hashlib import sha1, md5, sha512, sha384, sha256, sha224
if PYTHON3_6:
    from hashlib import sha3_512, sha3_384, sha3_256, sha3_224
else:
    sha3_512 = sha512
    sha3_384 = sha384
    sha3_256 = sha256
    sha3_224 = sha224
from zlib import crc32
import hmac
from .xtype import str_or_bytes
from .xencode import try_utf8e


def MACwoHASH(key: str_or_bytes, content: str_or_bytes, method=sha3_512) -> hmac.HMAC:
    return hmac.new(try_utf8e(key), try_utf8e(content), method)


def MACwHASH(key: str_or_bytes, content: str_or_bytes, method=sha3_512) -> hmac.HMAC:
    return hmac.new(method(key).digest(), try_utf8e(content), method)


def machd(*args, **kwargs) -> str:
    return MACwoHASH(*args, **kwargs).hexdigest()


def macd(*args, **kwargs) -> bytes:
    return MACwoHASH(*args, **kwargs).digest()


def macHhd(*args, **kwargs) -> str:
    return MACwHASH(*args, **kwargs).hexdigest()


def macHd(*args, **kwargs) -> bytes:
    return MACwHASH(*args, **kwargs).digest()


def _crc32d_update(_input, d: int = 0) -> int:
    if hasattr(_input, "seek") and hasattr(_input, "read"):
        _input.seek(0)
        while True:
            data = _input.read(1024*8)
            if not data:
                break
            d = crc32(data, d)
        _input.seek(0)
    elif isinstance(_input, (str, bytes)):
        d = crc32(try_utf8e(_input), d)
    else:
        raise Exception("input type {} not implemented".format(type(_input)))
    return d


def crc32hd(_input, d: int = 0) -> str:
    return format(_crc32d_update(_input, d), "x").zfill(8)


def crc32d(_input, d: int = 0) -> bytes:
    return _crc32d_update(_input, d).to_bytes(4, byteorder="big")


def _hash_d_update(_input, d):
    if hasattr(_input, "seek") and hasattr(_input, "read"):
        _input.seek(0)
        while True:
            data = _input.read(1024*8)
            if not data:
                break
            d.update(data)
        _input.seek(0)
    elif isinstance(_input, (str, bytes)):
        d.update(try_utf8e(_input))
    else:
        raise Exception("input type {} not implemented".format(type(_input)))
    return d


def _hexdigest(_input, d) -> str:
    d = _hash_d_update(_input, d)
    return d.hexdigest()


def _digest(_input, d) -> bytes:
    d = _hash_d_update(_input, d)
    return d.digest()


def md5hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, md5(*args, **kwargs))


def sha1hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha1(*args, **kwargs))


def sha3_224hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha3_224(*args, **kwargs))


def sha3_256hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha3_256(*args, **kwargs))


def sha3_384hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha3_384(*args, **kwargs))


def sha3_512hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha3_512(*args, **kwargs))


def sha224hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha224(*args, **kwargs))


def sha256hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha256(*args, **kwargs))


def sha384hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha384(*args, **kwargs))


def sha512hd(_input, *args, **kwargs) -> str:
    return _hexdigest(_input, sha512(*args, **kwargs))


def md5d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, md5(*args, **kwargs))


def sha1d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha1(*args, **kwargs))


def sha3_224d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha3_224(*args, **kwargs))


def sha3_256d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha3_256(*args, **kwargs))


def sha3_384d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha3_384(*args, **kwargs))


def sha3_512d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha3_512(*args, **kwargs))


def sha224d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha224(*args, **kwargs))


def sha256d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha256(*args, **kwargs))


def sha384d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha384(*args, **kwargs))


def sha512d(_input, *args, **kwargs) -> bytes:
    return _digest(_input, sha512(*args, **kwargs))


if PYTHON3_6:
    from hashlib import blake2b


    def blake2bhd(_input, *args, **kwargs) -> str:
        return _hexdigest(_input, blake2b(*args, **kwargs))


    def blake2bd(_input, *args, **kwargs) -> bytes:
        return _digest(_input, blake2b(*args, **kwargs))

