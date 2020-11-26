from enum import Enum, unique
from urllib.parse import ParseResult, urlparse

from masemiwa.morre_queue import MorreQueue

# this is the one and only Morre-Queue - a Thread runing in the background, managing the talking to Morre
the_queue = MorreQueue()


class ConfigurationException(Exception):
    pass


@unique
class Configuration(Enum):
    """
    the configuration AND the default configuration is stored here
    """
    CONNECTION_TIMEOUT = 10, int, "timeout in seconds for any request"
    MORRE_SERVER = urlparse(
        "http://yourServer:7474"), ParseResult, "the URL of the morre server to use (without '/morre/')"

    def __init__(self, default_value, value_type, explanation: str):
        print("uiui", self)

        # check
        if type(default_value) is not value_type:
            raise ConfigurationException(
                "critical error in default configuration; wrong configuration value type (%s); key %s",
                type(default_value), self)
        if type(explanation) is not str or explanation.strip() is "":
            raise ConfigurationException(
                "error in default configuration; explanation missing; key %s", self)

        # init
        self.__default_value: str = default_value
        self.__value_type = value_type
        self.__explanation: str = explanation

    def explanation(self) -> str:
        return self.__explanation
