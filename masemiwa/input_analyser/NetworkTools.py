from typing import Dict

import requests
import logging

from requests import HTTPError, Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

logger = logging.getLogger(__name__)


def download_file(url: str, headers: Dict = None) -> Response:
    logger.debug("request file %s", url)
    r: Response = None
    try:
        if headers is None:
            r = requests.get(url, timeout=5)
        else:
            r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
    except ConnectTimeoutError or ConnectTimeout:
        logger.warning("unable to get file %s; Timeout!", url)
        return None
    except HTTPError:
        code: str = 'unknown'
        if not r:
            code = r.status_code

        logger.warning("unable to get file %s; HTTP-ErrorCode %s", url, code)
        return None

    logger.debug("successfully got file %s")
    return r
