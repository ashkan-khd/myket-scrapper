from abc import ABC, abstractmethod

import requests
from requests.models import Response


class IMDBRequestInterface(ABC):

    @abstractmethod
    def request(self) -> Response:
        pass


class IMDBCodeRequest(IMDBRequestInterface):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    def __init__(self, imdb_code: str) -> None:
        super().__init__()
        self.imdb_code = imdb_code

    @property
    def imdb_url(self) -> str:
        return f"https://www.imdb.com/title/{self.imdb_code}/"

    def request(self) -> Response:
        response = requests.get(self.imdb_url, headers=self.headers)
        response.raise_for_status()
        return response

