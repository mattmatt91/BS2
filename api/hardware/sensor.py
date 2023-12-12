import Adafruit_DHT

class Sensor:
    def __init__(self, sensor_type="DHT", pin=2):
        self.sensor = sensor_type
        self.pin = pin

    def __del__(self):
        # Destructor doesn't need to do anything special in this case
        pass

    def fetch_data(self):
        # Fetch the humidity and temperature data
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return {"humidity":humidity, "temperature":temperature}


