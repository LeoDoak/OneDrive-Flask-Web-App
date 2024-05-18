from omnitools import str_or_bytes, b64e, b64d, try_utf8d, try_utf8e, jl, jd_and_utf8e, utf8d
from Crypto.Signature import PKCS1_v1_5, PKCS1_PSS
from Crypto.Hash import SHA3_512, SHA3_384
from Crypto.Cipher import PKCS1_OAEP
from .utils import CertificateBase
from Crypto.PublicKey import RSA
from OpenSSL.crypto import (
    PKey, X509, X509Extension,
    X509Store, X509StoreContext, load_certificate,
    TYPE_DSA, TYPE_RSA,
    FILETYPE_PEM, FILETYPE_ASN1, FILETYPE_TEXT,
    dump_certificate, dump_privatekey
)
import random


class EasyRSA(object):
    def __init__(
            self, *, bits: int = None,
            public_key: str_or_bytes = None,
            private_key: str_or_bytes = None
    ) -> None:
        if not (
                (public_key is None and private_key is None and bits is not None) or
                (bits is None and private_key is None and public_key is not None) or
                (public_key is None and bits is None and private_key is not None)
        ):
            raise Exception("only one operation per instance is allowed")
        self.__key = bits
        self.__public_key = public_key
        self.__private_key = private_key
        if isinstance(self.__public_key, str):
            self.__public_key = b64d(self.__public_key)
        if isinstance(self.__private_key, str):
            self.__private_key = b64d(self.__private_key)

    def gen_key_pair(self):
        key = RSA.generate(bits=self.__key)
        try:
            return dict(
                private_key=key.export_key(),
                public_key=key.public_key().export_key()
            )
        except Exception as e:
            raise e
        finally:
            self.__key = None

    def max_msg_size(self) -> int:
        try:
            if self.__public_key:
                return RSA.import_key(extern_key=self.__public_key).n.bit_length() // 8 - 42
            elif self.__private_key:
                return RSA.import_key(extern_key=self.__private_key).n.bit_length() // 8 - 42
        except Exception as e:
            raise e
        finally:
            self.__private_key = None
            self.__public_key = None

    def encrypt(self, v: str_or_bytes) -> bytes:
        if len(try_utf8e(v)) > EasyRSA(public_key=self.__public_key).max_msg_size():
            return self.encryptlong(v)
        v = try_utf8e(v)
        return PKCS1_OAEP.new(key=RSA.import_key(extern_key=self.__public_key)).encrypt(v)

    def encryptlong(self, v: str_or_bytes) -> bytes:
        max_msg_size = EasyRSA(public_key=self.__public_key).max_msg_size()
        parts = []
        while v:
            parts.append(b64e(self.encrypt(v[:max_msg_size])))
            v = v[max_msg_size:]
        return jd_and_utf8e(parts)

    def decrypt(self, v: bytes) -> str_or_bytes:
        try:
            return self.decryptlong(jl(utf8d(v)))
        except:
            pass
        v = PKCS1_OAEP.new(key=RSA.import_key(extern_key=self.__private_key)).decrypt(v)
        return try_utf8d(v)

    def decryptlong(self, parts: list) -> str_or_bytes:
        v = []
        for part in parts:
            v.append(self.decrypt(b64d(part)))
        if isinstance(v[0], str):
            return "".join(v)
        else:
            return b"".join(v)

    def sign(self, msg: str_or_bytes) -> bytes:
        return PKCS1_PSS.new(rsa_key=RSA.import_key(extern_key=self.__private_key)).sign(SHA3_384.new(try_utf8e(msg)))

    def verify(self, msg: str_or_bytes, sig: bytes) -> bool:
        PKCS1_PSS.new(rsa_key=RSA.importKey(self.__public_key).publickey()).verify(SHA3_384.new(try_utf8e(msg)), sig)
        return True


class Certificate(CertificateBase):
    def __init__(
            self, *,
            file_type: int = FILETYPE_PEM,
            private_key_type: int = TYPE_RSA, private_key_bits: int = 2048, valid_duration: int = 10,
            x509_serial_no: int = random.SystemRandom().randint(2**64, 2**128), x509_version: int = 2
    ):
        super().__init__()
        self.key = PKey()
        self.key.generate_key(private_key_type, private_key_bits)
        self.certificate.set_serial_number(x509_serial_no)
        self.certificate.set_version(x509_version)
        self.subject = self.certificate.get_subject()
        self.file_type = file_type
        self.certificate.set_pubkey(self.key)
        self.certificate.gmtime_adj_notBefore(0)
        self.certificate.gmtime_adj_notAfter(int(valid_duration * (1 * 365 * 24 * 60 * 60)))

    def dump(self, filename: str = None, merge: bool = False):
        if not filename:
            filename = self.subject.commonName
        if merge:
            with open("{}.pem".format(filename), "wb") as fo:
                fo.write(dump_certificate(self.file_type, self.certificate))
                fo.write(dump_privatekey(self.file_type, self.key))
        else:
            with open("{}.crt".format(filename), "wb") as fo:
                fo.write(dump_certificate(self.file_type, self.certificate))
            with open("{}.key".format(filename), "wb") as fo:
                fo.write(dump_privatekey(self.file_type, self.key))


