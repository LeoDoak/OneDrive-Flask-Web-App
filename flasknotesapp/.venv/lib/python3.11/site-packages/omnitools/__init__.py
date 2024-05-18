__version__ = "0.0.268"
__keywords__ = ["omnitools python utilities shortcuts misc"]


# if not __version__.endswith(".0"):
#     import re
#     print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
#     print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
#     import os
#     os._exit(1)


from .xdecorator import *
from .xstdin import *
from .xstdout import *
from .xtype import *
from .xencode import *
from .xhash import *
from .xrng import *
from .xjs import *
from .xinspect import *
from .xtrace import *
from .xmisc import *
from .ximage import *
from .xmask import *
from .xdatetime import *
from .xdebug import *
from .xhtml import *
from .xfile import *
from .xos import *
from .xpip import *
from .xftp import *

