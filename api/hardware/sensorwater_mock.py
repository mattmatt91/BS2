import random
import asyncio


class MockSensorWater:
    def __init__(self):
        pass

    async def measure_data(self):
        temp_water = round(random.uniform(18, 23), 2)
        pH = round(random.uniform(6, 8), 2)
        ec = round(random.uniform(500, 2000), 2)
        waterlevel = await self.get_waterlevel()
        return {"pH": pH, "ec": ec, "temp_water": temp_water, "waterlevel": waterlevel}

    def calc_pH(self, voltage: float):
        return random.uniform(9, 80)

    def calc_ec(self, voltage: float, temp_water: float):
        return random.uniform(500, 2000)

    async def get_waterlevel(self):
        asyncio.sleep(0.01)
        return round(random.uniform(20, 25), 2)
