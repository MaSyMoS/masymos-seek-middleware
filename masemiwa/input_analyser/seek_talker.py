"""
get and deal with data from the seek instance
"""
from typing import Any
from urllib.parse import urlparse, ParseResultBytes

import requests
import logging

from requests import HTTPError, Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

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

    logger.debug("request JSON from %s", url.url)
    r: Response = None
    try:
        r = requests.get(url.url, headers=headers, timeout=5)
        r.raise_for_status()
    except ConnectTimeoutError or ConnectTimeout:
        logger.warning("unable to get JSON from %s; Timeout!", url.url)
        return None
    except HTTPError:
        code: str = 'unknown'
        if not r:
            code = r.status_code

        logger.warning("unable to get JSON from %s; HTTP-ErrorCode %s", url.url, code)
        return None

    logger.debug("successfully got JSON from %s")
    return r.json()


