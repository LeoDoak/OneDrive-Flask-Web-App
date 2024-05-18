__version__ = "6.0.0"
__keywords__ = ["aes cipher cbc ctr gcm stream block encrypt decrypt nonce iv file wrapper reader writer"]


if not __version__.endswith(".0"):
    import re
    print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
    print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
    import os
    os._exit(1)


from .cbc import AESCipherCBC, AESCipherCBCnoHASH, AESCipherCBCwoIV, AESCipherCBCnoHASHwoIV, AES, Random
from .ctr import AESCipherCTR, AESCipherCTRnoIV, AESCipherCTRnoHASH, AESCipherCTRnoHASHnoIV, Counter
from .gcm import AESCipherGCM, AESCipherGCMnoHASH, AESCipherGCMwoIV, AESCipherGCMnoHASHwoIV, AESCipherGCMSTREAM, AESCipherGCMSTREAMnoHASH, AESCipherGCMSTREAMwoIV, AESCipherGCMSTREAMnoHASHwoIV
from .utils import AESCipherCTRFileEncReader, AESCipherCTRFileEncWriter, AESCipherCTRFileDecReader, AESCipherCTRFileDecWriter

