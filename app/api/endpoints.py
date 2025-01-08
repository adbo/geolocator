from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.crud import get_geolocation
from db.database import get_db
from db.models import Geolocation

router = APIRouter()

@router.get("/geolocations/{ip_or_url}", response_model=Geolocation)
def read_geolocation(ip_or_url: str, db: Session = Depends(get_db)):
    return get_geolocation(db, ip_or_url)