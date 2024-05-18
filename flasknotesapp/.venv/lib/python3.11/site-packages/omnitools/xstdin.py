import sys
import string
from .xos import IS_WIN32


class _KEYS:
    A = b"A"
    B = b"B"
    C = b"C"
    D = b"D"
    E = b"E"
    F = b"F"
    G = b"G"
    H = b"H"
    I = b"I"
    J = b"J"
    K = b"K"
    L = b"L"
    M = b"M"
    N = b"N"
    O = b"O"
    P = b"P"
    Q = b"Q"
    R = b"R"
    S = b"S"
    T = b"T"
    U = b"U"
    V = b"V"
    W = b"W"
    Y = b"Y"
    X = b"X"
    Z = b"Z"
    a = b"a"
    b = b"b"
    c = b"c"
    d = b"d"
    e = b"e"
    f = b"f"
    g = b"g"
    h = b"h"
    i = b"i"
    j = b"j"
    k = b"k"
    l = b"l"
    m = b"m"
    n = b"n"
    o = b"o"
    p = b"p"
    q = b"q"
    r = b"r"
    s = b"s"
    t = b"t"
    u = b"u"
    v = b"v"
    w = b"w"
    y = b"y"
    x = b"x"
    z = b"z"
    SPACE = b" "
    BACKTICK = b"`"
    TILDE = b"~"
    _1 = b"1"
    NOT = b"!"
    _2 = b"2"
    AT = b"@"
    _3 = b"3"
    HASH = b"#"
    _4 = b"4"
    DOLLAR = "$"
    _5 = b"5"
    PERCENT = b"%"
    _6 = b"6"
    XOR = b"^"
    _7 = b"7"
    AND = b"&"
    _8 = b"8"
    ASTERISK = b"*"
    _9 = b"9"
    RBRACKET_L = b"("
    _0 = b"0"
    RBRACKET_R = b")"
    SUB = b"-"
    _ = b"_"
    EQ = b"="
    ADD = b"+"
    SBRACKET_L = b"["
    CBRACKET_L = b"{"
    SBRACKET_R = b"]"
    CBRACKET_R = b"}"
    BACKSLASH = b"\\"
    OR = b"|"
    SEMICOLON = b";"
    COLON = b":"
    QUOTE = b"'"
    DQUOTE = b'"'
    COMMA = b","
    LT = b"<"
    DOT = b"."
    GT = b">"
    SLASH = b"/"
    QM = b"?"
    CTRL_A = b"CTRL_A"
    CTRL_B = b"CTRL_B"
    CTRL_C = b"CTRL_C"
    CTRL_D = b"CTRL_D"
    CTRL_E = b"CTRL_E"
    CTRL_F = b"CTRL_F"
    CTRL_G = b"CTRL_G"
    CTRL_K = b"CTRL_K"
    CTRL_L = b"CTRL_L"
    CTRL_N = b"CTRL_N"
    CTRL_O = b"CTRL_O"
    CTRL_P = b"CTRL_P"
    CTRL_Q = b"CTRL_Q"
    CTRL_R = b"CTRL_R"
    CTRL_S = b"CTRL_S"
    CTRL_T = b"CTRL_T"
    CTRL_U = b"CTRL_U"
    CTRL_V = b"CTRL_V"
    CTRL_W = b"CTRL_W"
    CTRL_Y = b"CTRL_Y"
    CTRL_X = b"CTRL_X"
    CTRL_Z = b"CTRL_Z"
    ESC = b"ESC"
    F1 = b"F1"
    F2 = b"F2"
    F3 = b"F3"
    F4 = b"F4"
    F5 = b"F5"
    F6 = b"F6"
    F7 = b"F7"
    F8 = b"F8"
    F9 = b"F9"
    F10 = b"F10"
    F11 = b"F11"
    CTRL_F1 = b"CTRL_F1"
    CTRL_F2 = b"CTRL_F2"
    CTRL_F3 = b"CTRL_F3"
    CTRL_F4 = b"CTRL_F4"
    CTRL_F5 = b"CTRL_F5"
    CTRL_F6 = b"CTRL_F6"
    CTRL_F7 = b"CTRL_F7"
    CTRL_F8 = b"CTRL_F8"
    CTRL_F9 = b"CTRL_F9"
    CTRL_F10 = b"CTRL_F10"
    CTRL_F11 = b"CTRL_F11"
    CTRL_F12 = b"CTRL_F12"
    UP = b"UP"
    DOWN = b"DOWN"
    LEFT = b"LEFT"
    RIGHT = b"RIGHT"
    INS = b"INS"
    DEL = b"DEL"
    HOME = b"HOME"
    END = b"END"
    PGUP = b"PGUP"
    PGDN = b"PGDN"
    CTRL_DEL = b"CTRL_DEL"
    CTRL_HOME = b"CTRL_HOME"
    CTRL_END = b"CTRL_END"
    CTRL_PGUP = b"CTRL_PGUP"
    CTRL_PGDN = b"CTRL_PGDN"
    CTRL_UP = b"CTRL_UP"
    CTRL_DOWN = b"CTRL_DOWN"
    CTRL_LEFT = b"CTRL_LEFT"
    CTRL_RIGHT = b"CTRL_RIGHT"
    NULL = b"NULL"
    ENTER = b"ENTER"
    TAB = b"TAB"
    FILE_SEP = b"FILE_SEP"
    GRP_SEP = b"GRP_SEP"
    RCD_SEP = b"RCD_SEP"
    UNIT_SEP = b"UNIT_SEP"
    BACKSPACE = b"BACKSPACE"


