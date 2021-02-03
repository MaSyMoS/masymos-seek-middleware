import os
from configparser import ConfigParser
from enum import Enum, unique

MASEMIWA_VERSION: str = "1.0.1"

CONFIGURATION_FILE: str = '/opt/config/masemiwa.cfg'
CONFIGURATION_DEFAULT_SECTION: str = 'MaSeMiWa'


class ConfigurationException(Exception):
    pass


class ConfigurationFileException(Exception):
    pass


@unique
class Configuration(Enum):
    """
    the configuration AND the default configuration is stored here
    """
    CONNECTION_TIMEOUT = 10, int, "timeout in seconds for any non-morre request"
    CONNECTION_TIMEOUT_MORRE = 542, int, "timeout in seconds for any morre request"
    MORRE_SERVER = "http://masymos_neo4j:7474", str, "the URL of the morre server to use (without '/morre/')"
    LOG_CONFIGURATION_FILE = "/opt/config/masemiwa_log.cfg", str, "the absolute path to the log-configuration-file"

    __default_value: str
    __value: str
    __value_type: type
    __explanation: str

    def __init__(self, default_value, value_type: type, explanation: str):

        self._check(default_value, explanation, value_type)

        # init
        self.__default_value = default_value
        self.__value = default_value
        self.__value_type = value_type
        self.__explanation = explanation

    def _check(self, new_value, explanation, value_type: type):
        if type(new_value) != value_type:
            raise ConfigurationException(
                "error in configuration; wrong configuration value type (%s); key %s",
                type(new_value), self)
        if type(explanation) is not str or explanation.strip() == "":
            raise ConfigurationException(
                "error in configuration; explanation missing; key %s", self)

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


def reload_configuration() -> None:
    """
    will try to reload the configuration from disk
    if there is no configuration file, it will be created
    """
    # check, if file exists
    if not os.path.exists(CONFIGURATION_FILE) \
            or os.path.getsize(CONFIGURATION_FILE) == 0:
        _overwrite_config_file()
    else:
        # load configuration
        _load_configuration_from_file()


def _overwrite_config_file() -> None:
    config_parser: ConfigParser = ConfigParser(allow_no_value=True)

    config_parser.add_section(CONFIGURATION_DEFAULT_SECTION)

    key: Configuration
    for key in Configuration:
        config_parser.set(CONFIGURATION_DEFAULT_SECTION, "; {1} ({0})".format(key.value_type, key.explanation))
        config_parser.set(CONFIGURATION_DEFAULT_SECTION, str(key.name), str(key.default_value))

    with open(CONFIGURATION_FILE, 'w') as fp:
        config_parser.write(fp)


def _load_configuration_from_file() -> None:
    config_parser: ConfigParser = ConfigParser(allow_no_value=True)
    config_parser.read(CONFIGURATION_FILE)

    # check section
    if not config_parser.has_section(CONFIGURATION_DEFAULT_SECTION):
        raise ConfigurationFileException("the main section '{0}' is missing".format(CONFIGURATION_DEFAULT_SECTION))

    # check keys and values
    config_items: list = [item for item in Configuration]
    good_items = _check_config_keys_and_values(config_parser[CONFIGURATION_DEFAULT_SECTION].items(), config_items)

    # all checks done, overwrite the configuration!
    good_key: str
    good_value: any
    for (good_key, good_value) in good_items:
        for item in config_items:
            if item.name != good_key.upper():
                continue
            item.set(good_value)


def _check_config_keys_and_values(config_parser: list, config_items: list) -> list:
    """
    :param config_parser: list of tuples (key,value)
    :param config_items: [item for item in Configuration]
    :return:
    """
    known_keys: list = [item.name for item in config_items]
    # collect all good (key,value) tuples in this list
    good_items: list = []
    key: str
    value: str
    for (key, value) in config_parser:

        # all keys must be known
        if key.upper() not in known_keys:
            raise ConfigurationFileException(
                "the configuration file defines an unknown key '{0}'; known keys: {1}".format(key, known_keys))

        # the values must have the right type
        item: Configuration
        for item in config_items:
            if item.name != key.upper():
                continue

            try:
                value_with_right_type = item.value_type(value)
                if type(value_with_right_type) is not item.value_type:
                    raise ValueError()
            except ValueError:
                raise ConfigurationFileException(
                    "value of {0} cannot be converted to type {1}".format(key, item.value_type))

            good_items.append((key, value_with_right_type))
    return good_items
