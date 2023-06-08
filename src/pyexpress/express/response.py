from json import dumps
from socket import socket
from ..utils import status_code


class Response:
    __default_headers = {
        "X-Powered-By": "Express.py",
        "content-type": "text/html; charset=utf-8",
    }

    def __init__(self, conn: socket) -> None:
        self.__conn = conn
        self.__headers = self.__default_headers
        self.__status = 200
        self.__msg = status_code[self.__status]

    def set_headers(self, headers: dict[str, str]):
        self.__headers = headers

    def __write_head(self):
        res = f"HTTP/1.1 {self.__status} {self.__msg}\n"
        for key in self.__headers.keys():
            res += f"{key}: {self.__headers[key]}\n"
        res += "\n\n"
        return res.encode("utf-8")

    def json(self, data: dict):
        pre = dumps(data)
        self.set_headers({
            "X-Powered-By": "Express.py",
            "content-type": "application/json",
        })
        response_ = self.__write_head() + pre.encode("utf-8")
        self.__conn.send(response_)
        self.__conn.close()

    def status(self, code):
        self.__status = code
        self.__msg = status_code[code]
        return self

    def get_status(self):
        return f"{self.__status} - {self.__msg}"
