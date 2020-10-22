from typing import List

import logging

logger = logging.getLogger(__name__)

mime_type_allow_list: List = ['application/sbml+xml', \
                              'application/xml', \
                              'text/xml']


def check_mime_type(mime: str) -> bool:
    """
    checks the MIME type from SEEK-JSON against allow-list
    """
    return mime in mime_type_allow_list
