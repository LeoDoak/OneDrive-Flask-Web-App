from typing import Any, Type, overload, Callable


class overload_condition:
    def __init__(self, *types, args_i=-1, kwargs_k=None, condition=None, func=None):
        self.types = types or tuple()
        self.args_i = args_i
        self.kwargs_k = kwargs_k
        self.condition = condition
        self.func = func


normal_overload_cache = {}


def normal_overload(
        *types, # type: Type[Any]
        group # type: str
):
    def dec(_func):
        def wrapper(*args, **kwargs):
            if types:
                return _func(*args, **kwargs)
            else:
                self = None
                args = list(args)
                is_class = "." in _func.__qualname__
                if args:
                    qualname = args[0].__qualname__ if hasattr(args[0], "__qualname__") else args[0].__class__.__qualname__
                    if qualname == _func.__qualname__.split(".")[0]:
                        self = args.pop(0)
                sig = tuple([type(_) for _ in args]+[type(_) for _ in kwargs.values()])
                match_type = [_[1] for _ in normal_overload_cache[group] if sig == _[0]]
                # print(normal_overload_cache, self, sig, match_type)
                if not match_type:
                    raise LookupError("cannot find appropriate handler for method {} with signature {}".format(
                        _func.__qualname__,
                        [_.__name__ for _ in sig]
                    ))
                if is_class:
                    args.insert(0, self)
                return match_type[0](*args, **kwargs)
        if group not in normal_overload_cache:
            normal_overload_cache[group] = []
        if types:
            normal_overload_cache[group].append([types, _func])
        return wrapper
    return dec


def conditional_overload(
        *conditions # type: overload_condition
):
    def dec(_func):
        # print(_func, _func.__qualname__, conditions)
        def wrapper(*args, **kwargs):
            self = None
            args = list(args)
            is_class = "." in _func.__qualname__
            if args:
                qualname = args[0].__qualname__ if hasattr(args[0], "__qualname__") else args[0].__class__.__qualname__
                if qualname == _func.__qualname__.split(".")[0]:
                    self = args.pop(0)
            func = None
            sig = []
            for condition in conditions:
                exist = False
                found = [False]
                __func = None
                try:
                    t = kwargs[condition.kwargs_k]
                    exist = True
                    if callable(condition.condition) and condition.condition(t):
                        __func = condition.func
                        found[0] = True
                except:
                    pass
                if not found[0]:
                    try:
                        t = args[condition.args_i]
                        exist = True
                        if callable(condition.condition) and condition.condition(t):
                            __func = condition.func
                            found[0] = True
                    except:
                        pass
                sig = tuple([type(_) for _ in args]+[type(_) for _ in kwargs.values()])
                if condition.types:
                    found.append(False)
                    if sig == condition.types:
                        __func = condition.func
                        found[1] = True
                # print(__func,found,args,kwargs,len(sig),len(condition.types),callable(condition.condition) and condition.condition(args[condition.args_i]))
                if len(found) == 1 and found[0]:
                    func = __func
                    break
                elif len(found) == 2 and all(found):
                    func = __func
                    break
                elif len(found) == 2 and found[1] and exist:
                    func = __func
                    break
            # print(args, kwargs)
            if not func:
                raise LookupError("cannot find appropriate handler for method {} with signature {}".format(
                    _func.__qualname__,
                    [_.__name__ for _ in sig]
                ))
            if is_class:
                args.insert(0, self)
            return func(*args, **kwargs)
        return wrapper
    return dec


@overload
def overloaded(
        *types, # type: Type[Any]
        group # type: str
) -> Callable:
    ...


@overload
def overloaded(
        *conditions # type: overload_condition
) -> Callable:
    ...


@conditional_overload(
    overload_condition(
        args_i=0,
        kwargs_k="group",
        condition=lambda x: isinstance(x, overload_condition),
        func=conditional_overload
    ),
    overload_condition(
        args_i=0,
        kwargs_k="group",
        condition=lambda x: not isinstance(x, overload_condition),
        func=normal_overload
    ),
)
def overloaded(*args, **kwargs) -> Callable:
    ...


def create_normal_overloaded_wrapper(group: str):
    def wrapper(*args):
        if len(args) == 1 and callable(args[0]):
            return overloaded(group=group)(args[0])
        else:
            return overloaded(*args, group=group)
    return wrapper

