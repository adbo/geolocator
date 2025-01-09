from pydantic import BaseModel


class GeolocationCreate(BaseModel):
    ip_or_url: str
