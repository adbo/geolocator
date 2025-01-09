from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import JSON


class Geolocation(SQLModel, table=True):
    """Represents geolocation data stored in the database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: Optional[str] = Field(index=True)
    ip_or_url: str = Field(unique=True, index=True)
    continent_code: Optional[str] = None
    continent_name: Optional[str] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    region_name: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[Decimal]
    longitude: Optional[Decimal]
    raw_data: Optional[dict] = Field(sa_type=JSON)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, sa_column_kwargs={'onupdate': datetime.now})