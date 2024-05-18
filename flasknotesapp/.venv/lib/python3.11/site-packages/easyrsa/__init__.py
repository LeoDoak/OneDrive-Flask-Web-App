__version__ = "3.1.0"
__keywords__ = ["easy rsa public private key sign verify trusted root certificate authority x509 pkcs1 oaep pss ssl"]


if not __version__.endswith(".0"):
    import re
    print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
    print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
    import os
    os._exit(1)


from .core import *

