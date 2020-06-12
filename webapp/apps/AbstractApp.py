from flask import Flask


class Apps:
    """This is a super class for applications within the software"""
    def __init__(self, url, load_on_server_start):
        self.load_on_server_start = load_on_server_start
        self.url = url

    def load_on_server_start(self) -> bool:
        return self.load_on_server_start

    def get_url(self) -> str:
        return self.url

    def setupOn(self, server: Flask) -> None:
        """Creates the application on the server, and defines its layout and callbacks"""
        raise Exception("Method not implemented")