class CertificateAuthority(CertificateBase):
    def __init__(
            self, *,
            file_type: int = FILETYPE_PEM,
            private_key_type: int = TYPE_RSA, private_key_bits: int = 2048, valid_duration: int = 10,
            x509_serial_no: int = random.SystemRandom().randint(2**64, 2**128), x509_version: int = 2
    ):
        super().__init__()
        self.key = PKey()
        self.key.generate_key(private_key_type, private_key_bits)
        self.certificate.set_serial_number(x509_serial_no)
        self.certificate.set_version(x509_version)
        self.basicConstraints(False, b"CA:TRUE")
        self.keyUsage(False, b"keyCertSign, cRLSign")
        self.subject = self.certificate.get_subject()
        self.file_type = file_type
        self.certificate.set_pubkey(self.key)
        self.certificate.gmtime_adj_notBefore(0)
        self.certificate.gmtime_adj_notAfter(int(valid_duration * (1 * 365 * 24 * 60 * 60)))

    def sign(self, digest: str = "sha256") -> "CertificateAuthority":
        self.subjectKeyIdentifier(False, b"hash", subject=self.certificate)
        self.authorityKeyIdentifier(False, b"keyid:always", issuer=self.certificate)
        self.certificate.set_issuer(self.subject)
        self.certificate.sign(self.key, digest)
        return self

    def dump(self, filename: str = None, merge: bool = False):
        if not filename:
            filename = self.subject.commonName
        if merge:
            with open("ca_{}.pem".format(filename), "wb") as fo:
                fo.write(dump_certificate(self.file_type, self.certificate))
                fo.write(dump_privatekey(self.file_type, self.key))
        else:
            with open("ca_{}.crt".format(filename), "wb") as fo:
                fo.write(dump_certificate(self.file_type, self.certificate))
            with open("ca_{}.key".format(filename), "wb") as fo:
                fo.write(dump_privatekey(self.file_type, self.key))

    def sign_certificate(self, certificate: Certificate, digest: str = "sha256") -> "Certificate":
        certificate.basicConstraints(False, b"CA:FALSE")
        certificate.subjectKeyIdentifier(False, b"hash", subject=certificate.certificate)
        certificate.authorityKeyIdentifier(False, b"keyid:always", issuer=self.certificate)
        certificate.extendedKeyUsage(False, b"clientAuth")
        certificate.keyUsage(False, b"digitalSignature")
        certificate.certificate.set_issuer(self.subject)
        certificate.certificate.sign(self.key, digest)
        return certificate

    def verify_certificate(self, certificate: Certificate) -> bool:
        ca_store = X509Store()
        ca_store.add_cert(self.certificate)
        X509StoreContext(ca_store, certificate.certificate).verify_certificate()
        return True

    def verify_certificate_from_raw(self, fp, file_type: int = FILETYPE_PEM) -> bool:
        if not isinstance(self, CertificateAuthority):
            fp0 = self
            if isinstance(fp0, str):
                ca_certificate = load_certificate(file_type, open(fp0, "rb").read())
            elif isinstance(fp0, bytes):
                ca_certificate = load_certificate(file_type, fp0)
            else:
                ca_certificate = load_certificate(file_type, fp0.read())
        else:
            ca_certificate = self.certificate
        if isinstance(fp, str):
            certificate = load_certificate(file_type, open(fp, "rb").read())
        elif isinstance(fp, bytes):
            certificate = load_certificate(file_type, fp)
        else:
            certificate = load_certificate(file_type, fp.read())
        ca_store = X509Store()
        ca_store.add_cert(ca_certificate)
        X509StoreContext(ca_store, certificate).verify_certificate()
        return True


class EasyRSAv1(EasyRSA):
    def sign(self, msg: str_or_bytes) -> bytes:
        return PKCS1_v1_5.new(rsa_key=RSA.import_key(extern_key=self.__private_key)).sign(SHA3_512.new(try_utf8e(msg)))

    def verify(self, msg: str_or_bytes, sig: bytes) -> bool:
        PKCS1_v1_5.new(rsa_key=RSA.importKey(self.__public_key).publickey()).verify(msg_hash=SHA3_512.new(try_utf8e(msg)), signature=sig)
        return True


