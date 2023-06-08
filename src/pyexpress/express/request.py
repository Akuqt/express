from json import loads
from socket import socket
from ..utils import get_params, parse_route


class Request:
    def __init__(self, headers: dict[str, str], body: bytes | dict, conn: socket, route: str) -> None:
        self.__conn = conn
        self.__size = 4096
        self.body = body
        self.__route = route
        self.headers = headers
        self.query: dict[str, dict[str, list[str]]] = {}
        self.params: dict[str, str] = {}
        self.__get_data()
        self.__parse()

    def __get_data(self):
        if ("content-length" in self.headers.keys()):
            lenght = int(self.headers["content-length"])
            while len(self.body) < lenght:
                self.body += self.__conn.recv(self.__size)

    def __parse(self):
        query, normalized = parse_route(self.__route, self.headers)
        params = get_params(normalized, self.__route)
        self.params = params
        self.query = query
        if ("content-type" in self.headers.keys()):
            if (self.headers["content-type"] == "application/json"):
                self.body = loads(self.body.decode("utf-8"))
