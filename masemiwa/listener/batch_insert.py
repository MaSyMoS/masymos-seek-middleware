import logging

import masemiwa.morre_queue as morre
from masemiwa.listener import HandleIO, E500_HTTP_RETURN_CODE_INTERNAL_ERROR, \
    E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO, E200_HTTP_RETURN_CODE_SUCCESS_ADDED
from masemiwa.listener.insert import HandleInsert

logger = logging.getLogger(__name__)


class HandleBatch(HandleIO):
    __links: list
    __blobs: list

    def __init__(self, links: list):
        self.__links = links
        self.__blobs = []

    def process(self) -> (str, int):
        valid: bool = False

        link: str
        # collect everything
        for link in self.__links:
            # create insert
            insert: HandleInsert = HandleInsert(link)
            # ignore the outcome
            insert.process(send_to_queue=False)
            # check and save for later
            if insert.is_valid:
                self.__blobs.extend(insert.get_blobs())
                valid = True

        logger.debug("checked %d links with %d valid content_blobs", len(self.__links), len(self.__blobs))

        # send
        if valid:
            if not self._send():
                return "FATAL unable to add {0} content_blob links to insert queue; check the logs!".format(
                    len(self.__blobs)), E500_HTTP_RETURN_CODE_INTERNAL_ERROR
        else:
            return "models cannot be used with MORRE", E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO

        return "added {0} content_blob links to insert-queue".format(
            len(self.__blobs)), E200_HTTP_RETURN_CODE_SUCCESS_ADDED

    def _send(self) -> bool:
        blobs: list = self.__blobs
        if len(blobs) > 0:
            morre.the_queue.add_to_insert_queue_and_eventually_start(blobs)
            return True
        return False
