from pydantic import BaseModel
from datetime import date

class WeatherCreate(BaseModel):
    location: str
    start_date: date
    end_date: date

