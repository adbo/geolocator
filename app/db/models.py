from typing import Optional
from sqlmodel import SQLModel, Field, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Numeric


class Geolocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: Optional[str] = Field(index=True)
    ip_or_url: str = Field(unique=True, index=True)
    continent_code: Optional[str] = None
    continent_name: Optional[str] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    region_name: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[Numeric] = Field(sa_column_kwargs={"type_": Numeric(precision=9, scale=6)})
    longitude: Optional[Numeric] = Field(sa_column_kwargs={"type_": Numeric(precision=9, scale=6)})
    raw_data: Optional[dict] = None
    created_at: Optional[DateTime] = Field(default_factory=func.now)
    updated_at: Optional[DateTime] = Field(default_factory=func.now, sa_column_kwargs={"onupdate": func.now()})