if IS_WIN32:
    import msvcrt


    class KEYS(_KEYS):
        CTRL_NUMDOT = b"CTRL_NUMDOT"
        CTRL_SHIFT_TAB = b"CTRL_SHIFT_TAB"
        CTRL_NUM1 = b"CTRL_NUM1"
        CTRL_NUM2 = b"CTRL_NUM2"
        CTRL_NUM3 = b"CTRL_NUM3"
        CTRL_NUM4 = b"CTRL_NUM4"
        CTRL_NUM6 = b"CTRL_NUM6"
        CTRL_NUM7 = b"CTRL_NUM7"
        CTRL_NUM8 = b"CTRL_NUM8"
        CTRL_NUM9 = b"CTRL_NUM9"
        CTRL_NUMDIV = b"CTRL_NUMDIV"
        CTRL_INS = b"CTRL_INS"
        CTRL_ENTER = b"CTRL_ENTER"
        CTRL_BACKSPACE = b"CTRL_BACKSPACE"


    map_x00 = {
        b";": KEYS.F1,
        b"<": KEYS.F2,
        b"=": KEYS.F3,
        b">": KEYS.F4,
        b"?": KEYS.F5,
        b"@": KEYS.F6,
        b"A": KEYS.F7,
        b"B": KEYS.F8,
        b"C": KEYS.F9,
        b"D": KEYS.F10,
        b"^": KEYS.CTRL_F1,
        b"_": KEYS.CTRL_F2,
        b"`": KEYS.CTRL_F3,
        b"a": KEYS.CTRL_F4,
        b"b": KEYS.CTRL_F5,
        b"c": KEYS.CTRL_F6,
        b"d": KEYS.CTRL_F7,
        b"e": KEYS.CTRL_F8,
        b"f": KEYS.CTRL_F9,
        b"g": KEYS.CTRL_F10,
        b"\x03": KEYS.NULL,
        b"\x93": KEYS.CTRL_NUMDOT,
        b"\x94": KEYS.CTRL_SHIFT_TAB,
        b"u": KEYS.CTRL_NUM1,
        b"\x91": KEYS.CTRL_NUM2,
        b"v": KEYS.CTRL_NUM3,
        b"s": KEYS.CTRL_NUM4,
        b"t": KEYS.CTRL_NUM6,
        b"w": KEYS.CTRL_NUM7,
        b"\x8d": KEYS.CTRL_NUM8,
        b"\x84": KEYS.CTRL_NUM9,
        b"\x95": KEYS.CTRL_NUMDIV,
    }
    map_xe0 = {
        b"H": KEYS.UP,
        b"P": KEYS.DOWN,
        b"K": KEYS.LEFT,
        b"M": KEYS.RIGHT,
        b"R": KEYS.INS,
        b"S": KEYS.DEL,
        b"G": KEYS.HOME,
        b"O": KEYS.END,
        b"I": KEYS.PGUP,
        b"Q": KEYS.PGDN,
        b"\x85": KEYS.F11,
        b"\x89": KEYS.CTRL_F11,
        b"\x8a": KEYS.CTRL_F12,
        b"\x92": KEYS.CTRL_INS,
        b"\x93": KEYS.CTRL_DEL,
        b"w": KEYS.CTRL_HOME,
        b"u": KEYS.CTRL_END,
        b"\x86": KEYS.CTRL_PGUP,
        b"v": KEYS.CTRL_PGDN,
        b"\x8d": KEYS.CTRL_UP,
        b"\x91": KEYS.CTRL_DOWN,
        b"s": KEYS.CTRL_LEFT,
        b"t": KEYS.CTRL_RIGHT,
    }
    map = {
        b"\t": KEYS.TAB,
        b"\r": KEYS.ENTER,
        b"\n": KEYS.CTRL_ENTER,
        b"\x1b": KEYS.ESC,
        b"\x08": KEYS.BACKSPACE,
        b"\x7f": KEYS.CTRL_BACKSPACE,
        b"\x1c": KEYS.FILE_SEP,
        b"\x1d": KEYS.GRP_SEP,
        b"\x1e": KEYS.RCD_SEP,
        b"\x1f": KEYS.UNIT_SEP,
    }


    def getch():
        char = msvcrt.getch()
        if char == b"\xe0":
            char2 = msvcrt.getch()
            try:
                return map_xe0[char2]
            except:
                return char+char2
        if char == b"\x00":
            char2 = msvcrt.getch()
            try:
                return map_x00[char2]
            except:
                return char+char2
        if char in map:
            return map[char]
        if char[0] in range(1, 26+1):
            return b"CTRL_"+bytes([65-1+char[0]])
        return char
