import logging
from .listener.server_functions import app

logger = logging.getLogger(__name__)




# TODO handle configuration



# debug mode
if __name__ == "__main__":
    app.run(debug=True)
