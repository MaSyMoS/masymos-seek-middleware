from json.decoder import JSONObject
from typing import List, Optional
from xml.etree import ElementTree as ET
import requests

import logging

from requests import Response

from masemiwa.input_analyser.NetworkTools import download_file
from masemiwa.input_analyser.seek_beans import ContentBlob

logger = logging.getLogger(__name__)


def check_content_blob(blob: ContentBlob) -> bool:
    """
    checks the JSON meta data of a content_blob
    and provides a simple boolean result
    """

    logger.debug("check content_blob %s", blob.__repr__())

    ## CHECK BASE
    if blob.mime.strip() is '' or \
            blob.link.strip() is '':
        return False

    ## CHECK MIME
    if not _check_mime_type(blob.mime):
        return False

    ## CHECK NAMESPACE, LEVEL and VERSION
    content: str = _download_blob_content(blob)
    if not _check_namespace(content):
        return False

    return True


mime_type_allow_list: List = ['application/sbml+xml', \
                              'application/xml', \
                              'text/xml']


def _check_mime_type(mime: str) -> bool:
    """
    checks the MIME type from SEEK-JSON against allow-list
    """
    return mime in mime_type_allow_list


def _download_blob_content(blob: ContentBlob) -> Optional[str]:
    """
    get XML for content_blob-link
    :param blob: the ContentBlob object
    :return: None on Error else xml as text
    """

    r: Response = download_file(blob.link + "/download")
    if r is None:
        return
    return r.text


def _check_namespace(content) -> bool:
    # TODO change to Optionl[bool] when adding retry functionality \
    #  indicate File not Found with None\
    #  or throw exception, maybe thats better!\
    #  https://github.com/MaSyMoS/masymos-seek-middleware/issues/11

    # TODO
    return False
