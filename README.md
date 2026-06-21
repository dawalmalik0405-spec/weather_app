# Weather Dashboard

A small full-stack weather application built with FastAPI, SQLite, and vanilla JavaScript. It resolves place names through Open-Meteo's geocoding API, retrieves current weather and a seven-day forecast, stores searches locally, and provides a browser dashboard for managing and exporting saved records.

## Features

- Location autocomplete powered by Open-Meteo geocoding
- Current temperature and relative humidity
- Forecast filtering for a user-selected date range
- Interactive Leaflet/OpenStreetMap location map
- Persistent weather searches in a local SQLite database
- View, update, and delete saved records
- JSON and CSV exports
- Interactive FastAPI API documentation
- No API key required

## Technology stack

| Layer | Technology |
| --- | --- |
| API | Python, FastAPI |
| Data access | SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, CSS, vanilla JavaScript |
| Map | Leaflet with OpenStreetMap tiles |
| Weather and geocoding | Open-Meteo APIs |
| Server | Uvicorn |

## Project structure

```text
hackathon/
|-- backend/
|   |-- main.py                       # FastAPI setup and static UI hosting
|   |-- database.py                   # SQLite engine and DB sessions
|   |-- models.py                     # Weather and forecast tables
|   |-- routes/
|   |   |-- weather.py                # CRUD, search, and export endpoints
|   |   |-- weater.py                 # WeatherCreate request schema
|   |   `-- export.py                 # Currently unused placeholder
|   |-- services/
|   |   |-- geocoding_service.py      # Place lookup and suggestions
|   |   |-- weather_service.py        # Current weather and forecast lookup
|   |   `-- validation_service.py     # Date-range validation
|   `-- static/
|       |-- index.html                # Dashboard markup
|       |-- app.js                    # UI behavior and API calls
|       `-- style.css                 # Dashboard styling
|-- LICENSE
|-- requirements.txt                  # Pinned Python dependencies
`-- README.md
```

## How it works

1. The browser sends a location and date range to the FastAPI API.
2. The geocoding service converts the location into latitude and longitude. If multiple results exist, the service prefers a result in India and otherwise uses the first match.
3. The weather service requests current conditions and a seven-day daily forecast from Open-Meteo.
4. Forecast days within the requested range are stored with the current conditions in SQLite.
5. The API returns the saved data to the dashboard, which renders the conditions, forecast, and map.

## Prerequisites

- Python 3.10 or newer
- Git (when installing by cloning the repository)
- Internet access at runtime for Open-Meteo, Leaflet, and OpenStreetMap

Python runtime dependencies are pinned in `requirements.txt` for reproducible installation.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/dawalmalik0405-spec/weather_app.git
cd weather_app
```

If the project is already downloaded, open PowerShell in the project root—the directory containing `README.md`, `requirements.txt`, and `backend`.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, allow local scripts for your user and then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the application

The server must be started from the `backend` directory because the application currently uses relative import, static-file, database, and export paths.

```powershell
cd backend
python -m uvicorn main:app --reload
```

After Uvicorn reports that the application has started, open the dashboard at:

<http://localhost:8000>

The same server hosts both the browser frontend and the API; no separate frontend command is required.

### Available URLs

| Page | URL |
| --- | --- |
| Weather dashboard | <http://localhost:8000> |
| Swagger API documentation | <http://localhost:8000/docs> |
| ReDoc API documentation | <http://localhost:8000/redoc> |

### Stop or restart the server

- Press `Ctrl+C` in the server terminal to stop it.
- Run `python -m uvicorn main:app --reload` again to restart it.
- Run `deactivate` when you are finished with the virtual environment.

### Run the project again later

For subsequent runs, dependencies do not need to be reinstalled. From the project root, run:

```powershell
.\.venv\Scripts\Activate.ps1
cd backend
python -m uvicorn main:app --reload
```

### Linux or macOS

The equivalent environment activation and startup commands are:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd backend
python -m uvicorn main:app --reload
```

### Verify the installation

With the server running, this PowerShell command should return saved records as JSON (an empty list on a new installation):

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/weather/"
```

If the app does not start, confirm that:

