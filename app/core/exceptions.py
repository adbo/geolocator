from fastapi import HTTPException
from starlette import status

class GeolocationNotFound(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class IPStackAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)