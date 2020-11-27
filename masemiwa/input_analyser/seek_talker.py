"""
get data from the seek instance
"""
import logging
from typing import Any, Optional

from requests import Response

from masemiwa.input_analyser.beans import SeekUrl, SeekContentBlob
from masemiwa.input_analyser.seek_network import download_file

logger = logging.getLogger(__name__)


def _download_seek_metadata(seek_url: SeekUrl) -> Any:
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


def _download_blob_content(blob: SeekContentBlob) -> Optional[str]:
    """
    get XML for content_blob-link
    :param blob: the SeekContentBlob object
    :return: None on Error else xml as text
    """

    r: Response = download_file(blob.link + "/download")
    if r is None:
        return
    return r.text