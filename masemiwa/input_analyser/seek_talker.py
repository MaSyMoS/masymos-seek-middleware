"""
get and deal with data from the seek instance
"""
from typing import Any
from urllib.parse import urlparse, ParseResultBytes

import requests


class SeekUrlException(ValueError):
    pass


class SeekUrl():
    """
    parse and interpret a SEEk URL
    """
    __input: ParseResultBytes

    def __init__(self, url: str):
        self.__input = urlparse(url)

        # remove unnecessary components
        self.__input = self.__input._replace(params=''). \
            _replace(query=''). \
            _replace(fragment='')

        # remove endings like '.json'
        if '.' in self.__input.path:
            self.__input = self.__input._replace(path=self.__input.path.split(".")[0])

        try:
            if self.url is None or self.url.strip() is '' or self.id is None:
                raise SeekUrlException("URL invalid - result-URLor ID is empty: {0}".format(url))
        except Exception as e:
            raise SeekUrlException("invalid SEEK-URL: {0}".format(url))

    @property
    def url(self) -> str:
        return str(self.__input.geturl())

    @property
    def id(self) -> int:
        return int(self.__input.path.rsplit('/', 1)[-1])

    def __repr__(self):
        return self.url


def json_for_resource(url: SeekUrl) -> Any:
    """
    get json meta data fro a seek object
    :param url: the url o.O
    :return: JSON, hopefully
    """

    headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Charset": "ISO-8859-1"
    }

    r = requests.get(url.url, headers=headers)
    r.raise_for_status()
    return r.json()
