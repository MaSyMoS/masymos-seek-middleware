import logging

from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json, process_response

logger = logging.getLogger(__name__)


class MorreInsert(MorreConnect):
    __blob: SeekContentBlob

    def __init__(self, blob: SeekContentBlob):
        super().__init__()

        if not blob \
                or type(blob) is not SeekContentBlob \
                or blob.link.strip() == "":
            logger.fatal("MorreInsert called with invalid content_blob: %s", blob)
            raise AttributeError("MorreInsert called with invalid content_blob")

        self.__blob = blob

    def send(self) -> bool:
        logger.debug("insert - start sending %s", self.__blob.link)

        data: dict = dict(fileId=self.__blob.link,
                          url=self.__blob.link,
                          modelType=self.__blob.type.value,
                          enforceUniqueFileId=True)
        response: dict = send_post_request_with_json('add_model', data)

        return process_response(response,
                                success_msg="insert - successfully add {0}".format(self.__blob.link),
                                error_msg="insert - failed to add {0}".format(self.__blob.link))
