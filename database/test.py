import requests

# Define the API URL
BASE_URL = "http://127.0.0.1:6000"

# Add sensor data
sensor_data = {
    "timestamp": "2023-12-09 02:21:46",
    "humidity": 30.631,
    "temperature": 22.248,
    "lamp_bloom": False,
    "lamp_grow": False,
    "fan": False
}
response = requests.post(f"{BASE_URL}/add_sensor_data", json=sensor_data)
# print("Add Sensor Data Response:", response.json())


# Get measuring data
response = requests.get(f"{BASE_URL}/get_measuring_data")
print("Measuring Data:", response.json())

# Store parameter
parameter_data = {
    "parameter_name": "Temperature",
    "parameter_type": "Float",
    "parameter_value": "18",
    "min_value": "15",
    "max_value": "30",
    "parameter_entries": []
}
response = requests.post(f"{BASE_URL}/store_parameter", json=parameter_data)
print("Store Parameter Response:", response.json())


# Get parameter by name
parameter_name = "Temperature"
response = requests.get(f"{BASE_URL}/get_parameter/")
print(response.json())

exit()