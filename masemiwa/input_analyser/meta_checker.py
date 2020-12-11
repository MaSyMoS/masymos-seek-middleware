import logging
import re
from typing import List
from xml.etree import ElementTree as ElementTreeFunctions
from xml.etree.ElementTree import ElementTree, Element

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.input_analyser.beans import SeekContentBlob, XmlNamespace, SeekUrl, SeekJson, SeekContentBlobType
from masemiwa.input_analyser.seek_network import download_seek_metadata, download_blob_content

logger = logging.getLogger(__name__)


class MetaChecker:
    """
    this class combines all meta checks done for a SEEK model
    extracts all valid content blobs
    raises InputAnalyseError on any error
    """
    __json: SeekJson
    __one_download_failed: bool
    __valid: bool
    __valid_blobs: List[SeekContentBlob]
    __seek_url: SeekUrl

    def __init__(self, url: str):
        self.__valid_blobs = []
        self.__valid = False
        self.__one_download_failed = False

        # parse URL
        self.__seek_url = SeekUrl(url)

        # get metadata
        seek_json: dict = download_seek_metadata(self.__seek_url)
        if seek_json is None:
            logger.debug("unable to get metadata from url %s", self.__seek_url)
            raise InputAnalyseError(InputAnalyseErrorReason.URL_NO_CONTENT, self.__seek_url.url)

        # parse JSON, check metadata
        self.__json = SeekJson(seek_json)

        # check content_blobs
        blobs: List[SeekContentBlob] = self.__json.content_blobs
        if blobs is None or len(blobs) == 0:
            raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID, self.__seek_url.url)
        blob: SeekContentBlob
        for blob in blobs:
            try:
                if self._check_content_blob(blob):
                    self.__valid = True
                    self.__valid_blobs.append(blob)
            except InputAnalyseError as e:
                if e.reason is InputAnalyseErrorReason.DATA_FILE_NOT_FOUND:
                    logger.info("unable to download file %s", blob.link)
                    self.__one_download_failed = True
                elif e.reason is InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH:
                    logger.info("namespace vs. attribute level/version mismatch in file %s", blob.link)
                else:
                    logger.info("unable to process content blob %s; %s - %s",
                                 blob.link, e.reason, e.reason.error_message)

    @property
    def is_valid(self) -> bool:
        return self.__valid

    @property
    def url(self) -> SeekUrl:
        return self.__seek_url

    @property
    def valid_blobs(self) -> List[SeekContentBlob]:
        return self.__valid_blobs

    @property
    def did_one_download_fail(self) -> bool:
        return self.__one_download_failed

    def __repr__(self):
        return "metachecker#" + str(self.__seek_url.url)

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
        xml: str = download_blob_content(blob)
        if xml is None:
            logger.debug("unable to download file for %s", blob.__repr__())
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_FILE_NOT_FOUND)
            pass
        if not MetaChecker._check_namespace(blob, xml):
            logger.debug("namespace check FAILED for %s", blob.__repr__())
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_NAMESPACE_NOT_SUPPORTED, blob.__repr__())
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
    def _check_namespace(blob: SeekContentBlob, xml: str) -> bool:

        namespace: XmlNamespace = MetaChecker._extract_namespace(xml)

        if namespace.namespace.startswith('http://www.sbml.org/sbml'):
            if namespace.level <= 2:
                blob.set_type(SeekContentBlobType.SBML)
                return True

        elif namespace.namespace.startswith('http://sed-ml.org'):
            if namespace.level == 1 \
                    and namespace.version < 3:
                blob.set_type(SeekContentBlobType.SEDML)
                return True

        elif namespace.namespace.startswith('http://www.cellml.org/cellml/1.0') \
                or namespace.namespace.startswith('http://www.cellml.org/cellml/1.1'):
            blob.set_type(SeekContentBlobType.CELLML)
            return True

        return False

    @staticmethod
    def _extract_namespace(xml: str) -> XmlNamespace:
        # parse XML
        root: ElementTree
        try:
            root = ElementTreeFunctions.fromstring(xml.strip())
        except ElementTreeFunctions.ParseError:
            logger.debug("unable to parse file")
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_NOT_VALID_XML)

        child: Element
        data: dict = {}
        for child in root.findall('.'):
            try:
                data['namespace'] = re.search('.*{(.*)}.*', str(child)).group(1)
                logger.debug("found namespace '%s'", data['namespace'])
            except AttributeError:
                continue
            # gt version ans level from attribute
            if data.get('namespace') is not None:
                try:
                    data['version'] = int(child.attrib['version'])
                except ValueError:
                    raise InputAnalyseError(InputAnalyseErrorReason.DATA_ATTRIBUTE_NOT_PARSABLE)
                except KeyError:
                    # optional
                    pass
                try:
                    data['level'] = int(child.attrib['level'])
                except ValueError:
                    raise InputAnalyseError(InputAnalyseErrorReason.DATA_ATTRIBUTE_NOT_PARSABLE)
                except KeyError:
                    # optional
                    pass
                break

        if data.get('namespace') is None:
            logger.debug("no namespace found")
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_NAMESPACE_EMPTY)

        # create XmlNamespace
        return XmlNamespace(data['namespace'],
                            data.get('level'),
                            data.get('version'))
