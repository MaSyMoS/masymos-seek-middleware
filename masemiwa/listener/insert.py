import logging

import masemiwa.config as conf
from masemiwa.input_analyser import InputAnalyseErrorReason, InputAnalyseError
from masemiwa.input_analyser.meta_checker import MetaChecker
from masemiwa.listener import E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK, E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO, \
    E502_HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD, E200_HTTP_RETURN_CODE_SUCCESS_ADDED

logger = logging.getLogger(__name__)


class Minsert():
    """
    handles all INSERT logic for a single model link (can have several content_blob)
    """

    def __init__(self, link: str):
        self.__link: str = link
        self.__metachecker: MetaChecker = None

    def process(self) -> (str, int):
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
            self._send()

        return "added {0} to queue".format(self.__link), E200_HTTP_RETURN_CODE_SUCCESS_ADDED

    def _check(self) -> bool:
        """
        will check the link
        :return True, if valid
        """

        self.__metachecker = MetaChecker(self.__link)
        return self.__metachecker.is_valid

    def _send(self) -> None:
        """
        will send the Link to the running Morre-Queue
        """
        links: list = self.__metachecker.valid_blobs_links

        if links is not None and len(links) > 0:
            conf.the_queue.add_to_queue_and_eventually_start(links)
