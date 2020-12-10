import logging
from masemiwa.listener.server_functions import app

logger = logging.getLogger(__name__)

"""

to start the server use a framework like gunicorn
gunicorn --bind 0.0.0.0:5000 start_server:app

"""

# TODO handle configuration


# debug mode
if __name__ == "__main__":
    app.run(debug=True)
