import random
import asyncio


class MockSensorWater:
    def __init__(self, sensor_config: dict):
        pass

    async def measure_data(self):
        temp_water = round(random.uniform(18, 23), 2)
        pH = round(random.uniform(6, 8), 2)
        ec = round(random.uniform(500, 2000), 2)

        return {"pH": pH, "ec": ec, "temp_water": temp_water}

    def calc_pH(self, voltage: float):
        return random.uniform(9, 80)

    def calc_ec(self, voltage: float, temp_water: float):
        return random.uniform(500, 2000)
