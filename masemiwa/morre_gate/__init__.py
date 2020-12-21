import logging
from abc import abstractmethod, ABC

logger = logging.getLogger(__name__)


class MorreConnect(ABC):

    @abstractmethod
    def send(self) -> bool:
        pass
