import logging
from abc import abstractmethod, ABC

from masemiwa.input_analyser.beans import SeekContentBlob

logger = logging.getLogger(__name__)


class MorreConnect(ABC):

    def __init__(self, blob: SeekContentBlob):
        if not blob \
                or type(blob) is not SeekContentBlob \
                or blob.link.strip() is "":
            logger.fatal("MorreInsert called with invalid content_blob: %s", blob)
            raise AttributeError("MorreInsert called with invalid content_blob")

    @abstractmethod
    def send(self) -> bool:
        pass
