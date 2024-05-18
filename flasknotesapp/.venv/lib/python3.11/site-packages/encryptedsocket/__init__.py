__version__ = "3.0.0"
__keywords__ = ["encrypted rpc socket server client rsa aes"]


if not __version__.endswith(".0"):
    import re
    print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
    print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
    import os
    os._exit(1)


from .server import SS
from .client import SC, args


