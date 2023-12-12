import random

class MockSensor:
    def __init__(self, sensor_type="DHT", pin=2):
        self.sensor = sensor_type
        self.pin = pin

    def __del__(self):
        pass

    def fetch_data(self):
        # Generate random humidity and temperature values
        humidity = round(random.uniform(20, 100),3)  # Random humidity in percentage
        temperature = round(random.uniform(15, 30),3)  # Random temperature in degrees Celsius
        return {"humidity":humidity, "temperature":temperature}

# Example usage
# mock_sensor = MockDHTSensor(None, None)
# humidity, temperature = mock_sensor.fetch_data()
# print('Mock Humidity: {}, Mock Temperature: {}'.format(humidity, temperature))
