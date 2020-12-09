import logging

from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json, process_response

logger = logging.getLogger(__name__)


class MorreDelete(MorreConnect):
    __link: str

    def __init__(self, link: str):
        super().__init__(link)
        self.__link = link

    def send(self) -> bool:
        logger.debug("delete - start sending %s", self.__link)

        data: dict = dict(fileId=self.__link)
        response: dict = send_post_request_with_json('delete_model_by_fileid', data)

        return process_response(response,
                                success_msg="delete - successfully removed {0}".format(self.__link),
                                error_msg="delete - failed to remove {0}".format(self.__link))
