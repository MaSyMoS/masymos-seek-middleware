import threading
from lib2to3.patcomp import _type_of_literal
from threading import Thread

import logging

logger = logging.getLogger(__name__)


class MorreQueue(Thread):
    """
    this thread runs in the background and handles the interaction with MaSyMoS Morre
    thread starts automatically after calling `add_to_queue_and_start()`
    """

    def __init__(self, start_queue: list = []):
        """
        :param start_queue: list of str - contains a list or content_blob-URLs
        """
        super().__init__()
        # make synchronise possible
        self.__lock = threading.Lock()
        # create the start list
        self.__queue: list = []
        self._add_to_queue(start_queue)

    def _add_to_queue(self, add_queue: list = []) -> None:
        self.__lock.acquire()
        try:
            for s in add_queue:
                if type(s) is not str:
                    raise TypeError("the list must contain strings only!")
                self.__queue.append(s)
            logger.debug("added list with %d elements to Morre-Queue", len(add_queue))
        finally:
            self.__lock.release()

    def add_to_queue_and_start(self, add_queue: list = []) -> None:
        self._add_to_queue(add_queue)
        self.start()

    def _pop(self) -> str:
        self.__lock.acquire()
        try:
            ret: str = self.__queue.pop()
        finally:
            self.__lock.release()
        return ret

    @property
    def queue_length(self) -> int:
        return len(self.__queue)

    def run(self) -> None:
        logger.debug("start the Morre-Queue")

        while len(self.__queue) is not 0:
            next: str = self._pop()
            # TODO talk to Morre

        logger.debug("finish the Morre-Queue")
