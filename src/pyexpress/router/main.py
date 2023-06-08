from .base import BaseRouter


class Router(BaseRouter):

    def __init__(self) -> None:
        super().__init__()

    def extract(self):
        return self._stack
