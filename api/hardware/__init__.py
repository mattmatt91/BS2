import os
import json


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}


config = read_json_file("config.json")


operating_mode = os.environ.get("operating_system", "default")
print(operating_mode)
if operating_mode == "mock":
    # Import mock classes
    from .sensor_mock import MockSensor as Sensor
    from .relais_mock import MockRelais as Relais
    from .cam_mock import MockImageCapturer as Cam
    from .sensorwater_mock import MockSensorWater as SensorWater
    from .waterrelais_mock import WaterRelaisMock as WaterRelais
elif operating_mode == "raspi":
    from .sensor import Sensor as Sensor
    from .relais import Relais as Relais
    from .cam import ImageCapturer as Cam
    from .sensorwater import SensorWater as SensorWater
    from .waterrelais_mock import WaterRelaisMock as WaterRelais
else:
    raise Exception("operating system must be mock or raspi")
