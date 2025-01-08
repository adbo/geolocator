from sqlmodel import Session, select

from db.models import Geolocation
from utils.ipstack_client import get_geolocation_data

def get_geolocation(db: Session, ip_or_url: str, force_refresh: bool = False):
    geolocation_db = db.exec(select(Geolocation).where(Geolocation.ip_or_url == ip_or_url)).first()

    if geolocation_db and not force_refresh:
        return geolocation_db

    geolocation_data = get_geolocation_data(ip_or_url)
    print(geolocation_data)

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
        "raw_data": geolocation_data
    }

    geolocation = Geolocation(**geolocation_fields)
    db.add(geolocation)
    db.commit()
    return geolocation