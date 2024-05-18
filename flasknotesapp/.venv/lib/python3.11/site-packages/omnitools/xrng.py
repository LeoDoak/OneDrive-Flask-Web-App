import os
import random
import string


__ALL__ = ["randb", "randi", "randstr"]


def randb(size=64):
    return os.urandom(size)


def randi(power: int = 6) -> int:
    power = int(power)
    return random.randint(10 ** power, 10 ** (power + 1) - 1)


def randstr(length: int, extra_str: str = "") -> str:
    return "".join(random.SystemRandom().choice(string.ascii_letters+string.digits+extra_str) for _ in range(length))
