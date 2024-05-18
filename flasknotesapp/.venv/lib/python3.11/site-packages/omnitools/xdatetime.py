import datetime
import email.utils
from dateutil.tz import tzlocal, tzoffset


def dt2yyyymmddhhmmss(dt: datetime.datetime = None, ymd_delimiter: str = "-", hms_delimiter: str = "-") -> str:
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime(
        "%Y{ymd_delimiter}%m{ymd_delimiter}%d %H{hms_delimiter}%M{hms_delimiter}%S".format(
            ymd_delimiter=ymd_delimiter,
            hms_delimiter=hms_delimiter,
        )
    )


def yyyymmddhhmmss2dt(string: str, ymd_delimiter: str = "-", hms_delimiter: str = "-") -> datetime.datetime:
    return datetime.datetime.strptime(
        string, "%Y{ymd_delimiter}%m{ymd_delimiter}%d %H{hms_delimiter}%M{hms_delimiter}%S".format(
            ymd_delimiter=ymd_delimiter,
            hms_delimiter=hms_delimiter,
        )
    )


def timezone_offset() -> float:
    return tzlocal().utcoffset(datetime.datetime.now(tzlocal())).total_seconds()


def rfc822gmt2dt(string: str) -> datetime.datetime:
    t = email.utils.parsedate(string)[:6]
    if t:
        return datetime.datetime.fromtimestamp(datetime.datetime(*t).timestamp()+timezone_offset())


def dt2rfc822gmt(dt: datetime.datetime) -> str:
    return datetime.datetime.fromtimestamp(dt.timestamp()-timezone_offset()).strftime("%a, %d %b %Y %H:%M:%S GMT")


