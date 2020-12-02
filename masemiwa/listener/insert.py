import logging

import masemiwa.config as conf
from masemiwa.input_analyser import InputAnalyseErrorReason, InputAnalyseError
from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.input_analyser.meta_checker import MetaChecker
from masemiwa.listener import E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK, E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO, \
    E502_HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD, E200_HTTP_RETURN_CODE_SUCCESS_ADDED, \
    E500_HTTP_RETURN_CODE_INTERNAL_ERROR, HandleIO

logger = logging.getLogger(__name__)


class handle_insert(HandleIO):
    """
    handles all INSERT logic for a single model link (can have several content_blob)
    """

    def __init__(self, link: str):
        self.__link: str = link
        self.__metachecker: MetaChecker = None

    def process(self) -> (str, int):
        """
        processes the meta checking
        :return: the HTTP message and code
        """
        # fetch metadata from SEEK, check it, fetch blobs and check namespaces
        try:
            valid: bool = self._check()
        except InputAnalyseError as e:
            if e.reason is InputAnalyseErrorReason.URL_INVALID \
                    or e.reason is InputAnalyseErrorReason.URL_NO_CONTENT:
                logger.error("unable to contact SEEK, %s, %s", e.reason, e.reason.error_message)
                return e.reason.error_message, E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK

            if self.__metachecker and self.__metachecker.did_one_download_fail:
                logger.info("a least one download failed for %s", self.__link)
                return InputAnalyseErrorReason.DATA_FILE_NOT_FOUND.error_message, E502_HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD

            logger.debug("abort, %s, %s, %s", e.reason, e.reason.error_message, self.__link)
            return e.reason.error_message, E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO

        if valid:
            # pass to morre-queue
            if not self._send():
                return "FATAL unable to add {0} to insert queue; check the logs!".format(
                    self.__link), E500_HTTP_RETURN_CODE_INTERNAL_ERROR

        return "added {0} to insert-queue".format(self.__link), E200_HTTP_RETURN_CODE_SUCCESS_ADDED

    def _check(self) -> bool:
        """
        will check the link
        :return True, if valid
        """

        self.__metachecker = MetaChecker(self.__link)
        return self.__metachecker.is_valid

    def _send(self) -> bool:
        """
        will send the Link to the Morre-Queue
        """
        blobs: list = self.__metachecker.valid_blobs

        if blobs is not None \
                and len(blobs) > 0 \
                and all(isinstance(x, SeekContentBlob) for x in list):
            conf.the_queue.add_to_insert_queue_and_eventually_start(blobs)
            return True

        logger.fatal(
            "the seems to be a check missing, \
            this list here is empty or has the wrong type of objects. this must not happen here!")
        return False
