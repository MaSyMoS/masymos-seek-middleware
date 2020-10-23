from typing import List


class ContentBlob():
    """
    dumb container for a content_blob JSON object
    """

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

    @property
    def id(self) -> int:
        return self.__json['data']['id']

    @property
    def latest_version(self) -> int:
        return self.__json['data']['attributes']['latest_version']

    @property
    def content_blobs(self) -> List[ContentBlob]:
        ret: List[ContentBlob] = []
        blob: dict
        for blob in self.__json['data']['attributes']['content_blobs']:
            obj: ContentBlob = ContentBlob(blob)
            ret.append(obj)
        return ret

    def __init__(self, json: dict):
        self.__json = json

    def __repr__(self):
        return "seek-json#" + self.id
