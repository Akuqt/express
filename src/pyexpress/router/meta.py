from ..types import Middleware, Callback


class Metadata:
    def __init__(
        self, path: str, method: str, middlewares: list[Middleware], callback: Callback
    ) -> None:
        self.__path = path
        self.__method = method
        self.__callback = callback
        self.__middlewares = middlewares

    def get(self):
        return self.__path, self.__method, self.__middlewares, self.__callback
