from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


class Connector:
    def __init__(self, address, port) -> None:
        self.__address = address
        self.__port = port
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__socket.bind((self.__address, self.__port))

    def listen(self) -> socket:
        self.__socket.listen(1)

    def get_conn(self):
        (connection, _) = self.__socket.accept()
        return connection
