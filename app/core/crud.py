from sqlmodel import Session, select

from db.models import Geolocation
from utils.ipstack_client import get_geolocation_data
from core.exceptions import IPStackAPIError
from sqlalchemy.exc import SQLAlchemyError


def get_geolocation_from_db(db: Session, ip_or_url: str):
    """Retrieves geolocation data from the database by IP address or URL."""
    try:
        return db.exec(
            select(Geolocation).where(Geolocation.ip_or_url == ip_or_url)
        ).first()
    except SQLAlchemyError as e:
        raise


def get_or_create_geolocation(db: Session, ip_or_url: str):
    """
    Retrieves geolocation data from the database or creates it if it doesn't exist.

    Fetches data from the IPStack API if not found in the database.
    """
    geolocation_db = get_geolocation_from_db(db, ip_or_url)
    if geolocation_db:
        return geolocation_db, False

    try:
        geolocation_data = get_geolocation_data(ip_or_url)
    except IPStackAPIError as e:
        raise

    geolocation_fields = {
        "ip": geolocation_data.get("ip"),
        "ip_or_url": ip_or_url,
        "continent_code": geolocation_data.get("continent_code"),
        "continent_name": geolocation_data.get("continent_name"),
        "country_code": geolocation_data.get("country_code"),
        "country_name": geolocation_data.get("country_name"),
        "region_name": geolocation_data.get("region_name"),
        "city": geolocation_data.get("city"),
        "latitude": geolocation_data.get("latitude"),
        "longitude": geolocation_data.get("longitude"),
        "raw_data": geolocation_data,
    }

    geolocation = Geolocation(**geolocation_fields)
    try:
        db.add(geolocation)
        db.commit()
        db.refresh(geolocation)
        return geolocation, True
    except SQLAlchemyError as e:
        db.rollback()
        raise


def delete_geolocation_from_db(db: Session, ip_or_url: str):
    """Deletes geolocation data from the database by IP address or URL."""
    geolocation = db.exec(
        select(Geolocation).where(Geolocation.ip_or_url == ip_or_url)
    ).first()

    if geolocation:
        try:
            db.delete(geolocation)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise
    return False
