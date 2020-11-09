from typing import List

import logging

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.input_analyser.beans import SeekContentBlob, XmlNamespace, SeekUrl, SeekJson
from masemiwa.input_analyser.seek_talker import _download_seek_metadata, _download_blob_content

logger = logging.getLogger(__name__)


class MetaChecker():
    """
    this class combines all meta checks done for a candidate file link
    raises InputAnalyseError on any error
    """

    def __init__(self, url: str):
        self.__valid: bool = False

        # parse URL
        self.__url: SeekUrl = SeekUrl(url)

        # get metadata
        seek_json: dict = _download_seek_metadata(self.__url)
        if seek_json is None:
            logger.debug("unable to get metadata from url %s", self.__url)
            raise InputAnalyseError(InputAnalyseErrorReason.URL_NO_CONTENT, self.__url)

        # parse JSON, check metadata
        self.__json: SeekJson = SeekJson(seek_json)

        # check content_blobs
        for blob in self.__json.content_blobs:
            # TODO
            pass

    # check mime

    @property
    def is_valid(self) -> bool:
        return self.__valid

    @property
    def url(self) -> SeekUrl:
        return self.__url

    def __repr__(self):
        return "metachecker#" + str(self.__url.url)

    @staticmethod
    def _check_content_blob(blob: SeekContentBlob) -> bool:
        """
        checks the JSON meta data of a content_blob
        return true, if everything is ok
        else raises `InputAnalyseError`
        """

        logger.debug("check content_blob %s", blob.__repr__())

        # CHECK MIME
        if not MetaChecker._check_mime_type(blob.mime):
            logger.debug("mime check FAILED for %s", blob.__repr__())
            raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_MIME_NOT_SUPPORTED, blob.__repr__())
        logger.debug("mime check passed")

        # CHECK NAMESPACE, LEVEL and VERSION
        xml: str = _download_blob_content(blob)
        if xml is None:
            # TODO throw an exception, indicating File not Found with None
            pass
        if not MetaChecker._check_namespace(xml):
            logger.debug("namespace check FAILED for %s", blob.__repr__())
            raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_NAMESPACE_NOT_SUPPORTED, blob.__repr__())
        logger.debug("namespace check passed")

        return True

    _mime_type_allow_list: List = ['application/sbml+xml',
                                   'application/xml',
                                   'text/xml']

    @staticmethod
    def _check_mime_type(mime: str) -> bool:
        """
        checks the MIME type from SEEK-JSON against allow-list
        """
        return mime in MetaChecker._mime_type_allow_list

    @staticmethod
    def _check_namespace(content: str) -> bool:
        # TODO add retry-functionality https://github.com/MaSyMoS/masymos-seek-middleware/issues/11

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
