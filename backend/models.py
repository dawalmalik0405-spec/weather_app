from sqlalchemy import column
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)

    location = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    start_date = Column(Date)
    end_date = Column(Date)

    temperature = Column(Float)
    humidity = Column(Float)

    weather_condition = Column(String)

    map_url = Column(String)

    created_at = Column(DateTime)

    forecasts = relationship(
        "ForecastRecord",
        back_populates="weather_record"
    )


class ForecastRecord(Base):
    __tablename__ = "forecast_records"

    id = Column(Integer, primary_key=True)

    weather_record_id = Column(
        Integer,
        ForeignKey("weather_records.id")
    )

    forecast_date = Column(Date)

    max_temp = Column(Float)

    min_temp = Column(Float)

    condition = Column(String)

    weather_record = relationship(
        "WeatherRecord",
        back_populates="forecasts"
    )