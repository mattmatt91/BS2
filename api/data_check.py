class DataCheck:
    @classmethod
    def check_sensor_data(cls, sensor_data):
        sensor_data_warnings = []
        if sensor_data["pH"] >= 7:
            sensor_data_warnings.append("pH value to high")
        elif sensor_data["pH"] < 4:
            sensor_data_warnings.append("pH value to low")
        return sensor_data_warnings
