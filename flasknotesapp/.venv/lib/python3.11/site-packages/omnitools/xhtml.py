import lxml.html
import html
import urllib.parse
import re
from .xencode import try_utf8d


def html2xml(s):
    return lxml.html.fromstring(try_utf8d(s))


def str2html(s):
    return html.escape(s).replace(" ", "&nbsp;").replace("\n", "<br/>\n").replace("{", "&#x7B;").replace("}", "&#x7D;")


def encodeURIComponent(s):
    return urllib.parse.quote(s, safe="")


def decodeURIComponent(s):
    return urllib.parse.unquote(s)


def encodeURI(s):
    start = 0
    if re.search(r"^https?:\/\/", s):
        start = 2
    s = s.split("/")
    for i in range(start, len(s)):
        s[i] = encodeURIComponent(s[i])
    return "/".join(s)


def decodeURI(s):
    return "%2F".join([decodeURIComponent(_) for _ in re.split(r"%2[Ff]", s)])


