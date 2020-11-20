import logging

from masemiwa.input_analyser import InputAnalyseErrorReason, InputAnalyseError
from masemiwa.input_analyser.meta_checker import MetaChecker
from masemiwa.listener import HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK, HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO, \
    HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD, HTTP_RETURN_CODE_SUCCESS_ADDED

logger = logging.getLogger(__name__)


class Minsert():
    """
    handles all INSERT logic for a single model link (can have several content_blob)
    """

    def __init__(self, link: str):
        self.__link = link
        self.__metachecker = None

    def process(self) -> (str, int):
        # fetch metadata from SEEK, check it, fetch blobs and check namespaces
        try:
            valid: bool = self.check()
        except InputAnalyseError as e:
            if e.reason is InputAnalyseErrorReason.URL_INVALID \
                    or e.reason is InputAnalyseErrorReason.URL_NO_CONTENT:
                logger.error("unable to contact SEEK, %s, %s", e.reason, e.reason.error_message)
                return e.reason.error_message, HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK

            if self.__metachecker.did_one_download_fail:
                logger.info("a least one download failed for %s", self.__link)
                return InputAnalyseErrorReason.DATA_FILE_NOT_FOUND.error_message, HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD

            logger.debug("abort, %s, %s, %s", e.reason, e.reason.error_message, self.__link)
            return e.reason.error_message, HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO

        if valid:
            # pass to morre-queue
            self._send()

        return "added {0} to queue".format(self.__link), HTTP_RETURN_CODE_SUCCESS_ADDED

    def _check(self) -> bool:
        """
        will check the link
        :return True, if valid
        """

        self.__metachecker: MetaChecker = MetaChecker(self.__link)
        return self.__metachecker.is_valid

    def _send(self) -> None:
        """
        will send the Link to the running Morre-Queue
        """
        self.__metachecker.
        # TODO
        raise NotImplementedError
