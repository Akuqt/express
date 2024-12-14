from .meta import Metadata
from ..types import Middleware, Callback


class BaseRouter:
    def __init__(self) -> None:
        self._stack: list[Metadata] = []

    def __get_middlewares_and_callback(self, args: tuple[Middleware | Callback]):
        middleware_stack: list[Middleware] = []
        callback_arg: Callback = None
        for arg in args:
            if arg is None:
                continue
            if (
                callable(arg)
                and arg.__code__.co_argcount == 2
                and args.index(arg) == len(args) - 1
            ):
                callback_arg = arg
            if callable(arg) and arg.__code__.co_argcount == 3:
                middleware_stack.append(arg)
        return middleware_stack, callback_arg

    def _push_stack(self, path: str, method: str, args: tuple[Middleware | Callback]):
        middlewares, callback = self.__get_middlewares_and_callback(args)
        self._stack.append(Metadata(path, method, middlewares, callback))

    def get(self, path: str, *args: Middleware | Callback):
        self._push_stack(path, "GET", args)

    def post(self, path: str, *args: Middleware | Callback):
        self._push_stack(path, "POST", args)
