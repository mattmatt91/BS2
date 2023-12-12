import os
import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return {}
    

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
       

create_path_if_not_exists("app/data")
config = read_json_file("config.json")



operating_mode = os.environ.get('operating_system', 'default')

if operating_mode == 'mock':
    # Import mock classes
    from .sensor_mock import MockSensor as Sensor
    from .relais_mock import MockRelais as Relais
    from .cam_mock import MockImageCapturer as Cam
else:
    # Import real sensor classes
    from .sensor import Sensor as Sensor
    from .relais import Relais as Relais
    from .cam import ImageCapturer as Cam
