from fastapi import FastAPI
from database import Base
from database import engine
from routes.weather import router as weather_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(weather_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def serve_frontend():
  return FileResponse("static/index.html")




