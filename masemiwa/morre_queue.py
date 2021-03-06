import atexit
import logging
import threading
from threading import Thread, Lock
from time import sleep

from masemiwa.input_analyser.beans import SeekContentBlob
from masemiwa.morre_gate.morre_annotations import MorreAnnotations
from masemiwa.morre_gate.morre_delete import MorreDelete
from masemiwa.morre_gate.morre_insert import MorreInsert

logger = logging.getLogger(__name__)


class MorreQueue(Thread):
    """
    this thread runs in the background and handles the interaction with MaSyMoS Morre
    thread starts automatically after calling `add_to_queue_and_start()`
    """
    __queue_delete: set
    __queue_insert: list
    __lock: Lock
    __has_been_started_yet: bool

    def __init__(self):
        super().__init__()
        self.__has_been_started_yet = False
        self.__stop_thread = False
        # make synchronise possible
        self.__lock = threading.Lock()
        # create queues
        # INSERT contains SeekContentBlob
        self.__queue_insert = []
        # DELETE contains str
        self.__queue_delete = set()

    def _add_to_insert_queue(self, add_queue=None) -> None:
        if add_queue is None:
            add_queue = []
        self.__lock.acquire()
        try:
            for s in add_queue:
                if type(s) is not SeekContentBlob:
                    raise TypeError("the list must contain SeekContentBlob only!")
                self.__queue_insert.append(s)
            logger.debug("added list with %d elements to Morre-INSERT-Queue", len(add_queue))
        finally:
            self.__lock.release()

    def _add_to_delete_queue(self, del_queue=None) -> None:
        if del_queue is None:
            del_queue = []
        self.__lock.acquire()
        try:
            s: str
            for s in del_queue:
                if type(s) is not str:
                    raise TypeError("the list must contain String only!")
                self.__queue_delete.add(s.strip())
            logger.debug("added list with %d elements to Morre-DELETE-Queue", len(del_queue))
        finally:
            self.__lock.release()

    def _add_to_update_queue(self, upd_queue=None) -> None:
        if upd_queue is None:
            upd_queue = []
        self.__lock.acquire()
        try:
            s: SeekContentBlob
            for s in upd_queue:
                if type(s) is not SeekContentBlob:
                    raise TypeError("the list must contain SeekContentBlob only!")
                self.__queue_delete.add(s.link_to_model)
                self.__queue_insert.append(s)
            logger.debug("added list with %d elements to Morre-UPDATE-Queue", len(upd_queue))
        finally:
            self.__lock.release()

    def add_to_insert_queue_and_eventually_start(self, add_queue=None) -> None:
        if add_queue is None:
            add_queue = []
        self._add_to_insert_queue(add_queue)
        if not self.is_alive():
            self.start()

    def add_to_delete_queue_and_eventually_start(self, url: str) -> None:
        self._add_to_delete_queue([url])
        if not self.is_alive():
            self.start()

    def add_to_update_queue_and_eventually_start(self, upd_queue=None) -> None:
        if upd_queue is None:
            upd_queue = []
        self._add_to_update_queue(upd_queue)
        if not self.is_alive():
            self.start()

    def _pop_from_insert_queue(self) -> SeekContentBlob:
        """
        :return: one element from INSERT queue
        """
        self.__lock.acquire()
        try:
            ret: SeekContentBlob = self.__queue_insert.pop()
        finally:
            self.__lock.release()
        return ret

    def _pop_from_delete_queue(self, specific: SeekContentBlob = None) -> str:
        """
        :return: one link from DELETE queue
        """
        self.__lock.acquire()
        try:
            if specific is not None:
                try:
                    self.__queue_delete.remove(specific.link_to_model)
                except KeyError:
                    # this error can be ignored
                    logger.debug("couldn't remove value '%s' from delete queue - not found", specific)
                ret: str = specific.link_to_model
            else:
                ret: str = self.__queue_delete.pop()
        finally:
            self.__lock.release()
        return ret

    @property
    def insert_queue_length(self) -> int:
        return len(self.__queue_insert)

    @property
    def delete_queue_length(self) -> int:
        return len(self.__queue_delete)

    @property
    def has_been_started_yet(self) -> bool:
        return self.__has_been_started_yet

    def run(self) -> None:
        """
        idea behind the runner:
        - delete all morre entries defines in delete queue
        - insert all entries defines in insert queue
            - check delete queue before every insert - if there is still an entry in the delete queue, this is an update
        - when queue is empty, run annotation index
        """
        logger.debug("start the Morre-Queue")
        self.__has_been_started_yet = True

        while True:

            inserted_something: bool = False
            while (len(self.__queue_insert) + len(self.__queue_delete)) > 0:
                if len(self.__queue_delete) > 0:
                    # send DELETE to Morre
                    next_delete: str = self._pop_from_delete_queue()
                    logger.debug("Q:DEL %s", next_delete)
                    delete: MorreDelete = MorreDelete(next_delete)
                    delete.send()
                    continue

                if len(self.__queue_insert) > 0:
                    inserted_something = True
                    next_insert: SeekContentBlob = self._pop_from_insert_queue()
                    logger.debug("Q:INS %s", next_insert)

                    if next_insert.link_to_model in self.__queue_delete:
                        # this is an UPDATE → fist delete, then insert
                        # send DELETE to Morre
                        next_delete: str = self._pop_from_delete_queue(next_insert)
                        logger.debug("Q:DEL2 %s", next_insert)
                        delete: MorreDelete = MorreDelete(next_delete)
                        delete.send()

                    # send INSERT to Morre
                    insert: MorreInsert = MorreInsert(next_insert)
                    insert.send()
                    # TODO handle a return false here with adding the blob/link to the backlog and try later
                    #  https://github.com/MaSyMoS/masymos-seek-middleware/issues/11

            if inserted_something:
                logger.debug("start Annotation Indexing")

                # Annotation Indexing
                annotations: MorreAnnotations = MorreAnnotations()
                annotations.send()

            sleep(1)
            if self.__stop_thread:
                logger.debug("stop the Morre-Queue")
                break

    @atexit.register
    def stop(self) -> None:
        """
        will stop the Thread
        """
        if self.is_alive:
            logger.debug("stopping the Morre-Queue requested")
        else:
            logger.debug("stopping the Morre-Queue requested, but queue is not running")
        self.__stop_thread = True


# this is the one and only Morre-Queue - a Thread running in the background, managing the talking to Morre
the_queue: MorreQueue


def init_morre_queue() -> None:
    global the_queue
    the_queue = MorreQueue()


init_morre_queue()
