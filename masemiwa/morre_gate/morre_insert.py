import logging
from abc import ABC

from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json

logger = logging.getLogger(__name__)


class MorreInsert(MorreConnect):
    def __init__(self, url):
        super().__init__(url)
        self.__url = url

    def send(self) -> bool:
        data:dict= dict(fileId=self.__url,
                        url=self.__url,
                        modelType="SBML")
        send_post_request_with_json('add_model')
