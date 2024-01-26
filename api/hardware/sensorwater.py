# pip install adafruit-circuitpython-ads1x15
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from WaterLevelSensor import WaterLevelSensor


class SensorWater:
    def __init__(self, sensor_config: {"GPIO_TRIGGER": 15, "GPIO": 16}) -> None:
        # ad stuff for ec and ph
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        self.chan_pH = AnalogIn(ads, ADS.P0)
        self.chan_ec = AnalogIn(ads, ADS.P1)

        # onewire stuff for watertemperature
        ow_bus = OneWireBus(board.D5)
        self.ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

        # init waterlevelsensor
        self.waterlevelsensor = WaterLevelSensor(
            GPIO_ECHO=sensor_config["GPIO_ECHO"],
            GPIO_TRIGGER=sensor_config["GPIO_TRIGGER"],
        )

    async def measure_data(self):
        temp_water = self.ds18.temperature
        pH = self.calc_pH(self.chan_pH.voltage)
        ec = self.calc_ec(self.chan_ec.voltage, temp_water)
        waterlevel = await self.waterlevelsensor.get_distance()
        return {"pH": pH, "ec": ec, "temp_water": temp_water, "waterlevel": waterlevel}

    def calc_pH(self, voltage: float):
        # compute pH ..
        pH = voltage * 2
        return pH

    def calc_ec(self, voltage: float, temp_water: float):
        # compute ec ..
        ec_measured = voltage * 2
        TCF = 0.02  # constant
        ec = ec_measured * (1 + TCF * (temp_water - 25))
        return ec
