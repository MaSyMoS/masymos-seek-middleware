import logging
from abc import abstractmethod, ABC

logger = logging.getLogger(__name__)


class MorreConnect(ABC):

    def __init__(self, url: str):
        if not url \
                or type(url) is not str \
                or url.strip() is "":
            logger.fatal("MorreInsert called with invalid url: %s", url)
            raise AttributeError("MorreInsert called with invalid url")

    @abstractmethod
    def send(self) -> bool:
        pass
