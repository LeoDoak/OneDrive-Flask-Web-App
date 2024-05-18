def args(*args, **kwargs) -> tuple:
    return (args, kwargs)


def def_template(_def, *args, **kwargs):
    def __def():
        return _def(*args, **kwargs)

    return __def

