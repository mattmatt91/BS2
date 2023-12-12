

class ConverterFuncitons:
    def convert_to_sensor_data(data_list):
        sensor_data = {}
        for item in data_list:
            key = item['sensor']
            value = item['Value']
            if key in ['humidity', 'temperature']:
                sensor_data[key] = float(value)
            elif key in ['lamp_bloom', 'lamp_grow', 'fan']:
                sensor_data[key] = value == 'True'
            else:
                sensor_data[key] = value
        return sensor_data

    def transform_data(data):
        return [{"sensor": k, "Value": v} for item in data for k, v in item.items() if k != 'id']