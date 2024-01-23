from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import Database  # Import the Database class from database.py
from models import (
    SensorData,
    ParameterData,
    WarningDatabase,
)  # Import your models from models.py
import os

app = FastAPI()
os.makedirs("data/", exist_ok=True)
db = Database(
    "data/my_database.db"
)  # Initialize your database with the path to your db file
app.add_middleware(
    CORSMiddleware,
    # Replace with your React app's origin
    allow_origins=["http://api"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add_sensor_data")
async def add_sensor_data(sensor_data: SensorData):
    try:
        db.add_data(sensor_data.dict())
        return {"message": "Sensor data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/store_parameter")
async def store_parameter(parameter_data: ParameterData):
    try:
        db.add_parameter(parameter_data, init=False)
        return {"message": "Parameter stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/init_parameter")
async def init_parameter(parameter_data: ParameterData):
    try:
        db.add_parameter(parameter_data, init=True)
        return {"message": "Parameter initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_measuring_data")
async def get_measuring_data():
    try:
        data = db.get_measuring_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_parameter")
async def get_parameter():
    try:
        data = db.get_parameter()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_warnings")
async def get_warnings():
    try:
        warnings = db.get_warnings()
        return warnings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_warning")
async def add_warning(warning: WarningDatabase):
    try:
        db.add_warning(warning.dict())
        return {"message": "Warning added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete_warning/{warning_id}")
async def delete_warning(warning_id: int):
    try:
        db.delete_warning(warning_id)
        return {"message": "Warning deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown_event():
    db.close()
