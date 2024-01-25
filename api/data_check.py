class DataCheck:
    @classmethod
    def check_sensor_data(cls, sensor_data, preferences: dict):
        sensor_data_warnings = []
        if sensor_data["pH"] >= float(preferences["pH"]["value"]["max"]):
            sensor_data_warnings.append("pH value to high")
        elif sensor_data["pH"] < float(preferences["pH"]["value"]["min"]):
            sensor_data_warnings.append("pH value to low")

        if sensor_data["temperature"] >= float(
            preferences["Temperature"]["value"]["max"]
        ):
            sensor_data_warnings.append("Temperature value to high")
        elif sensor_data["temperature"] < float(
            preferences["Temperature"]["value"]["min"]
        ):
            sensor_data_warnings.append("Temperature value to low")

        if sensor_data["ec"] >= float(preferences["ec"]["value"]["max"]):
            sensor_data_warnings.append("ec value to high")
        elif sensor_data["ec"] < float(preferences["ec"]["value"]["min"]):
            sensor_data_warnings.append("ec value to low")

        return sensor_data_warnings
