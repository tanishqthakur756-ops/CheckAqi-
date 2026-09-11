"""
SQLAlchemy ORM models — map directly to the tables in schema.sql.

These are the database-side representation of Contracts A and B.
"""

from sqlalchemy import Column, Text, Float, Integer, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func

from .db import Base


class District(Base):
    __tablename__ = "districts"

    district_id = Column(Text, primary_key=True)
    lgd_code = Column(Text, unique=True)
    name = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)


class Station(Base):
    __tablename__ = "stations"

    station_id = Column(Text, primary_key=True)
    station_name = Column(Text)
    district_id = Column(Text, ForeignKey("districts.district_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    source = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)


class DailyReading(Base):
    __tablename__ = "daily_readings"

    station_id = Column(Text, ForeignKey("stations.station_id"), primary_key=True)
    date = Column(Date, primary_key=True)
    aqi = Column(Float)
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    no2 = Column(Float)
    temperature = Column(Float)
    rainfall_mm = Column(Float)
    wind_speed_kmh = Column(Float)
    data_type = Column(Text, default="observed")
    source = Column(Text, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())


class DistrictRollup(Base):
    __tablename__ = "district_rollups"

    district_id = Column(Text, ForeignKey("districts.district_id"), primary_key=True)
    date = Column(Date, primary_key=True)
    avg_aqi = Column(Float)
    max_aqi = Column(Float)
    avg_temp = Column(Float)
    avg_rainfall = Column(Float)
    avg_wind = Column(Float)  # FIX: was missing -- wind_correlation had nothing real to read
    season = Column(Text)
    station_count = Column(Integer, default=0)
    coverage_type = Column(Text)


class Source(Base):
    __tablename__ = "sources"

    source_name = Column(Text, primary_key=True)
    source_url = Column(Text)
    license_note = Column(Text)
    last_synced_at = Column(DateTime(timezone=True))
