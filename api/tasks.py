

import requests
from models import ParameterModel, ParameterUpdateModel
from hardware import Sensor, Relais, Cam, config
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from converter_functions import ConverterFuncitons
from datetime import datetime

DATABASE_URL = config["URLS"]["DATABASE_URL"]
schedule_intervals = config["schedule_intervals"]
pin_assignment_relais = config["pin_assignment_relais"]
pin_assignment_sensors = config["pin_assignment_sensors"]




class Tasks:
    def __init__(self) -> None:
        print("init task instance")
        self.scheduler = AsyncIOScheduler()
        self.sensor = Sensor(pin=pin_assignment_sensors["DHT"])
        self.relais = Relais(pin_assignment_relais)
        self.cam = Cam()
    

    async def start_scheduler(self):
        await self.init_lamp()
        self.scheduler.add_job(
            self.measure_data,
            trigger=IntervalTrigger(minutes=schedule_intervals["measure_data"])
        )
        self.scheduler.add_job(
            self.store_image,
            trigger=IntervalTrigger(minutes=schedule_intervals["capture_img"])
        )
        parameter = await self.get_parameter()
        bloom_hour = 12 if parameter["Light"]["value"] == "bloom" else 18
        self.scheduler.add_job(
            self.toggle_lamp_on,
            trigger=CronTrigger(hour=0, minute=0, second=0),
            id="lamp_on"
        )
        self.scheduler.add_job(
            self.toggle_lamp_off,
            trigger=CronTrigger(hour=0, minute=0, second=bloom_hour),
            id="lamp_off"
        )
        self.scheduler.start()
        print("scheduler started")




    async def init_lamp(self):
        parameter = await self.get_parameter()
        time_off = 12 if parameter["Light"]["value"] == "bloom" else 18
        time_now = datetime.now().hour
        
        if time_off > time_now:
            await self.toggle_lamp_on()
        elif time_off <= time_now:
            await self.toggle_lamp_off()

    async def sensor_data(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = self.sensor.fetch_data()
        sensor_data = [{"sensor": "timestamp", "Value": current_time}]
        sensor_data += [{"sensor": k, "Value": v} for k, v in data.items()]
        relais_states = self.relais.get_states()
        sensor_data += [{"sensor": k, "Value": v}
                        for k, v in relais_states.items()]
        return sensor_data

    async def set_parameter(self, param: ParameterModel, init=False):
        print(f"setting parameter {param}")
        if init:
            requests.post(f"{DATABASE_URL}/init_parameter", json=param.dict())
        else:
            requests.post(f"{DATABASE_URL}/store_parameter", json=param.dict())

            # Special tasks for changes
        if param.parameter == "Light":
            await self.update_light(param.value)

    async def update_light(self, lamp):
        if lamp == "bloom":
            hour_off = 12
        else:
            hour_off = 18
        print(f"from update light: seconds{hour_off}, lamp = {lamp}")
        job = self.scheduler.get_job("lamp_off")
        if job:
            job.reschedule(trigger=CronTrigger(
                hour=0, minute=0, second=hour_off))

    async def measure_data(self):
        data = await self.sensor_data()
        print("measure data")
        sensor_data = ConverterFuncitons.convert_to_sensor_data(data)
        requests.post(f"{DATABASE_URL}/add_sensor_data", json=sensor_data)

    async def toggle_lamp_on(self):
        param = await self.get_parameter()
        print(param["Light"]["value"]) #  == "bloom" else "lamp_grow"
        lamp = "lamp_bloom" 
        print(f"toggling lamp on= {lamp}")
        self.relais.operate_relais({lamp: True})

    async def toggle_lamp_off(self):
        print("toggling light off")
        await self.relais.operate_relais({"lamp_bloom": False, "lamp_grow": False})

    async def get_data(self):
        return requests.get(f"{DATABASE_URL}/get_measuring_data")

    async def get_parameter(self):
        data = requests.get(f"{DATABASE_URL}/get_parameter").json()
        data = {p["parameter"]: p for p in data}
        return data

    async def store_image(self):
        img = self.cam.capture()
        self.cam.save_image(img)

    async def stream_image(self):
        img = self.cam.capture()
        return self.cam.format_for_serving(img)

