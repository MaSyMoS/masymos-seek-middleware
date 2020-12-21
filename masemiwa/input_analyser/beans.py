import logging
import re
from enum import unique, Enum
from typing import List, Optional, Match
from urllib.parse import ParseResult, urlparse

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason

logger = logging.getLogger(__name__)


class SeekUrl:
    """
    parse and interpret a SEEk URL
    :raises InputAnalyseError on error
    """
    __input: ParseResult

    def __init__(self, url: str):
        self.__input = urlparse(url)

        # remove unnecessary components
        # noinspection PyProtectedMember
        self.__input = self.__input._replace(params=''). \
            _replace(query=''). \
            _replace(fragment='')

        # remove endings like '.json'
        if '.' in self.__input.path:
            # noinspection PyProtectedMember
            self.__input = self.__input._replace(path=self.__input.path.split(".")[0])

        try:
            if self.url is None or self.url.strip() == "" or self.id is None:
                logger.debug("URL invalid - result-URL or ID is empty: {0}".format(url))
                raise InputAnalyseError(InputAnalyseErrorReason.URL_INVALID,
                                        "URL invalid - result-URL or ID is empty: {0}".format(url))
        except Exception:
            # this try is for the url.strip() call
            logger.debug("URL invalid (%s)", url)
            raise InputAnalyseError(InputAnalyseErrorReason.URL_INVALID, url)

    @property
    def url(self) -> str:
        return str(self.__input.geturl())

    @property
    def id(self) -> int:
        return int(self.__input.path.rsplit('/', 1)[-1])

    def __repr__(self):
        return "seek-url#" + self.__input.geturl()


@unique
class SeekContentBlobType(Enum):
    """
    define type of document by namespace, value is the string used in MaSyMoS Morre
    """
    SBML = "SBML"
    CELLML = "CELLML"
    SEDML = "SEDML"


class SeekContentBlob:
    """
    container for a content_blob JSON object; including base check (type, keys)
    :raises `InputAnalyseError`
    """
    __json: dict
    __type: Optional[SeekContentBlobType]

    @property
    def mime(self) -> str:
        return self.__json['content_type']

    @property
    def link(self) -> str:
        return self.__json['link']

    @property
    def type(self) -> SeekContentBlobType:
        return self.__type

    @property
    def link_to_model(self) -> str:
        """
        :return:URL to model without "content_blob/…"
        """
        return self.link.rsplit('/content_blob', 1)[0]

    def set_type(self, t: SeekContentBlobType):
        self.__type = t

    def __init__(self, json: dict):
        self.__type = None
        self.__json = json
        try:
            if self.mime.strip() == '' or \
                    self.link.strip() == '':
                raise ValueError("MIME or LINK of content_blob empty")
        except (ValueError, KeyError) as e:
            logger.debug("content_blob json invalid, error: %s", e)
            raise InputAnalyseError(InputAnalyseErrorReason.CONTENT_BLOB_CONTENT_INVALID)

    def __repr__(self):
        return "seek-blob-json#" + self.link


class SeekJson:
    """
    container for the whole JSON returned from SEEK; including base check (type, keys)
    :raises `InputAnalyseError`
    """
    __json: dict

    @property
    def id(self) -> int:
        return int(self.__json['data']['id'])

    @property
    def latest_version(self) -> int:
        return int(self.__json['data']['attributes']['latest_version'])

    @property
    def content_blobs(self) -> List[SeekContentBlob]:
        ret: List[SeekContentBlob] = []
        blob: dict
        for blob in list(self.__json['data']['attributes']['content_blobs']):
            if type(blob) is not dict:
                logger.debug("blob type (%s) incorrect, skip", type(blob))
                continue
            obj: SeekContentBlob
            try:
                obj = SeekContentBlob(blob)
            except InputAnalyseError as e:
                logger.debug("skip blob, error initialising SeekContentBlob %s", e)
                continue
            ret.append(obj)
        return ret

    def __init__(self, json: dict):
        self.__json = json.copy()
        try:
            # referencing a non-existing key will result in a KeyError
            # the call of self.id etc. will also raise a ValueError, if the value is wrong
            if type(self.id) is not int \
                    or self.id is None:
                raise ValueError("ID is invalid (%s)", self.id)
            if type(self.latest_version) is not int \
                    or self.latest_version is None:
                raise ValueError("latest_version is invalid (%s)", self.latest_version)
            if type(self.__json['data']['attributes']['content_blobs']) is not dict \
                    and type(self.__json['data']['attributes']['content_blobs']) is not list:
                raise ValueError("content_blob invalid")
        except (ValueError, KeyError) as e:
            logger.debug("json invalid, error: %s", e)
            raise InputAnalyseError(InputAnalyseErrorReason.JSON_CONTENT_INVALID)

    def __repr__(self):
        return "seek-json#" + str(self.id)


class XmlNamespace:
    """
    container for the namespace + level + version
    with a bit logic to check level/version from namespace against given level/version
    :raises XmlNamespaceVersionLevelMismatchException
    """
    __namespace: str
    __level: int
    __version: int

    def __init__(self, namespace: str, level: Optional[int] = None, version: Optional[int] = None):
        # check namespace
        if namespace is None or namespace.strip() == "":
            logger.debug("namespace cannot be empty or None")
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_NAMESPACE_EMPTY)

        # get level and version from namespace
        namespace_level: int
        namespace_version: int
        namespace_level, namespace_version = self._extract_level_version_from_namespace(namespace)

        # compare level/version with level/version from namespace
        # # non-existing values are ignored here
        if level is None:
            level = namespace_level
        if version is None:
            version = namespace_version
        if namespace_level is None:
            namespace_level = level
        if namespace_version is None:
            namespace_version = version

        if level != namespace_level or \
                version != namespace_version:
            logger.debug("level/version ({0}/{1}) is not matching with namespace level/version ({2}/{3})".format(
                level, version, namespace_level, namespace_version))
            raise InputAnalyseError(InputAnalyseErrorReason.DATA_NAMESPACE_LEVEL_VERSION_MISMATCH, namespace)

        self.__namespace = namespace
        self.__level = level
        self.__version = version

    def __repr__(self):
        return self.namespace

    @property
    def namespace(self) -> str:
        return self.__namespace

    @property
    def level(self) -> Optional[int]:
        return self.__level

    @property
    def version(self) -> Optional[int]:
        return self.__version

    @staticmethod
    def _extract_level_version_from_namespace(namespace: str) -> (Optional[int], Optional[int]):
        """
        extracts level and version from namespace like "http://www.sbml.org/sbml/level2/version4"
        :param namespace:
        :return: namespace_level, namespace_version as Optional[int]
        """
        namespace_level: Optional[int] = None
        l: Optional[Match] = re.search(r'level(\d*)', namespace)
        if l is not None:
            namespace_level = int(l.group(1))
        namespace_version: Optional[int] = None
        v: Optional[Match] = re.search(r'version(\d*)', namespace)
        if v is not None:
            namespace_version = int(v.group(1))
        return namespace_level, namespace_version
