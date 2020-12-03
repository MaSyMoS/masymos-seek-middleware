import logging

from masemiwa.morre_gate import MorreConnect
from masemiwa.morre_gate.morre_network import send_post_request_with_json

logger = logging.getLogger(__name__)


class MorreAnnotations(MorreConnect):
    def __init__(self):
        pass

    def send(self) -> bool:
        logger.debug("annotations - start updating annotation index")

        data: dict = dict(dropExistingIndex=False)
        response: dict = send_post_request_with_json('create_annotation_index', data)

        if response \
                and response.get('ok') is not None \
                and str(response.get('ok')).strip().lower() is "true":
            logger.info("annotations - successfully removed %s", self.__blob.link)
            return True

        logger.info("annotations - failed to update annotation index", self.__blob.link)
        return False
