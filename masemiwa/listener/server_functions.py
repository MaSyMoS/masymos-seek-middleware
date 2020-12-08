from flask import Flask
from flask import request
import logging

from masemiwa.input_analyser import InputAnalyseError, InputAnalyseErrorReason
from masemiwa.listener import E405_HTTP_RETURN_CODE_MALFORMED_REQUEST
from masemiwa.listener.delete import handle_delete
from masemiwa.listener.insert import handle_insert

logger = logging.getLogger(__name__)

app = Flask("MaSeMiWa")


def __check_if_valid_post_json_request(request: request, key_to_check: str = 'link') -> bool:
    if request.method == 'POST' \
            and request.is_json \
            and key_to_check in dict(request.get_json()) \
            and str(dict(request.get_json()).get(key_to_check)).strip() is not "":
        return True
    return False


# define server functions

@app.route('/batch', methods=['POST'])
def batch() -> (str, int):
    if not __check_if_valid_post_json_request(request, key_to_check='links'):
        logger.warning("malformed BATCH-INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'links'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    links: list = list(dict(request.get_json()).get('links'))
    # TODO

    return "ok"


@app.route('/insert', methods=['POST'])
def insert() -> (str, int):
    # check if link is valid
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    i: handle_insert = handle_insert(link)

    return i.process()


@app.route('/delete', methods=['POST'])
def delete() -> (str, int):
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed DELETE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    d: handle_insert = handle_delete(link)

    return d.process()


@app.route('/update', methods=['POST'])
def update() -> (str, int):
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed UPDATE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    # TODO delete
    # ToDo insert

    return "ok"
