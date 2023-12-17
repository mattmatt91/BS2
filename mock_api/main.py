from datetime import datetime, timedelta
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
import random
from fastapi.responses import FileResponse
from pathlib import Path
# main.py (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import Union




my_sensors = ["humidity", "temperature", "pressure"]


app = FastAPI()

# Configure CORS to allow requests from your React app's origin
app.add_middleware(
    CORSMiddleware,
    # Replace with your React app's origin
    allow_origins=["http://api:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParameterModel(BaseModel):
    parameter: str
    value: Union[bool, float, int, str]  # Accepts multiple types

    # Optional: Validator to check the type or format of the value
    @validator('value')
    def check_value(cls, v, values, **kwargs):
        # Add validation logic here, if needed
        return v

@app.get("/video")
def get_image():
    print("test img route")
    image_path = "test_img.png"
    return FileResponse(image_path)

@app.post("/set_parameter")
async def set_parameter(param: ParameterModel):
    # Logic to handle the parameter update
    # You might want to update a database, a file, or another data structure here
    print(f"Received: {param}")
    return {"message": "Parameter updated successfully"}

# Additional GET route to serve parameters (for testing)
@app.get("/parameter")
async def get_parameter():
    print("test get parameter")
    # Mock data
    return [
        {"parameter": "Temperature", "datatype": "Float", "value": 23.5, "min": 15, "max": 30},
        {"parameter": "Light", "datatype": "Bool", "value": True},
        {"parameter": "Mode", "datatype": "String", "value": "Auto", "entrys": ["Auto", "Manual", "Eco"]}
    ]


@app.get("/sensor-data")
def get_sensor_data():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensor_data = [{
                "sensor": "timestamp",
                "Legal": "Legal_timestamp",
                "Value": current_time
                    }]
    for sensor in my_sensors:
        sensor_data.append({
                "sensor": sensor,
                "Legal": f"Legal_{sensor}",
                "Value": round(random.uniform(40, 70), 2)
                    })
    
    return sensor_data


@app.get("/data")
def get_sensor_data():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sensor_data = [{
        "sensor": "timestamp",
        "Legal": "Legal_timestamp",
        "Value": current_time
    }]
    
    my_sensors = ["humidity", "temperature", "pressure"]

    for i in range(100):
        timestamp = (datetime.now() + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
        sensor_data.append({
            "sensor": "timestamp",
            "Value": timestamp
        })
        for sensor in my_sensors:
            sensor_data.append({
                "sensor": sensor,
                "Value": round(random.uniform(40, 70), 2)
            })
    print(sensor_data)
    return sensor_data