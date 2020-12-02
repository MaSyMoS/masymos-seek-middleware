import logging
from abc import ABC

from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json

logger = logging.getLogger(__name__)


class MorreDelete(MorreConnect):
    def __init__(self, link: str):
        super().__init__(link)
        self.__link = link

    def send(self) -> bool:
        logger.debug("delete - start sending %s", self.__link)

        data: dict = dict(fileId=self.__link)
        response: dict = send_post_request_with_json('delete_model', data)

        if response \
                and response.get('ok') is not None \
                and str(response.get('ok')).strip().lower() is "true":
            logger.info("delete - successfully removed %s", self.__link)
            return True

        logger.info("delete - failed to remove %s", self.__link)
        return False
