import logging
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import ParseResult, urljoin

import requests

from masemiwa import config
from requests import Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

_MODEL_UPDATE_SERVICE_URL = "/morre/model_update_service/"

logger = logging.getLogger(__name__)


def _prepare_url(module: str):
    return config.Configuration.MORRE_SERVER.value + _MODEL_UPDATE_SERVICE_URL + module


def _send_post_request_with_json(module: str, data: dict) -> Optional[dict]:
    """
    :param module: the last part of the URL. i.e. `add_modul`
    :param data: the JSON to send
    :return: the returning JSON as dict
    """

    url: str = _prepare_url(module)
    headers = {
        "Content-Type": "application/json",
        "Accept-Charset": "UTF-8"
    }

    logger.debug("send request to morre %s", url)
    r: Response = None
    try:
        r = requests.post(url, data=data,
                          headers=headers, timeout=config.Configuration.CONNECTION_TIMEOUT_MORRE.value)
        r.raise_for_status()
    except ConnectTimeoutError or ConnectTimeout:
        logger.warning("timeout - unable to make request %s; Timeout!", url)
        return
    except HTTPError:
        code: str = 'unknown'
        if r:
            code = r.status_code

        logger.warning("unable to make request %s; HTTP-ErrorCode %s", url, code)
        return

    logger.debug("successfully got feedback %s", url)
    return r
