class Metadata:
    def __init__(self, path: str, method: str, callback: callable) -> None:
        self.__path = path
        self.__method = method
        self.__callback = callback

    def get(self):
        return self.__path, self.__method, self.__callback
