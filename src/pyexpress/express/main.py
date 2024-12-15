from .handler import Handler
from .connector import Connector
from ..router import BaseRouter
from ..common import Global
from collections.abc import Callable


class Express(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.class_id = "Express"

    def use(self, param: Global):
        if param.class_id == "Router":
            self._use_router(param)

    def listen(
        self, address="127.0.0.1", port=8000, cb: Callable[[str, int], any] = None
    ):
        self.port = port
        self.address = address
        if not cb is None:
            cb(self.address, self.port)
        connector = Connector(self.address, self.port)
        try:
            connector.listen()
            while True:
                conn = connector.get_conn()
                self._apply(conn)

        except KeyboardInterrupt:
            print("FIN")
        except Exception as e:
            print(e.with_traceback())
