"""
get and deal with data from the seek instance
"""
from typing import Any
from urllib.parse import urlparse, ParseResultBytes

import logging

from requests import  Response

from masemiwa.input_analyser.NetworkTools import download_file

logger = logging.getLogger(__name__)


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


def download_seek_metadata(seek_url: SeekUrl) -> Any:
    """
    get json meta data from a seek object
    :param seek_url: the url o.O
    :return: None on Error else json-filled-dict, hopefully
    """

    headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Charset": "UTF-8"
    }

    r: Response = download_file(seek_url.url, headers=headers)
    if r is None:
        return
    return r.json()
