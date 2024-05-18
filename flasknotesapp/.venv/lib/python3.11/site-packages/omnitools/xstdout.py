import sys


def p(*args, end="\n", flush=True, error=False) -> None:
    writer = sys.stderr.buffer if error else sys.stdout.buffer
    args = " ".join(str(_) for _ in args).encode()
    if not isinstance(end, bytes):
        end = str(end if end is not None else "").encode()
    writer.write(args+end)
    if flush:
        writer.flush()


