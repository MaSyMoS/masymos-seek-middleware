from typing import Dict, Optional

import requests
import logging

import masemiwa.config as conf

from requests import HTTPError, Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

logger = logging.getLogger(__name__)


def download_file(url: str, headers: Dict = None) -> Optional[Response]:
    """
    downloads a file from any URL
    :param url: the URL
    :param headers: OPT the headers to pass to requests.get()
    :return: the Response or None on any known error (will log the error)
    """
    logger.debug("request file %s", url)
    r: Response = None
    try:
        if headers is None:
            r = requests.get(url, timeout=conf.Configuration.CONNECTION_TIMEOUT.value)
        else:
            r = requests.get(url, headers=headers, timeout=conf.Configuration.CONNECTION_TIMEOUT.value)
        r.raise_for_status()
    except ConnectTimeoutError or ConnectTimeout:
        logger.warning("timeout - unable to get file %s; Timeout!", url)
        return
    except HTTPError:
        code: str = 'unknown'
        if r:
            code = r.status_code

        logger.warning("unable to get file %s; HTTP-ErrorCode %s", url, code)
        return

    logger.debug("successfully got file %s", url)
    return r
