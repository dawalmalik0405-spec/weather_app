from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from routes.weater import WeatherCreate
from services.validation_service import validate_date_range
from services.geocoding_service import get_coordinates,get_location_suggestions
from services.weather_service import get_weather,get_forecast

import json

from models import WeatherRecord,ForecastRecord

import csv
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.post("/")
def create_weather(
    request: WeatherCreate,
    db: Session = Depends(get_db)
):
    
    validate_date_range(
        request.start_date,
        request.end_date
    )

    coordinates = get_coordinates(
        request.location
    )

    if coordinates is None:
        raise HTTPException(
            status_code=400,
            detail="location not found"
        )

    weather = get_weather(
        coordinates["latitude"],
        coordinates["longitude"]
    )

    forecast = get_forecast(
        coordinates["latitude"],
        coordinates["longitude"],
        request.start_date,
        request.end_date
    )


    record = WeatherRecord(
        location=request.location,

        latitude=coordinates["latitude"],
        longitude=coordinates["longitude"],

        start_date=request.start_date,
        end_date=request.end_date,

        temperature=weather["temperature"],
        humidity=weather["humidity"],

        weather_condition=(
            forecast[0]["condition"]
            if forecast
            else "Unknown"
        ),

        map_url=f"https://maps.google.com/?q={coordinates['latitude']},{coordinates['longitude']}",

        created_at=datetime.utcnow()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    for day in forecast:

        forecast_record = ForecastRecord(
            weather_record_id=record.id,

            forecast_date=datetime.strptime(
                day["date"],
                "%Y-%m-%d"
            ).date(),

            max_temp=day["max_temp"],

            min_temp=day["min_temp"],

            condition=day["condition"]
        )
        
        db.add(forecast_record)

    db.commit()

    

    return {
        "id":record.id,
        "location": request.location,
        "current_weather":weather,
        "forecast":forecast,
        "latitude": coordinates["latitude"],
        "longitude":coordinates["longitude"],
        "matched_location": coordinates["name"],
        "country": coordinates.get("country"),
        "map_url": record.map_url
    }



@router.get("/")
def get_all_weather(
    db:Session = Depends(get_db)
):
    
    records = db.query(
        WeatherRecord
    ).all()

    return records


@router.get("/search")
def search_locations(
    query: str
):
    coordinates = get_location_suggestions(
        query
    )

    return coordinates


@router.get("/{id}")
def get_weather_id(
    id:int,
    db:Session = Depends(get_db)
):
    
    
    records = db.query(
        WeatherRecord
    ).filter(
        WeatherRecord.id == id
    ).first()
 
    if not records:
      raise HTTPException(
          status_code=404,
          detail="Record not found"
      )
    
    forcasts = db.query(
        ForecastRecord
    ).filter(
        ForecastRecord.weather_record_id==id
    ).all()

    return {
        "id": records.id,
        "location": records.location,

        "temperature": records.temperature,
        "humidity": records.humidity,

        "weather_condition": records.weather_condition,

        "latitude": records.latitude,
        "longitude": records.longitude,

        "start_date": records.start_date,
        "end_date": records.end_date,

        "forecast": forcasts
    }



@router.put("/{id}")
def update_weather(
    id:int,
    request:WeatherCreate,
    db:Session = Depends(get_db)
):
    
    record = db.query(
        WeatherRecord
    ).filter(
        WeatherRecord.id == id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )
    
    validate_date_range(
        request.start_date,
        request.end_date
    )

    coordinates = get_coordinates(
        request.location
    )
    if coordinates is None:
      raise HTTPException(
          status_code=400,
          detail="Location not found"
      )

    weather = get_weather(
        coordinates["latitude"],
        coordinates["longitude"]
    )

    forecast = get_forecast(
        coordinates["latitude"],
        coordinates["longitude"],
        request.start_date,
        request.end_date
    )  

    record.location = request.location

    record.latitude = coordinates["latitude"]
    record.longitude = coordinates["longitude"]

    record.start_date = request.start_date
    record.end_date = request.end_date

    record.temperature = weather["temperature"]
    record.humidity = weather["humidity"]

    record.weather_condition = (
        forecast[0]["condition"]
        if forecast
        else "Unknown"
    )


    db.query(
        ForecastRecord
    ).filter(
        ForecastRecord.weather_record_id == id
    ).delete()
   

    for day in forecast:

      forecast_record = ForecastRecord(
          weather_record_id=id,

          forecast_date=datetime.strptime(
              day["date"],
              "%Y-%m-%d"
          ).date(),

          max_temp=day["max_temp"],
          min_temp=day["min_temp"],
          condition=day["condition"]
      )

      db.add(forecast_record)


    db.commit()
    db.refresh(record)

    return {
        "id": record.id,
        "location": record.location,
        "current_weather": {
            "temperature": record.temperature,
            "humidity": record.humidity
        },
        "forecast": forecast,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "map_url": record.map_url
    }




@router.delete("/{id}")
def delete_weather(
   id:int,
   db:Session = Depends(get_db)
):
   
  record = db.query(
    WeatherRecord
  ).filter(
    WeatherRecord.id == id
  ).first()

  if not record:
    raise HTTPException(
        status_code=404,
        detail="Record not found"
    )
   

  db.query(
    ForecastRecord
  ).filter(
        ForecastRecord.weather_record_id == id
  ).delete()

  db.delete(record)

  db.commit()
  return {
      "message": "Record deleted successfully"
  }


@router.get("/export/json")
def export_json(
    db: Session = Depends(get_db)
):
   
    records = db.query(
        WeatherRecord
    ).all()




    result = []

    for record in records:
       
        forecasts = db.query(
            ForecastRecord
        ).filter(
            ForecastRecord.weather_record_id == record.id
        ).all()
       
        result.append({
            "id": record.id,
            "location": record.location,

            "temperature": record.temperature,
            "humidity": record.humidity,

            "weather_condition": record.weather_condition,

            "start_date": record.start_date,
            "end_date": record.end_date,

            "forecast": [
                {
                    "date": forecast.forecast_date,
                    "max_temp": forecast.max_temp,
                    "min_temp": forecast.min_temp,
                    "condition": forecast.condition
                }
                for forecast in forecasts
            ]
        })

    with open(
        "weather_export.json",
        "w",
        encoding="utf-8"
    ) as file:
           
        json.dump(
            result,
            file,
            indent=4,
            default=str
        )

    return FileResponse(
        "weather_export.json",
        media_type="application/json",
        filename="weather_export.json"
    )


  
@router.get("/export/csv")
def export_csv(
   db:Session = Depends(get_db)
):
   
  records = db.query(
        WeatherRecord
    ).all()     
  
  with open(
      "weather_export.csv",
      "w",
      newline="",
      encoding="utf-8"
  ) as file:
     
    writer = csv.writer(file)

    writer.writerow([
       "Weather ID",
        "Location",
        "Temperature",
        "Humidity",
        "Condition",
        "Forecast Date",
        "Max Temp",
        "Min Temp",
        "Forecast Condition"
    ])

    for record in records:
      forecasts = db.query(
        ForecastRecord
      ).filter(
        ForecastRecord.weather_record_id == record.id
      ).all()

      for forecast in forecasts:

            writer.writerow([
                record.id,
                record.location,
                record.temperature,
                record.humidity,
                record.weather_condition,

                forecast.forecast_date,
                forecast.max_temp,
                forecast.min_temp,
                forecast.condition
            ])


  return FileResponse(
     "weather_export.csv",
     media_type="text/csv",
     filename="weather_export.csv"
  )




   

   






    