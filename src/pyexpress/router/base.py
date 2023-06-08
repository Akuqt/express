from .meta import Metadata


class BaseRouter:
    def __init__(self) -> None:
        self._stack: list[Metadata] = []

    def _push_stack(self, path: str, method: str, callback: callable):
        self._stack.append(Metadata(path, method, callback))

    def get(self, path: str, callback: callable):
        self._push_stack(path, "GET", callback)

    def post(self, path: str, callback: callable):
        self._push_stack(path, "POST", callback)
