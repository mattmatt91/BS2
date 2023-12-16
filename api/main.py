
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from converter_functions import ConverterFuncitons
from models import ParameterModel, ParameterUpdateModel
from tasks import Tasks
from hardware import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Replace with your React app's origin
    allow_origins=["http://192.168.1.30:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
param_config = config["param_config"]


# FastAPI routes
@app.on_event("startup")
async def start_tasks():
    for param_name, param_values in param_config.items():
        Tasks.set_parameter(ParameterModel(**param_values), init=True)
    Tasks.init_tasks()


@app.get("/video")
def get_image():
    return Tasks.stream_image()


@app.post("/set_parameter")
async def api_set_parameter(param: ParameterUpdateModel):
    new_parameter = Tasks.get_parameter()
    if param.parameter in new_parameter:
        data = new_parameter[param.parameter]
        data["value"] = param.value
        Tasks.set_parameter(ParameterModel(**data))


@app.get("/parameter")
async def get_parameter():
    parameter = Tasks.get_parameter()
    print(parameter)
    return [parameter[param] for param in parameter]


@app.get("/sensor-data")
def api_sensor_data():
    return Tasks.sensor_data()


@app.get("/data")
def get_data():
    measuring_data = Tasks.get_data().json()
    return ConverterFuncitons.transform_data(measuring_data)


@app.get("/data_download")
def get_data():
    data = Tasks.get_data().json()
    return StreamingResponse(ConverterFuncitons.generate_csv(data), media_type="text/csv", headers={"Content-Disposition": "attachment;filename=data.csv"})
