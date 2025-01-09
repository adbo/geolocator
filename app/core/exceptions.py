from fastapi import HTTPException
from starlette import status


class GeolocationNotFound(HTTPException):
    """Custom exception for when geolocation data is not found."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class IPStackAPIError(HTTPException):
    """Custom exception for errors when interacting with the IPStack API."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)
