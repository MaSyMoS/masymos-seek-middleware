import logging
import atexit

from masemiwa import log_configuration
from masemiwa.listener.server_functions import app
from masemiwa.morre_queue import MorreQueue, the_queue
import masemiwa.config as config

"""

to start the server use a framework like gunicorn
gunicorn --bind 0.0.0.0:5000 start_server:app

"""

# fallback logger (if misconfiguration in configuration/log configuration)
logging.basicConfig(level=logging.DEBUG)

config.reload_configuration()

# load external log configuration
log_configuration.reload_log_configuration()
logger = logging.getLogger(__name__)

logger.info("started MaSeMiWa ----------------------------------------------------------------------------------------")

# debug mode
if __name__ == "__main__":
    app.run(debug=True)
