import logging
from abc import ABC

from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json

logger = logging.getLogger(__name__)


class MorreInsert(MorreConnect):
    def __init__(self, blob: SeekContentBlob):
        super().__init__()

        if not blob \
                or type(blob) is not SeekContentBlob \
                or blob.link.strip() is "":
            logger.fatal("MorreInsert called with invalid content_blob: %s", blob)
            raise AttributeError("MorreInsert called with invalid content_blob")

        self.__blob = blob

    def send(self) -> bool:
        logger.debug("insert - start sending %s", self.__blob.link)

        data: dict = dict(fileId=self.__blob.link,
                          url=self.__blob.link,
                          modelType=self.__blob.type.value)
        response: dict = send_post_request_with_json('add_model', data)

        if response \
                and response.get('ok') is not None \
                and str(response.get('ok')).strip().lower() is "true":
            logger.info("insert - successfully added %s", self.__blob.link)
            return True

        logger.info("insert - failed to add %s", self.__blob.link)
        return False
