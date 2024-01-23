import random


class MockSensorWater:
    def __init__(self):
        pass

    def measure_data(self):
        temp_water = round(
            random.uniform(18, 23), 2
        )  # Random temperature between 18 and 23
        pH = round(random.uniform(6, 8), 2)  # Random pH value between 4 and 8
        ec = round(random.uniform(500, 2000), 2)  # Random EC value between 500 and 2000
        return {"pH": pH, "ec": ec, "temp_water": temp_water}

    def calc_pH(self, voltage: float):
        # Mock calculation for pH
        return random.uniform(9, 80)

    def calc_ec(self, voltage: float, temp_water: float):
        # Mock calculation for EC
        return random.uniform(500, 2000)
