import re
import math


def mask(string: str, coverage: float = 0.5):
    if re.search(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$", string):
        string = string.split("@")
        masked = mask(string[0])+"@"+string[1]
    else:
        length = len(string)
        i = math.ceil(length*coverage)
        masked = string[:i]+"*"*(length-i)
    return masked


