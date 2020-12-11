# this is the default log configuration
# if the log-config-file doesn't exist, this content will be written to this file
import logging
import logging.config
import os

from masemiwa.config import Configuration

_log_default_config = """
[loggers]
keys=root

[formatters]
keys=formatter1

[handlers]
keys=stream, file

[formatter_formatter1]
format=%(asctime)s %(threadName)s [%(levelname)s] %(name)s|%(filename)s:%(lineno)d | %(message)s

[handler_stream]
class=StreamHandler
args=()
formatter=formatter1

[handler_file]
class=FileHandler
args=("/opt/logs/masemiwa.log", "a")
formatter=formatter1

[logger_root]
handlers=stream, file
level=DEBUG
"""


def _overwrite_config_file():
    with open(Configuration.LOG_CONFIGURATION.value, 'w') as fp:
        fp.write(_log_default_config)


def reload_log_configuration():
    conf_file = Configuration.LOG_CONFIGURATION.value
    new_log_file: bool = False

    # check, if file exists
    if not os.path.exists(conf_file) \
            or os.path.getsize(conf_file) == 0:
        _overwrite_config_file()
        new_log_file = True

    # load log configuration
    logging.config.fileConfig(conf_file, disable_existing_loggers=False)

    logger = logging.getLogger(__name__)
    if new_log_file:
        logger.info("created new log configuration file in %s", conf_file)
    else:
        logger.info("successfully loaded log configuration file from %s", conf_file)
