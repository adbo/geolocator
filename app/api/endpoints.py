from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import Session

from core.crud import (
    get_geolocation_from_db,
    get_or_create_geolocation,
    delete_geolocation_from_db,
)
from core.exceptions import GeolocationNotFound, IPStackAPIError
from db.database import get_db
from db.models import Geolocation
from schemas.geolocation import GeolocationCreate

router = APIRouter()


@router.get("/geolocations/{ip_or_url}", response_model=Geolocation)
def read_geolocation(ip_or_url: str, db: Session = Depends(get_db)):
    """
    Retrieves geolocation data for a given IP address or URL.

    Args:
        ip_or_url: The IP address or URL to look up.
        db: The database session.

    Returns:
        The geolocation data.

    Raises:
        GeolocationNotFound: If no geolocation data is found.
    """
    geolocation = get_geolocation_from_db(db, ip_or_url)
    if not geolocation:
        raise GeolocationNotFound(detail=f"Geolocation for '{ip_or_url}' not found")
    return geolocation


@router.post(
    "/geolocations", response_model=Geolocation, status_code=status.HTTP_201_CREATED
)
def create_geolocation(
    response: Response, geolocation_in: GeolocationCreate, db: Session = Depends(get_db)
):
    """
    Creates or retrieves geolocation data for a given IP address or URL.

    If the geolocation data already exists, it returns the existing data with a 200 OK status.
    Otherwise, it fetches the data from the IPStack API, saves it to the database, and returns it with a 201 Created status.

    Args:
        response: The FastAPI response object.
        geolocation_in: The input data containing the IP address or URL.
        db: The database session.

    Returns:
        The created or existing geolocation data.

    Raises:
        HTTPException: If there is an error connecting to the IPStack API.
    """
    try:
        geolocation, created = get_or_create_geolocation(db, geolocation_in.ip_or_url)
        if not created:
            response.status_code = status.HTTP_200_OK
        return geolocation
    except IPStackAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


@router.delete("/geolocations/{ip_or_url}", status_code=status.HTTP_204_NO_CONTENT)
def delete_geolocation(ip_or_url: str, db: Session = Depends(get_db)):
    """
    Deletes geolocation data for a given IP address or URL.

    Args:
        ip_or_url: The IP address or URL to delete.
        db: The database session.

    Returns:
        None

    Raises:
        GeolocationNotFound: If no geolocation data is found to delete.
    """
    if not delete_geolocation_from_db(db, ip_or_url):
        raise GeolocationNotFound(detail=f"Geolocation for '{ip_or_url}' not found")
    return None
