import os

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
       

create_path_if_not_exists("app/data")


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
