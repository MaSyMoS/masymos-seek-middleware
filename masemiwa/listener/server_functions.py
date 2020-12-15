import logging

from flask import Flask
from flask import request

from masemiwa.listener import E405_HTTP_RETURN_CODE_MALFORMED_REQUEST
from masemiwa.listener.delete import HandleDelete
from masemiwa.listener.insert import HandleInsert
from masemiwa.morre_queue import the_queue, init_morre_queue

logger = logging.getLogger(__name__)

app = Flask("MaSeMiWa")


def __check_if_valid_post_json_request(req: request, key_to_check: str = 'link') -> bool:
    if req.method == 'POST' \
            and req.is_json \
            and key_to_check in dict(req.get_json()) \
            and str(dict(req.get_json()).get(key_to_check)).strip() != "":
        return True
    return False


# define server functions

@app.route('/batch', methods=['POST'])
def batch() -> (str, int):
    if not __check_if_valid_post_json_request(request, key_to_check='links'):
        logger.warning("malformed BATCH-INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'links'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    links: list = list(dict(request.get_json()).get('links'))
    logger.debug("called BATCH: %s items", len(links))
    # TODO

    return "ok"


@app.route('/insert', methods=['POST'])
def insert() -> (str, int):
    # check if link is valid
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called INSERT: %s", link)
    i: HandleInsert = HandleInsert(link)

    return i.process()


@app.route('/delete', methods=['POST'])
def delete() -> (str, int):
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed DELETE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called DELETE: %s", link)
    d: HandleDelete = HandleDelete(link)

    return d.process()


@app.route('/update', methods=['POST'])
def update() -> (str, int):
    if not __check_if_valid_post_json_request(request):
        logger.warning("malformed UPDATE request")
        return "use POST and send json data with mime 'application/json' and field 'link'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called UPDATE: %s", link)
    # TODO update

    return "ok"


@app.route('/restart_queue', methods=['POST'])
def shutdown():
    logger.info("restating the morre queue was requested")
    if the_queue.is_alive:
        the_queue.stop()
    init_morre_queue()
    return "restarted"
