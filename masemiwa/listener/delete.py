import logging

import masemiwa.morre_queue as morre
from masemiwa.input_analyser import InputAnalyseErrorReason, InputAnalyseError
from masemiwa.input_analyser.beans import SeekUrl
from masemiwa.listener import E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK, E202_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO, \
    E200_HTTP_RETURN_CODE_SUCCESS_ADDED, E500_HTTP_RETURN_CODE_INTERNAL_ERROR, HandleIO

logger = logging.getLogger(__name__)


class HandleDelete(HandleIO):
    """
    handles all DELETE logic for a single model link (can have several content_blob)
    """
    __link: str

    def __init__(self, link: str):
        self.__link = link

    def process(self) -> (str, int):
        """
        processes the preparation
        :return: the HTTP message and code
        """

        # create objects
        try:
            seek_url: SeekUrl = SeekUrl(self.__link)
            self.__link = seek_url.url
        except InputAnalyseError as e:
            if e.reason is InputAnalyseErrorReason.URL_INVALID:
                logger.error("unable to parse SEEK link, %s, %s", e.reason, e.reason.error_message)
                return e.reason.error_message, E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK

            logger.debug("abort, %s, %s, %s", e.reason, e.reason.error_message, self.__link)
            return e.reason.error_message, E202_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO

        # pass to morre-queue
        if not self._send():
            return "FATAL unable to add {0} to delete queue; check the logs!".format(
                self.__link), E500_HTTP_RETURN_CODE_INTERNAL_ERROR

        return "added {0} to delete-queue".format(self.__link), E200_HTTP_RETURN_CODE_SUCCESS_ADDED

    def _send(self) -> bool:
        """
        will send the Link to the Morre-Queue
        """

        if self.__link is not None \
                and self.__link.strip() != "":
            morre.the_queue.add_to_delete_queue_and_eventually_start(self.__link)
            return True

        logger.fatal(
            "there seems to be a check missing, "
            "this list here is empty or has the wrong type of objects. this must not happen here!")
        return False
