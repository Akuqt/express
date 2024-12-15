from json import dumps
from socket import socket
from ..utils import status_code
from ..common import Global


class Response(Global):
    __default_headers = {
        "X-Powered-By": "Express.py",
        "content-type": "text/html; charset=utf-8",
    }

    def __init__(self, conn: socket) -> None:
        super().__init__()
        self.class_id = "Response"
        self.__conn = conn
        self.__headers = self.__default_headers
        self.__status = 200
        self.__msg = status_code[self.__status]

    def set_headers(self, headers: dict[str, str]):
        self.__headers = headers

    def add_header(self, key: str, value: str):
        self.__headers[key] = value

    def get_headers(self) -> dict[str, str]:
        return self.__headers

    def __write_head(self):
        res = f"HTTP/1.1 {self.__status} {self.__msg}\n"
        for key in self.__headers.keys():
            res += f"{key}: {self.__headers[key]}\n"
        res += "\n\n"
        return res.encode("utf-8")

    def json(self, data: dict):
        pre = dumps(data)
        self.add_header("content-type", "application/json")
        response_ = self.__write_head() + pre.encode("utf-8")
        self.__conn.send(response_)
        self.__conn.close()

    def status(self, code):
        self.__status = code
        self.__msg = status_code[code]
        return self

    def get_status(self):
        return f"{self.__status} - {self.__msg}"
