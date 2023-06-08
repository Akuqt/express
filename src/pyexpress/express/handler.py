from socket import socket
from .request import Request
from .response import Response
from ..router import Router, BaseRouter
from ..utils import add_slash, parse_headers, parse_route, match_routes


class Handler(BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self._port = 8000
        self._address = "127.0.0.1"
        self.__conn: socket
        self.__size = 4096
        self.__headers: dict[str, str] = {}
        self.__body: bytes = b""

    def __match_route(self, path: str, method: str, headers: dict[str, str]):
        if (headers["method"] != method):
            return False
        _, normalized = parse_route(path, headers)
        return match_routes(normalized, add_slash(path))

    def _use_router(self, router: Router):
        if (not router is None):
            self._stack.extend(router.extract())

    def __head(self, conn: socket):
        self.__conn = conn
        base = self.__conn.recv(self.__size)
        try:
            content, headers = parse_headers(base)
            headers["route"] = add_slash(headers["route"])
            self.__headers = headers
            self.__body = content
        except:
            return

    def _apply(self, conn: socket):
        self.__head(conn)
        for i in range(len(self._stack)):
            path, method, callback = self._stack[i].get()
            if (self.__match_route(path, method, self.__headers)):
                self.__handle(path, callback, self.__conn,
                              self.__headers, self.__body)
                break
            else:
                if (i == len(self._stack) - 1):
                    self.__handle(path, self.__unknown, self.__conn,
                                  self.__headers, self.__body)

    def __unknown(self, _, res: Response):
        res.status(404).json({
            "error": "Not Found"
        })

    def __handle(self, path: str, callback: callable, conn: socket, headers: dict[str, str], body: bytes):
        path = add_slash(path)
        req = Request(headers, body, conn, path)
        res = Response(conn)
        route_ = req.headers["route"]
        method_ = req.headers["method"]
        callback(req, res)
        print(f"{method_} -- {route_} -- {res.get_status()}")
