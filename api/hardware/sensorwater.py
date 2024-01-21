# pip install adafruit-circuitpython-ads1x15
import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20


class SensorWater:
    def __init__(self) -> None:
        # ad stuff for ec and ph
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1015(i2c)
        self.chan_pH = AnalogIn(ads, ADS.P0)
        self.chan_ec = AnalogIn(ads, ADS.P1)

        # onewire stuff for watertemperature
        ow_bus = OneWireBus(board.D5)
        self.ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

    def measure_data(self):
        temp_water = self.ds18.temperature
        pH = self.calc_pH(self.chan_pH.voltage)
        ec = self.calc_ec(self.chan_ec.voltage, temp_water)
        return {"pH": pH, "ec": ec, "temp_water": temp_water}

    def calc_pH(self, voltage: float):
        # compute pH ..
        pH = voltage * 2
        return pH

    def calc_ec(self, voltage: float, temp_water: float):
        # compute ec ..
        ec = voltage * 2
        return ec
