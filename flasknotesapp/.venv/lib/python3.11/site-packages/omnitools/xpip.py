from subprocess import Popen
import importlib


def pip(*args, dry_run: bool = False, **kwargs):
    args = ["python3", "-m", "pip", *args]
    cmd = " ".join(args)
    if dry_run:
        return cmd
    else:
        print(cmd)
    return Popen(args).communicate()


def install(*args, **kwargs):
    return pip("install", *args, **kwargs)


def REQUIRE(pkg_name):
    pkgs = {
        "pyopenssl": "OpenSSL",
        "megadownloader": "megadownloader",
    }
    try:
        return importlib.import_module(pkgs[pkg_name.lower()])
    except KeyError:
        raise KeyError
    except ImportError:
        return False


def upgrade(quiet: bool = False, dry_run: bool = False):
    pkgs = [
        "omnitools",
        "sneaky",
        "vpncmd",
        "zippyshare",
        "userscloud",
        "sqlq",
        "text2png",
        "dwa",
        "pythoncgi",
        "aceditor",
        "credsafe",
        "threadwrapper",
        "easyrsa",
        "aescipher",
        "telewrapper",
        "encryptedsocket",
        "unencryptedsocket",
        "delugerpc",
        "aria2rpc",
    ]
    [print(i, pkgs[i]) for i in range(0, len(pkgs))]
    print(len(pkgs), "ALL")
    i = input("Enter i: ")
    if i.isdigit():
        i = int(i)
        if i >= 0 and i <= len(pkgs):
            if i == len(pkgs):
                pkg = pkgs
            else:
                pkg = [pkgs[i]]
            if quiet:
                pkg.insert(0, "--quiet")
            o = install(
                "-U",
                "--no-cache-dir",
                *pkg,
                dry_run=dry_run
            )
            if dry_run:
                print(o)


def uninstall(*args, **kwargs):
    return pip("uninstall", *args, **kwargs)


def download(*args, **kwargs):
    return pip("download", *args, **kwargs)


def freeze(*args, **kwargs):
    return pip("freeze", *args, **kwargs)


def list(*args, **kwargs):
    return pip("list", *args, **kwargs)


def show(*args, **kwargs):
    return pip("show", *args, **kwargs)


def check(*args, **kwargs):
    return pip("check", *args, **kwargs)


def config(*args, **kwargs):
    return pip("config", *args, **kwargs)


def search(*args, **kwargs):
    return pip("search", *args, **kwargs)


def cache(*args, **kwargs):
    return pip("cache", *args, **kwargs)


def index(*args, **kwargs):
    return pip("index", *args, **kwargs)


def wheel(*args, **kwargs):
    return pip("wheel", *args, **kwargs)


def hash(*args, **kwargs):
    return pip("hash", *args, **kwargs)


def completion(*args, **kwargs):
    return pip("completion", *args, **kwargs)


def debug(*args, **kwargs):
    return pip("debug", *args, **kwargs)


def help(*args, **kwargs):
    return pip("help", *args, **kwargs)


