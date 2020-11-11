from enum import Enum, unique
from typing import Optional


@unique
class InputAnalyseErrorReason(Enum):
    """
    this enum contains all possible reasons for InputAnalyseError
    the `enum.value` contains an explaining error message
    """
    URL_INVALID = "SEEK-URL is invalid"
    URL_NO_CONTENT = "unable to get SEEK Metadata from URL"
    JSON_CONTENT_INVALID = "the JSON content is invalid, i.e. an Integer is String or missing, check ID ans LINK"
    CONTENT_BLOB_CONTENT_INVALID = "SEEK-Metadata: the metadata is not valid, i.e. there is no file name or mime"
    CONTENT_BLOB_MIME_NOT_SUPPORTED = "SEEK-Metadata: the MIME of this file is not supported"
    DATA_FILE_NOT_FOUND = "file specified in conten_blob could not be found"
    DATA_NOT_VALID_XML = "XML-File: cannot parse file s XML"
    DATA_ATTRIBUTE_NOT_PARSABLE = "cannot parse level or version; must be Integer"
    DATA_NAMESPACE_EMPTY = "XML-File: namespace not defined"
    DATA_NAMESPACE_NOT_SUPPORTED = "XML-File: the NAMESPACE, LEVEL or VERSION of this file is not supported"
    DATA_NAMESPACE_LEVEL_VERSION_MISMATCH = "XML-File: level/version of XML-attributes is not matching with namespace level/version "


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
