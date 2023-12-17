
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from converter_functions import ConverterFuncitons
from models import ParameterModel, ParameterUpdateModel
from tasks import Tasks
from hardware import config
import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from authentification import Auhtentification, UserInDB


# Configuration
param_config = config["param_config"]



# Load users database
with open("credentials.json", "r") as file:
    fake_users_db = json.load(file)

app = FastAPI()

# Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User Registration


@app.post("/register/")
async def register_user(username: str, password: str):
    if username in Auhtentification.fake_users_db:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = Auhtentification.hash_password(password)
    Auhtentification.fake_users_db[username] = {"username": username,
                               "hashed_password": hashed_password}
    return {"message": "User created successfully"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for user: {form_data.username}")  # Debugging
    user = Auhtentification.fake_users_db.get(form_data.username)
    if not user:
        print("User not found.")  # Debugging
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    if not Auhtentification.verify_password(form_data.password, user["hashed_password"]):
        print("Password verification failed.")  # Debugging
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    access_token = Auhtentification.create_access_token(
        data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event("startup")
async def start_tasks(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    for param_name, param_values in param_config.items():
        Tasks.set_parameter(ParameterModel(**param_values), init=True)
    Tasks.init_tasks()


@app.get("/test")
def get_image(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    return {"api": "test"}


@app.get("/video")
def get_image(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    return Tasks.stream_image()


@app.post("/set_parameter")
async def api_set_parameter(param: ParameterUpdateModel, current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    new_parameter = Tasks.get_parameter()
    if param.parameter in new_parameter:
        data = new_parameter[param.parameter]
        data["value"] = param.value
        Tasks.set_parameter(ParameterModel(**data))


@app.get("/parameter")
async def get_parameter(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    parameter = Tasks.get_parameter()
    return [parameter[param] for param in parameter]


@app.get("/sensor-data")
def api_sensor_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    return Tasks.sensor_data()


@app.get("/data")
def get_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    measuring_data = Tasks.get_data().json()
    return ConverterFuncitons.transform_data(measuring_data)


@app.get("/data_download")
def get_data(current_user: UserInDB = Depends(Auhtentification.get_current_user)):
    data = Tasks.get_data().json()
    return StreamingResponse(ConverterFuncitons.generate_csv(data), media_type="text/csv", headers={"Content-Disposition": "attachment;filename=data.csv"})
