from fastapi import FastAPI, Depends, HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse

from converter_functions import ConverterFuncitons
from models import ParameterModel, ParameterUpdateModel
from tasks import Tasks
from timelapse import Timelapse
from hardware import config
import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentification import Auhtentification, UserInDB
import os
import io

# Configuration
param_config = config["param_config"]
os.makedirs("data/", exist_ok=True)


# Load login credentials
with open("credentials.json", "r") as file:
    fake_users_db = json.load(file)

app = FastAPI()
tasks = Tasks()


# Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/startup")
@app.on_event("startup")
async def start_tasks():
    for param_name, param_values in param_config.items():
        await tasks.set_parameter(ParameterModel(**param_values), init=True)

    await tasks.add_warning({"message": "API restarted", "type": "system"})
    await tasks.start_scheduler()


# User Registration
@app.post("/register/")
async def register_user(username: str, password: str):
    if username in Auhtentification.fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = Auhtentification.hash_password(password)
    Auhtentification.fake_users_db[username] = {
        "username": username,
        "hashed_password": hashed_password,
    }
    return {"message": "User created successfully"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for user: {form_data.username}")  # Debugging
    user = Auhtentification.fake_users_db.get(form_data.username)
    if not user:
        print("User not found.")  # Debugging
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not Auhtentification.verify_password(
        form_data.password, user["hashed_password"]
    ):
        print("Password verification failed.")  # Debugging
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = Auhtentification.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/test")
async def get_image(
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    return {"api": "test"}


@app.get("/video")
async def get_image(
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    return await tasks.stream_image()


@app.post("/set_parameter")
async def api_set_parameter(
    param: ParameterUpdateModel,
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    new_parameter = await tasks.get_parameter()
    if param.parameter in new_parameter:
        data = new_parameter[param.parameter]
        data["value"] = param.value
        await tasks.set_parameter(ParameterModel(**data))
        await tasks.add_warning(
            {
                "message": f"{param.parameter} set to {str(param.value)}",
                "type": "system",
            }
        )


@app.get("/parameter")
async def get_parameter(
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    parameter = await tasks.get_parameter()
    return [parameter[param] for param in parameter]


@app.get("/sensor-data")
async def api_sensor_data(
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    return await tasks.sensor_data()


@app.get("/data")
async def get_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    measuring_data = await tasks.get_data()
    measuring_data = measuring_data.json()
    return ConverterFuncitons.transform_data(measuring_data)


@app.get("/data_download")
async def get_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    data = await tasks.get_data()
    data = data.json()
    await tasks.add_warning({"message": f"Data downladed", "type": "system"})
    return StreamingResponse(
        ConverterFuncitons.generate_csv(data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment;filename=data.csv"},
    )


@app.get("/video_download")
async def download_video(
    current_user: UserInDB = Depends(Auhtentification.get_current_user),
):
    video_path = "timelapse_video.mp4"  # Specify the video file path
    video_file_path = Timelapse.download_video(video_path)
    await tasks.add_warning({"message": f"Viedeo downloaded", "type": "system"})
    return FileResponse(video_file_path, media_type="video/mp4", filename=video_path)


@app.get("/warnings")
async def get_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    warning_list = await tasks.get_warnings()
    warning_list = warning_list.json()
    return warning_list


@app.delete("/delete_warning/{warning_id}")
async def delete_warning(warning_id: int):
    await tasks.delete_warning(warning_id)
    return {"message": "Warning deleted successfully"}
