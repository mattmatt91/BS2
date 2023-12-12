
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from converter_functions import ConverterFuncitons
from models import ParameterModel, ParameterUpdateModel
from tasks import Tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Replace with your React app's origin
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
param_config = {
    "Temperature": {"parameter": "Temperature", "datatype": "Float", "value": 23.5, "min_value": 15, "max_value": 30},
    "Light": {"parameter": "Light", "datatype": "String", "value": "bloom", "entrys": ["bloom", "grow"]},
    "Mode": {"parameter": "Mode", "datatype": "String", "value": "Auto", "entrys": ["Auto", "Manual", "Eco"]},
    "StartRocket": {"parameter": "StartRocket", "datatype": "Bool", "value": True}
}


# FastAPI routes
@app.on_event("startup")
async def start_scheduler():
    Tasks.start_scheduler()
    for param_name, param_values in param_config.items():
        Tasks.set_parameter(ParameterModel(**param_values), init=True)


@app.get("/video")
def get_image():
    return Tasks.stream_image()


@app.post("/set_parameter")
async def api_set_parameter(param: ParameterUpdateModel):
    old_param = Tasks.get_parameter()
    new_param_set = {p["parameter"]: p for p in old_param}
    if param.parameter in new_param_set:
        data = new_param_set[param.parameter]
        data["value"] = param.value
        Tasks.set_parameter(ParameterModel(**data))


@app.get("/parameter")
async def get_parameter():
    return [param for param in Tasks.get_parameter()]


@app.get("/sensor-data")
def api_sensor_data():
    return Tasks.sensor_data()


@app.get("/data")
def get_data():
    measuring_data = Tasks.get_data()
    return ConverterFuncitons.transform_data(measuring_data.json())
