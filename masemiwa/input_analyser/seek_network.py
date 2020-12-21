import logging
from typing import Dict, Optional

import requests
from requests import HTTPError, Response, ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

import masemiwa.config as conf
from masemiwa.input_analyser.beans import SeekUrl, SeekContentBlob

logger = logging.getLogger(__name__)


# noinspection PyUnboundLocalVariable
def _download_file(url: str, headers: Dict = None) -> Optional[Response]:
    """
    downloads a file from any URL
    :param url: the URL
    :param headers: OPT the headers to pass to requests.get()
    :return: the Response or None on any known error (will log the error)
    """
    logger.debug("request file %s", url)
    r: Response
    try:
        if headers is None:
            r = requests.get(url, timeout=conf.Configuration.CONNECTION_TIMEOUT.value)
        else:
            r = requests.get(url, headers=headers, timeout=conf.Configuration.CONNECTION_TIMEOUT.value)
        r.raise_for_status()
    except (ConnectTimeoutError, ConnectTimeout) as e:
        logger.warning("timeout - unable to get file %s; Timeout! %s", url, e)
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

        logger.warning("unable to get file %s; HTTP-ErrorCode %s", url, code)
        return

    logger.debug("successfully got file %s", url)
    return r


def download_seek_metadata(seek_url: SeekUrl) -> Optional[dict]:
    """
    get json meta data from a seek object
    :param seek_url: the url o.O
    :return: None on Error else json-filled-dict, hopefully
    """

    headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Charset": "UTF-8"
    }

    r: Response = _download_file(seek_url.url + ".json", headers=headers)
    if r is None:
        return
    return r.json()


def download_blob_content(blob: SeekContentBlob) -> Optional[str]:
    """
    get XML for content_blob-link
    :param blob: the SeekContentBlob object
    :return: None on Error else xml as text
    """

    r: Response = _download_file(blob.link + "/download")
    if r is None:
        return
    return r.text
