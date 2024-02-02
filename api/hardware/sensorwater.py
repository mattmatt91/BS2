# pip install adafruit-circuitpython-ads1x15
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_onewire.bus import OneWireBus
import adafruit_ads1x15.ads1115 as ADS

# from adafruit_ds18x20 import DS18X20
from hardware.oled import OledDisplay
from datetime import datetime


class SensorWater:
    def __init__(self, sensor_config: dict) -> None:
        self.oled = OledDisplay()
        # ad stuff for ec and ph
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.chan_pH = AnalogIn(ads, ADS.P2)
        self.chan_ec = AnalogIn(ads, ADS.P0)

        # onewire stuff for watertemperature
        # pin = getattr(board, sensor_config["watertemperature"])
        # ow_bus = OneWireBus(pin)  #  ad to config
        # self.ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

    async def measure_data(self):
        self.oled.draw_number(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # temp_water = self.ds18.temperature
        temp_water = 19
        pH = self.calc_pH(self.chan_pH.voltage)
        ec = self.calc_ec(self.chan_ec.voltage, temp_water)
        return {"pH": pH, "ec": ec, "temp_water": temp_water}

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


if __name__ == "__main__":
    sensor_config = {}
    sensor_config["watertemperature"] = 4
    sw = SensorWater(sensor_config)
    for i in range(10):
        data = sw.measure_data()
        print(data)