else:
    import tty
    import termios


    class KEYS(_KEYS):
        ALT_DEL = b"ALT_DEL"
        ALT_HOME = b"ALT_HOME"
        ALT_END = b"ALT_END"
        ALT_PGUP = b"ALT_PGUP"
        ALT_PGDN = b"ALT_PGDN"
        SHIFT_DEL = b"SHIFT_DEL"
        CTRL_SHIFT_DEL = b"CTRL_SHIFT_DEL"
        ALT_SHIFT_DEL = b"ALT_SHIFT_DEL"
        F12 = b"F12"
        SHIFT_F1 = b"SHIFT_F1"
        SHIFT_F2 = b"SHIFT_F2"
        SHIFT_F3 = b"SHIFT_F3"
        SHIFT_F4 = b"SHIFT_F4"
        SHIFT_F5 = b"SHIFT_F5"
        SHIFT_F6 = b"SHIFT_F6"
        SHIFT_F7 = b"SHIFT_F7"
        SHIFT_F8 = b"SHIFT_F8"
        SHIFT_F9 = b"SHIFT_F9"
        SHIFT_F10 = b"SHIFT_F10"
        SHIFT_F11 = b"SHIFT_F11"
        SHIFT_F12 = b"SHIFT_F12"
        ALT_F1 = b"ALT_F1"
        ALT_F2 = b"ALT_F2"
        ALT_F3 = b"ALT_F3"
        ALT_F4 = b"ALT_F4"
        ALT_F5 = b"ALT_F5"
        ALT_F6 = b"ALT_F6"
        ALT_F7 = b"ALT_F7"
        ALT_F8 = b"ALT_F8"
        ALT_F9 = b"ALT_F9"
        ALT_F10 = b"ALT_F10"
        ALT_F11 = b"ALT_F11"
        ALT_F12 = b"ALT_F12"
        CTRL_SHIFT_F1 = b"CTRL_SHIFT_F1"
        CTRL_SHIFT_F2 = b"CTRL_SHIFT_F2"
        CTRL_SHIFT_F3 = b"CTRL_SHIFT_F3"
        CTRL_SHIFT_F4 = b"CTRL_SHIFT_F4"
        CTRL_SHIFT_F5 = b"CTRL_SHIFT_F5"
        CTRL_SHIFT_F6 = b"CTRL_SHIFT_F6"
        CTRL_SHIFT_F7 = b"CTRL_SHIFT_F7"
        CTRL_SHIFT_F8 = b"CTRL_SHIFT_F8"
        CTRL_SHIFT_F9 = b"CTRL_SHIFT_F9"
        CTRL_SHIFT_F10 = b"CTRL_SHIFT_F10"
        CTRL_SHIFT_F11 = b"CTRL_SHIFT_F11"
        CTRL_SHIFT_F12 = b"CTRL_SHIFT_F12"
        ALT_SHIFT_F1 = b"ALT_SHIFT_F1"
        ALT_SHIFT_F2 = b"ALT_SHIFT_F2"
        ALT_SHIFT_F3 = b"ALT_SHIFT_F3"
        ALT_SHIFT_F4 = b"ALT_SHIFT_F4"
        ALT_SHIFT_F5 = b"ALT_SHIFT_F5"
        ALT_SHIFT_F6 = b"ALT_SHIFT_F6"
        ALT_SHIFT_F7 = b"ALT_SHIFT_F7"
        ALT_SHIFT_F8 = b"ALT_SHIFT_F8"
        ALT_SHIFT_F9 = b"ALT_SHIFT_F9"
        ALT_SHIFT_F10 = b"ALT_SHIFT_F10"
        ALT_SHIFT_F11 = b"ALT_SHIFT_F11"
        ALT_SHIFT_F12 = b"ALT_SHIFT_F12"
        CTRL_SHIFT_ALT_F1 = b"CTRL_SHIFT_ALT_F1"
        CTRL_SHIFT_ALT_F2 = b"CTRL_SHIFT_ALT_F2"
        CTRL_SHIFT_ALT_F3 = b"CTRL_SHIFT_ALT_F3"
        CTRL_SHIFT_ALT_F4 = b"CTRL_SHIFT_ALT_F4"
        CTRL_SHIFT_ALT_F5 = b"CTRL_SHIFT_ALT_F5"
        CTRL_SHIFT_ALT_F6 = b"CTRL_SHIFT_ALT_F6"
        CTRL_SHIFT_ALT_F7 = b"CTRL_SHIFT_ALT_F7"
        CTRL_SHIFT_ALT_F8 = b"CTRL_SHIFT_ALT_F8"
        CTRL_SHIFT_ALT_F9 = b"CTRL_SHIFT_ALT_F9"
        CTRL_SHIFT_ALT_F10 = b"CTRL_SHIFT_ALT_F10"
        CTRL_SHIFT_ALT_F11 = b"CTRL_SHIFT_ALT_F11"
        CTRL_SHIFT_ALT_F12 = b"CTRL_SHIFT_ALT_F12"


    map_x1b = {
        b"\x1b": KEYS.ESC,
        b"P": KEYS.F1,
        b"Q": KEYS.F2,
        b"R": KEYS.F3,
        b"S": KEYS.F4,
        b"A": KEYS.UP,
        b"B": KEYS.DOWN,
        b"D": KEYS.LEFT,
        b"C": KEYS.RIGHT,
        b"H": KEYS.HOME,
        b"F": KEYS.END,
        b"2": KEYS.INS,
        b"3": KEYS.DEL,
        b"5": KEYS.PGUP,
        b"6": KEYS.PGDN,
        b"15": KEYS.F5,
        b"17": KEYS.F6,
        b"18": KEYS.F7,
        b"19": KEYS.F8,
        b"20": KEYS.F9,
        b"21": KEYS.F10,
        b"23": KEYS.F11,
        b"24": KEYS.F12,
    }
    map = {
        b"\r": KEYS.ENTER,
        b"\t": KEYS.TAB,
        b"\x00": KEYS.NULL,
        b"\x1c": KEYS.FILE_SEP,
        b"\x1d": KEYS.GRP_SEP,
        b"\x1e": KEYS.RCD_SEP,
        b"\x1f": KEYS.UNIT_SEP,
        b"\x7f": KEYS.BACKSPACE,
    }


    def getch():
        def _getch():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            char = None
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
            except Exception as e:
                raise e
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                if isinstance(char, str):
                    return char.encode()
                else:
                    return char
        def switch_mod(_mod):
            if _mod == b";5":
                return b"CTRL_"
            elif _mod == b";2":
                return b"SHIFT_"
            elif _mod == b";3":
                return b"ALT_"
            elif _mod == b";6":
                return b"CTRL_SHIFT_"
            elif _mod == b";4":
                return b"ALT_SHIFT_"
            elif _mod == b";8":
                return b"CTRL_SHIFT_ALT_"
        char = _getch()
        if char in map:
            return map[char]
        elif char == b"\x1b":
            char2 = _getch()
            if char2 == b"\x1b":
                return map_x1b[char2]
            elif char2 == b"O":
                char3 = _getch()
                if char3 in map_x1b:
                    return map_x1b[char3]
                else:
                    return char+char2+char3
            elif char2 == b"[":
                char3 = _getch()
                if char3 in [b"1", b"2", b"3", b"5", b"6"]:
                    _char = _getch()
                    if _char == b";":
                        char4 = _char+_getch()
                        char5 = _getch()
                        if char5 in map_x1b:
                            return switch_mod(char4)+map_x1b[char5]
                        elif char3 in map_x1b:
                            return switch_mod(char4)+map_x1b[char3]
                        else:
                            return char+char2+char3+char4+char5
                    elif char3+_char in [b"15", b"17", b"18", b"19", b"20", b"21", b"23", b"24"]:
                        char4 = _char
                        _char = _getch()
                        if _char == b";":
                            char5 = _char+_getch()
                            char6 = _getch()
                            if char3+char4 in map_x1b:
                                return switch_mod(char5)+map_x1b[char3+char4]
                            else:
                                return char+char2+char3+char4+char5+char6
                        elif char3+char4 in map_x1b:
                            return map_x1b[char3+char4]
                        else:
                            return char+char2+char3+char4+_char
                    elif _char == b"~":
                        if char3 in map_x1b:
                            return map_x1b[char3]
                        else:
                            return char+char2+char3+_char
                    else:
                        char4 = _char
                    return char+char2+char3+char4
                elif char3 in map_x1b:
                    return map_x1b[char3]
                else:
                    return char+char2+char3
        if char[0] in range(1, 26+1):
            return b"CTRL_"+bytes([65-1+char[0]])
        return char


def getpw(prompt: str = "Enter password: "):
    print(prompt, end="", flush=True)
    pw = []
    while True:
        char = getch()
        if char == KEYS.CTRL_C:
            return
        elif char == KEYS.BACKSPACE and pw:
            pw.pop()
            continue
        elif char == KEYS.ENTER:
            return "".join(pw)
        if len(char) == 1 and char.decode() in string.printable:
            pw.append(char.decode())


def parse_credentials_argv(debug: bool = False):
    if debug:
        print("parsing credentials")
    credentials = []
    u = ["--username", "-U"]
    p = ["--password", "-P"]
    try:
        for i in range(0, len(sys.argv)):
            for k in u:
                if k == sys.argv[i]:
                    credentials.append(sys.argv[i+1])
                    break
        if len(credentials) == 0:
            if debug:
                print("skipped parse credentials")
            return credentials
        for i in range(0, len(sys.argv)):
            for k in p:
                if k == sys.argv[i]:
                    credentials.append(sys.argv[i+1])
                    break
        if len(credentials) == 2:
            if debug:
                print("parsed credentials")
            return credentials
        else:
            if debug:
                print("skipped parse credentials")
            return []
    except:
        if debug:
            print("skipped parse credentials")
        return []


