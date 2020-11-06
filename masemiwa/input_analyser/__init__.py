from enum import Enum, unique
from typing import Optional


@unique
class InputAnalyseErrorReason(Enum):
    """
    this enum contains all possible reasons for InputAnalyseError
    the `enum.value` contains an explaining error message
    """
    URL_INVALID = "SEEK-URL is invalid"
    CONTENT_BLOB_BASE_ERROR = "SEEK-Metadata: the metadata is not valid, i.e. there is no file name or mime"
    CONTENT_BLOB_MIME_NOT_SUPPORTED = "SEEK-Metadata: the MIME of this file is not supported"
    CONTENT_BLOB_NAMESPACE_EMPTY = "namespace not defined"
    CONTENT_BLOB_NAMESPACE_NOT_SUPPORTED = "XML-File: the NAMESPACE, LEVEL or VERSION of this file is not supported"
    CONTENT_BLOB_NAMESPACE_LEVEL_VERSION_MISMATCH = "level/version of XML-attributes is not matching with namespace level/version "


class InputAnalyseError(AttributeError):
    """
    this Error is thrown, if any check fails
    see `reason` for more info, `resource` optional for filename
    """

    def __init__(self, reason: InputAnalyseErrorReason, resource: Optional[str] = None):
        self.__reason = reason
        self.__resource = resource

    @property
    def reason(self) -> InputAnalyseErrorReason:
        return self.__reason

    @property
    def resource(self) -> Optional[str]:
        return self.__resource

    @property
    def message(self) -> str:
        return self.__reason.value
