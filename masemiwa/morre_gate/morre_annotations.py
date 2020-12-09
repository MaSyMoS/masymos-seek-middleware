import logging

from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json, process_response

logger = logging.getLogger(__name__)


class MorreAnnotations(MorreConnect):
    def __init__(self):
        pass

    def send(self) -> bool:
        logger.debug("annotations - start updating annotation index")

        data: dict = dict(dropExistingIndex=False)
        response: dict = send_post_request_with_json('create_annotation_index', data)

        return process_response(response,
                                success_msg="annotations - successfully updated",
                                error_msg="annotations - failed to update annotation index")
