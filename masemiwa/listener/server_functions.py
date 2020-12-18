import logging

from flask import Flask
from flask import request

from masemiwa.listener import E405_HTTP_RETURN_CODE_MALFORMED_REQUEST, E200_HTTP_RETURN_CODE_SUCCESS_ADDED, \
    E503_HTTP_RETURN_CODE_MORRE_QUEUE_HAS_STOPPED
from masemiwa.listener.batch_insert import HandleBatch
from masemiwa.listener.delete import HandleDelete
from masemiwa.listener.insert import HandleInsert
from masemiwa.morre_queue import the_queue, init_morre_queue

logger = logging.getLogger(__name__)

app = Flask("MaSeMiWa")


def _check_if_valid_post_json_request(req: request, key_to_check: str = 'link') -> bool:
    if req.method == 'POST' \
            and req.is_json \
            and key_to_check in dict(req.get_json()) \
            and str(dict(req.get_json()).get(key_to_check)).strip() != "":
        return True
    return False


def _add_status_to_message(t: tuple = "unknown") -> (str, int):
    msg: str
    status: int = -1
    if type(t) is tuple and len(t) == 2:
        msg = t[0]
        if type(t[1]) is int:
            status = int(t[1])
    else:
        msg = str(t)

    return "{0} - {1}".format(status, msg), status


_E405_HTTP_RETURN_CODE_MALFORMED_REQUEST_RETURN_VALUE = (
    "use POST and send json data with mime 'application/json' and field 'link'",
    E405_HTTP_RETURN_CODE_MALFORMED_REQUEST)
_E503_ABORT_BECAUSE_MORRE_QUEUE_HAS_STOPPED_RETURN_VALUE = (
    "503 - Morre-Queue is not running; internal error, check the logs!", E503_HTTP_RETURN_CODE_MORRE_QUEUE_HAS_STOPPED)


def _abort_because_morre_queue_has_stopped() -> bool:
    """
    :return: true, if morre-queue was started but isn't running anymore
    """
    if the_queue.has_been_started_yet is False \
            or the_queue.is_alive():
        return False

    return True


# define server functions

@app.route('/batch', methods=['POST'])
def batch() -> (str, int):
    if not _check_if_valid_post_json_request(request, key_to_check='links'):
        logger.warning("malformed BATCH-INSERT request")
        return "use POST and send json data with mime 'application/json' and field 'links'", E405_HTTP_RETURN_CODE_MALFORMED_REQUEST

    if _abort_because_morre_queue_has_stopped():
        return _E503_ABORT_BECAUSE_MORRE_QUEUE_HAS_STOPPED_RETURN_VALUE

    links: list = list(dict(request.get_json()).get('links'))
    logger.debug("called BATCH: %s items", len(links))
    b: HandleBatch = HandleBatch(links)

    return _add_status_to_message(b.process())


@app.route('/insert', methods=['POST'])
def insert() -> (str, int):
    # check if link is valid
    if not _check_if_valid_post_json_request(request):
        logger.warning("malformed INSERT request")
        return _E405_HTTP_RETURN_CODE_MALFORMED_REQUEST_RETURN_VALUE

    if _abort_because_morre_queue_has_stopped():
        return _E503_ABORT_BECAUSE_MORRE_QUEUE_HAS_STOPPED_RETURN_VALUE

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called INSERT: %s", link)
    i: HandleInsert = HandleInsert(link)

    return _add_status_to_message(i.process())


@app.route('/delete', methods=['POST'])
def delete() -> (str, int):
    if not _check_if_valid_post_json_request(request):
        logger.warning("malformed DELETE request")
        return _E405_HTTP_RETURN_CODE_MALFORMED_REQUEST_RETURN_VALUE

    if _abort_because_morre_queue_has_stopped():
        return _E503_ABORT_BECAUSE_MORRE_QUEUE_HAS_STOPPED_RETURN_VALUE

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called DELETE: %s", link)
    d: HandleDelete = HandleDelete(link)

    return _add_status_to_message(d.process())


@app.route('/update', methods=['POST'])
def update() -> (str, int):
    if not _check_if_valid_post_json_request(request):
        logger.warning("malformed UPDATE request")
        return _E405_HTTP_RETURN_CODE_MALFORMED_REQUEST_RETURN_VALUE

    if _abort_because_morre_queue_has_stopped():
        return _E503_ABORT_BECAUSE_MORRE_QUEUE_HAS_STOPPED_RETURN_VALUE

    link: str = str(dict(request.get_json()).get('link')).strip()
    logger.debug("called UPDATE: %s", link)
    # TODO update

    return _add_status_to_message(("ok", E200_HTTP_RETURN_CODE_SUCCESS_ADDED))


@app.route('/restart_queue', methods=['POST'])
def shutdown():
    logger.info("restating the morre queue was requested")
    if the_queue.is_alive:
        the_queue.stop()
    init_morre_queue()
    return _add_status_to_message(("restarted", E200_HTTP_RETURN_CODE_SUCCESS_ADDED))
