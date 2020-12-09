from enum import Enum, unique


class ConfigurationException(Exception):
    pass


@unique
class Configuration(Enum):
    """
    the configuration AND the default configuration is stored here
    """
    CONNECTION_TIMEOUT = 10, int, "timeout in seconds for any non-morre request"
    CONNECTION_TIMEOUT_MORRE = 542, int, "timeout in seconds for any morre request"
    MORRE_SERVER = "http://127.0.0.1:7474", str, "the URL of the morre server to use (without '/morre/')"

    def __init__(self, default_value, value_type:type, explanation: str):

        self._check(default_value, explanation, value_type)

        # init
        self.__default_value: str = default_value
        self.__value: str = default_value
        self.__value_type = value_type
        self.__explanation: str = explanation

    def _check(self, new_value, explanation, value_type:type):
        if type(new_value) != value_type:
            raise ConfigurationException(
                "critical error in default configuration; wrong configuration value type (%s); key %s",
                type(new_value), self)
        if type(explanation) is not str or explanation.strip() == "":
            raise ConfigurationException(
                "error in default configuration; explanation missing; key %s", self)

    def set(self, value) -> None:
        self._check(value, self.explanation, self.value_type)
        self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def default_value(self):
        return self.__default_value

    @property
    def value_type(self) -> type:
        return self.__value_type

    @property
    def explanation(self) -> str:
        return self.__explanation
