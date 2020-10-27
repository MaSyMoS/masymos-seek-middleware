from typing import List, Optional, Match
import re


class SeekContentBlob():
    """
    dumb container for a content_blob JSON object
    """
    __json: dict

    @property
    def mime(self) -> str:
        return self.__json['content_type']

    @property
    def link(self) -> str:
        return self.__json['link']

    def __init__(self, json: dict):
        self.__json = json

    def __repr__(self):
        return "blob-json#" + self.link


class SeekJson():
    """
    dumb container for the whole JSON returned from SEEK
    """
    __json: dict

    @property
    def id(self) -> int:
        return self.__json['data']['id']

    @property
    def latest_version(self) -> int:
        return self.__json['data']['attributes']['latest_version']

    @property
    def content_blobs(self) -> List[SeekContentBlob]:
        ret: List[SeekContentBlob] = []
        blob: dict
        for blob in self.__json['data']['attributes']['content_blobs'].values():
            obj: SeekContentBlob = SeekContentBlob(blob)
            ret.append(obj)
        return ret

    def __init__(self, json: dict):
        self.__json = json

    def __repr__(self):
        return "seek-json#" + self.id


class XmlNamespaceVersionLevelMismatchException(Exception):
    pass


def _extract_level_version_from_namespace(namespace):
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


class XmlNamespace():
    """
    :raises XmlNamespaceVersionLevelMismatchException
    """

    def __init__(self, namespace: str, level: Optional[int] = None, version: Optional[int] = None):
        # check namespace
        if namespace is None or namespace.strip() is "":
            raise AttributeError("namespace cannot be empty or None")

        # get level and version from namespace
        namespace_level, namespace_version = _extract_level_version_from_namespace(namespace)

        # compare level/version with level/version from namespace
        if level is None:
            level = namespace_level
        if version is None:
            version = namespace_version

        if level is not namespace_level or \
                version is not namespace_version:
            raise XmlNamespaceVersionLevelMismatchException(
                "level/version ({0}/{1}) is not matching with namespace level/version ({2}/{3})".format(
                    level, version, namespace_level, namespace_version))

        self.__namespace = namespace
        self.__level = level
        self.__version = version

        # todo check namespace level/version with provided level/version
        pass

    def __repr__(self):
        # todo
        pass

    @property
    def namespace(self) -> str:
        return self.__namespace

    @property
    def level(self) -> Optional[int]:
        return self.__level

    @property
    def version(self) -> Optional[int]:
        return self.__version
