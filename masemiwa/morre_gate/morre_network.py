import logging
from typing import Optional
from urllib.error import HTTPError

import requests
from requests import Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError, NewConnectionError

import masemiwa.config as conf

_MODEL_UPDATE_SERVICE_URL = "/morre/model_update_service/"

logger = logging.getLogger(__name__)


def _prepare_url(module: str):
    return conf.Configuration.MORRE_SERVER.value + _MODEL_UPDATE_SERVICE_URL + module


# noinspection PyUnboundLocalVariable
def send_post_request_with_json(module: str, data: dict) -> Optional[dict]:
    """
    :param module: the last part of the URL. i.e. `add_module`
    :param data: the JSON to send
    :return: the returning JSON as dict
    """

    url: str = _prepare_url(module)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8"
    }

    logger.debug("send request to morre %s %s %s", url, data, headers)
    r: Response
    try:
        r = requests.post(url, data=str(data),
                          headers=headers, timeout=conf.Configuration.CONNECTION_TIMEOUT_MORRE.value)
        r.raise_for_status()
    except (ConnectionError, NewConnectionError, OSError) as e:
        logger.warning("unable to make Morre request %s; Connection not possible!(%s)", url, e)
        return
    except (ConnectTimeoutError, ConnectTimeout):
        logger.warning("timeout - unable to make Morre request %s; Timeout!", url)
        return
    except HTTPError:
        code: str = 'unknown'
        try:
            r
        except NameError:
            # r is not defined - ignore
            pass
        else:
            code = r.status_code

        logger.warning("unable to make request %s; HTTP-ErrorCode %s", url, code)
        return

    logger.debug("successfully got feedback %s", url)
    return r.json()


def process_response(response, success_msg: str = "success", error_msg: str = "error") -> bool:
    """
    checks, if morre response is OK
    :param response: morre's response
    :param success_msg: the logging message to display on success
    :param error_msg: the logging message to display on error
    :return: True, if OK, else False
    """

    if response \
            and response.get('ok') is not None \
            and str(response.get('ok')).strip().lower() == "true":
        logger.info(success_msg)
        return True

    response_message: str = ""
    if response \
            and response.get('message') is not None:
        response_message = response.get('message')

    logger.info("%s|%s", error_msg, response_message)
    return False
