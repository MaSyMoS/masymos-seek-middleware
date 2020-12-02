from abc import abstractmethod, ABC

E200_HTTP_RETURN_CODE_SUCCESS_ADDED: int = 200
E204_HTTP_RETURN_CODE_SUCCESS_NOTHING_TO_DO: int = 204
E404_HTTP_RETURN_CODE_NO_CONNECTION_TO_SEEK: int = 404
E405_HTTP_RETURN_CODE_MALFORMED_REQUEST: int = 405
E502_HTTP_RETURN_CODE_NO_CONNECTION_TO_FILE_DOWNLOAD: int = 502
E500_HTTP_RETURN_CODE_INTERNAL_ERROR = 500


class HandleIO(ABC):
    """
    handles all DELETE logic for a single model link (can have several content_blob)
    """

    @abstractmethod
    def process(self) -> (str, int):
        pass

    @abstractmethod
    def _send(self) -> bool:
        pass
