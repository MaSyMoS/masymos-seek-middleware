from json.decoder import JSONObject
from typing import List, Optional
from xml.etree import ElementTree as ET
import requests

import logging

from requests import Response

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.input_analyser.network_tools import download_file
from masemiwa.input_analyser.beans import SeekContentBlob, XmlNamespace, SeekUrl

logger = logging.getLogger(__name__)


class MetaChecker():
    """
    this class combines all meta checks done for a candidate file link
    """

    def __init__(self, url: str):
        self.__url: SeekUrl = SeekUrl(url)
        self.__valid: bool = False

    @property
    def is_valid(self) -> bool:
        return self.__valid

    @property
    def url(self) -> SeekUrl:
        return self.__url


def check_content_blob(blob: SeekContentBlob) -> bool:
    """
    checks the JSON meta data of a content_blob
    return true, if everything is ok
    else raises `InputAnalyseError`
    """

    logger.debug("check content_blob %s", blob.__repr__())

    # CHECK BASE
    if blob.mime.strip() is '' or \
            blob.link.strip() is '':
        logger.debug("base check FAILED for %s", blob.__repr__())
        raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_BASE_ERROR, blob.__repr__())
    logger.debug("base check passed")

    # CHECK MIME
    if not _check_mime_type(blob.mime):
        logger.debug("mime check FAILED for %s", blob.__repr__())
        raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED, blob.__repr__())
    logger.debug("mime check passed")

    # CHECK NAMESPACE, LEVEL and VERSION
    xml: str = _download_blob_content(blob)
    if xml is None or not _check_namespace(xml):
        logger.debug("namespace check FAILED for %s", blob.__repr__())
        raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_NAMESPACE_NOT_SUPPORTED, blob.__repr__())
    logger.debug("namespace check passed")

    return True


_mime_type_allow_list: List = ['application/sbml+xml',
                               'application/xml',
                               'text/xml']


def _check_mime_type(mime: str) -> bool:
    """
    checks the MIME type from SEEK-JSON against allow-list
    """
    return mime in _mime_type_allow_list


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


def _check_namespace(content: str) -> bool:
    # TODO throw an exception, indicating File not Found with None
    #  https://github.com/MaSyMoS/masymos-seek-middleware/issues/11

    namespace: XmlNamespace
    # TODO extract namespace

    if namespace.namespace.startswith('http://www.sbml.org/sbml'):
        # TODO
        pass
    elif namespace.namespace.startswith('http://sed-ml.org'):
        # TODO
        pass
    elif namespace.namespace.startswith('http://www.cellml.org/cellml/1.0') or \
            namespace.namespace.startswith('http://www.cellml.org/cellml/1.1'):
        # TODO
        pass

    return False
