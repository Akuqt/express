from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_KEEPALIVE


class Connector:
    def __init__(self, address, port) -> None:
        self.__address = address
        self.__port = port
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__socket.bind((self.__address, self.__port))

    def listen(self):
        self.__socket.listen()

    def get_conn(self):
        (connection, _) = self.__socket.accept()
        return connection

    def close(self):
        self.__socket.close()
