from flask import Flask
from flask import request
import logging

logger = logging.getLogger(__name__)

app = Flask("MaSeMiWa")

__HTTP_RETURN_CODE_SUCCESS_ADDED: int = 200
__HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO: int = 204
__HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK: int = 404
__HTTP_RETURN_CODE_MALFORMED_REQUEST: int = 405
__HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD: int = 502


def __check_if_valid_post_json_request(request: request, key_to_check: str = 'link') -> bool:
    if request.method == 'POST' \
            and request.is_json \
            and key_to_check in dict(request.get_json()) \
            and str(dict(request.get_json()).get(key_to_check)).strip() is not "":
        return True
    return False


# define server functions

@app.route('/batch', methods=['POST'])
def insert():
    if not __check_if_valid_post_json_request(request, key_to_check='links'):
        logger.warning("malformed BATCH-INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'links'", __HTTP_RETURN_CODE_MALFORMED_REQUEST

    links: list = list(dict(request.get_json()).get('links'))
    # TODO

    return "ok"


@app.route('/insert', methods=['POST'])
def insert():
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'link'", __HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    # TODO

    return "ok"


@app.route('/delete', methods=['POST'])
def insert():
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed DELETE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", __HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    # TODO

    return "ok"


@app.route('/update', methods=['POST'])
def insert():
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed UPDATE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", __HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    # TODO delete
    # ToDo insert

    return "ok"
