"""
get and deal with data from the seek instance
"""
from typing import Any

import logging

from requests import  Response

from masemiwa.input_analyser.beans import SeekUrl
from masemiwa.input_analyser.network_tools import download_file

logger = logging.getLogger(__name__)


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
