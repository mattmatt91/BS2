

import requests
from models import ParameterModel, ParameterUpdateModel
from hardware import Sensor, Relais, Cam
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from converter_functions import ConverterFuncitons

DATABASE_URL = "http://database:6000"


class Tasks:
    sensor = Sensor()
    relais = Relais({"lamp_bloom": 6, "lamp_grow": 7, "fan": 8})
    cam = Cam()
    scheduler = AsyncIOScheduler()
    @staticmethod
    def start_scheduler():

        Tasks.scheduler.add_job(
            Tasks.measure_data, trigger=IntervalTrigger(minutes=60))
        Tasks.scheduler.add_job(
            Tasks.store_image, trigger=IntervalTrigger(minutes=60))
        Tasks.scheduler.add_job(Tasks.toggle_lamp_on, trigger=CronTrigger(
            hour=0, minute=0), id="lamp_on")
        Tasks.scheduler.add_job(Tasks.toggle_lamp_off, trigger=CronTrigger(
            hour=18, minute=0), id="lamp_off")

        Tasks.scheduler.start()

    @staticmethod
    def sensor_data():
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = Tasks.sensor.fetch_data()
        sensor_data = [{"sensor": "timestamp", "Value": current_time}]
        sensor_data += [{"sensor": k, "Value": v} for k, v in data.items()]
        relais_states = Tasks.relais.get_states()
        sensor_data += [{"sensor": k, "Value": v}
                        for k, v in relais_states.items()]
        return sensor_data

    @staticmethod
    def set_parameter(param: ParameterModel, init=False):
        if init:
            requests.post(f"{DATABASE_URL}/init_parameter", json=param.dict())
        else:
            requests.post(f"{DATABASE_URL}/store_parameter", json=param.dict())

            # Special tasks for changes
        if param.parameter == "Light":
            Tasks.update_light(param.value)

    @staticmethod
    def update_light(lamp):
        # Logic to handle light update
        if lamp == "bloom":
            hour = 12
        else:
            hour = 18
        # Reschedule the task or perform other actions based on the new lamp value
        # Assuming you have a scheduler job to modify, e.g., "lamp_on" or "lamp_off"
        job = Tasks.scheduler.get_job("lamp_on")
        if job:
            job.reschedule(trigger=CronTrigger(hour=hour, minute=0))

    @staticmethod
    def measure_data():
        data = Tasks.sensor_data()
        sensor_data = ConverterFuncitons.convert_to_sensor_data(data)
        requests.post(f"{DATABASE_URL}/add_sensor_data", json=sensor_data)

    @staticmethod
    def toggle_lamp_on():
        lamp = "lamp_bloom" if Tasks.get_parameter()["Light"]["value"] == "bloom" else "lamp_grow"
        lamp = "lamp_bloom" if Tasks.get_parameter()["Light"]["value"] == "bloom" else "lamp_grow"
        Tasks.relais.operate_relais({lamp: True})

    @staticmethod
    def toggle_lamp_off():
        Tasks.relais.operate_relais({"lamp_bloom": False, "lamp_grow": False})

    @staticmethod
    def get_data():
        return requests.get(f"{DATABASE_URL}/get_measuring_data")

    @staticmethod
    def get_parameter():
        data =  requests.get(f"{DATABASE_URL}/get_parameter").json()
        return data

    @staticmethod
    def store_image():
        img = Tasks.cam.capture()
        Tasks.cam.save_image(img)
    
    @staticmethod
    def stream_image():
        img = Tasks.cam.capture()
        return Tasks.cam.format_for_serving(img)
