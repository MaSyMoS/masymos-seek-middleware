import threading
from lib2to3.patcomp import _type_of_literal
from threading import Thread

import logging

logger = logging.getLogger(__name__)


class MorreQueue(Thread):
    """
    this thread runs in the background and handles the interaction with MaSyMoS Morre
    """

    def __init__(self, start_queue: list = []):
        super().__init__()
        # make synchronise possible
        self.__lock = threading.Lock()
        # create the start list
        self.__queue: list = []
        self.add_to_queue(start_queue)

    def add_to_queue(self, add_queue: list = []) -> None:
        self.__lock.acquire()
        try:
            for s in add_queue:
                if type(s) is not str:
                    raise TypeError("the list must contain strings only!")
                self.__queue.append(s)
            logger.debug("added list with %d elements to Morre-Queue", len(list))
        finally:
            self.__lock.release()

    @property
    def queue_length(self) -> int:
        return len(self.__queue)

    def run(self) -> None:
        logger.debug("start the Morre-Queue")
        # TODO
        logger.debug("finish the Morre-Queue")
