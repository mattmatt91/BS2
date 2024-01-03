from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import Database  # Import the Database class from database.py
from models import SensorData, ParameterData  # Import your models from models.py


app = FastAPI()

db = Database("/app/data/my_database.db")  # Initialize your database with the path to your db file

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
    print(sensor_data)
    try:
        db.add_data(sensor_data.dict())
        return {"message": "Sensor data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/store_parameter")
async def store_parameter(parameter_data: ParameterData):
    try:
        print(parameter_data)
        db.add_parameter(parameter_data, init=False)
        return {"message": "Parameter stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/init_parameter")
async def init_parameter(parameter_data: ParameterData):
    # print(parameter_data)
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

@app.on_event("shutdown")
def shutdown_event():
    db.close()