- The virtual environment is active.
- Dependencies were installed from the root `requirements.txt`.
- The Uvicorn command is being run inside `backend`.
- Port `8000` is not already being used by another process.
- Internet access is available for live weather, location search, and map resources.

## Configuration and generated files

The application does not currently use environment variables and does not require an API key.

When started from `backend`, it creates these ignored runtime files there:

- `weather.db` — SQLite application database
- `weather_export.json` — generated by the JSON export endpoint
- `weather_export.csv` — generated by the CSV export endpoint

Deleting `weather.db` resets all saved records. Stop the server before deleting it.

## API reference

All application endpoints use the `/weather` prefix.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/weather/` | Look up weather and save a record |
| `GET` | `/weather/` | List all saved weather records |
| `GET` | `/weather/search?query={text}` | Return location suggestions |
| `GET` | `/weather/{id}` | Return one record with its forecasts |
| `PUT` | `/weather/{id}` | Refresh and replace a saved record |
| `DELETE` | `/weather/{id}` | Delete a record and its forecasts |
| `GET` | `/weather/export/json` | Download all records as JSON |
| `GET` | `/weather/export/csv` | Download forecast rows as CSV |

### Create a weather record

```powershell
$body = @{
    location   = "New Delhi"
    start_date = "2026-06-21"
    end_date   = "2026-06-27"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/weather/" `
    -ContentType "application/json" `
    -Body $body
```

Request body:

```json
{
  "location": "New Delhi",
  "start_date": "2026-06-21",
  "end_date": "2026-06-27"
}
```

Example response shape:

```json
{
  "id": 1,
  "location": "New Delhi",
  "current_weather": {
    "temperature": 32.1,
    "humidity": 52
  },
  "forecast": [
    {
      "date": "2026-06-21",
      "max_temp": 36.2,
      "min_temp": 28.4,
      "condition": "Partly Cloudy"
    }
  ],
  "latitude": 28.63576,
  "longitude": 77.22445,
  "matched_location": "New Delhi",
  "country": "India",
  "map_url": "https://maps.google.com/?q=28.63576,77.22445"
}
```

### Update a record

`PUT /weather/{id}` accepts the same body as the create endpoint. It refreshes the current weather, deletes the record's old forecast rows, and stores a new filtered forecast.

### Error responses

Common responses include:

| Status | Cause |
| --- | --- |
| `400` | End date is earlier than start date |
| `400` | The supplied location cannot be resolved |
| `404` | The requested saved record does not exist |
| `422` | Missing fields, malformed JSON, or invalid ISO date values |

Upstream network and API failures are not currently converted into custom application errors and may result in a `500` response.

## Data model

### `weather_records`

Stores the searched location, coordinates, requested date range, current temperature and humidity, a representative weather condition, Google Maps URL, and creation timestamp.

### `forecast_records`

Stores forecast date, maximum temperature, minimum temperature, and condition. Each row belongs to a `weather_records` row through `weather_record_id`.

## External services

- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) resolves names and supplies autocomplete results.
- [Open-Meteo Weather Forecast API](https://open-meteo.com/en/docs) supplies current conditions and daily forecasts.
- [Leaflet](https://leafletjs.com/) renders the browser map.
- [OpenStreetMap](https://www.openstreetmap.org/) supplies map tiles.

## Current limitations

- Open-Meteo is requested with `forecast_days=7`; dates outside the returned seven-day window produce no forecast rows.
- Date validation only checks that the start date is not later than the end date.
- Requests to external services do not set timeouts, retry failures, or explicitly check HTTP status codes.
- SQLite schema creation uses `create_all`; there is no migration system.
- CORS currently permits every origin, which is convenient for development but should be restricted before deployment.
- Export files use fixed names, so concurrent export requests can overwrite each other.
- The frontend loads Leaflet assets from a CDN and therefore does not work fully offline.
- There is currently no automated test suite, authentication, or production deployment configuration.

## Development notes

- FastAPI creates the SQLite tables during application startup.
- The frontend uses same-origin relative URLs, so it is served by the same FastAPI process as the API.
- API behavior can be explored without the dashboard through Swagger UI at `/docs`.
- If the database schema changes during development, introduce migrations (for example, Alembic) rather than relying on `create_all` for existing databases.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
