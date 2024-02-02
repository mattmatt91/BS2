import bme680

# from WaterLevelSensor import WaterLevelSensor
import random


class Sensor:
    def __init__(self, sensor_comfig: dict):
        try:
            self.sensor = bme680.BME680(0x77)
        except (RuntimeError, IOError):
            print("Failed to connect to BME680 sensor on address  0x77...")

        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)

        # self.waterlevelsensor = WaterLevelSensor(
        #     GPIO_ECHO=sensor_comfig["GPIO_ECHO"],
        #     GPIO_TRIGGER=sensor_comfig["GPIO_TRIGGER"],
        # )

    def __del__(self):
        # Destructor doesn't need to do anything special in this case
        pass

    def fetch_data(self):
        # Fetch the humidity and temperature data
        if self.sensor.get_sensor_data():
            temperature = self.sensor.data.temperature
            humidity = self.sensor.data.humidity
            pressure = self.sensor.data.pressure
            # waterlevel = self.waterlevelsensor.get_distance()
            waterlevel = round(random.uniform(20, 25), 2)
        return {
            "humidity": humidity,
            "temperature": temperature,
            "pressure": pressure,
            "waterlevel": waterlevel,
        }
