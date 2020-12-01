import logging
from abc import ABC

from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json

logger = logging.getLogger(__name__)


class MorreInsert(MorreConnect):
    def __init__(self, blob:SeekContentBlob):
        super().__init__(blob)
        self.__blob = blob

    def send(self) -> bool:
        data:dict= dict(fileId=self.__blob.link,
                        url=self.__blob.link,
                        modelType=self.__blob.type.value)
        send_post_request_with_json('add_model')
