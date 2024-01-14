import csv
import io


class ConverterFuncitons:
    def convert_to_sensor_data(data_list):
        sensor_data = {}
        for item in data_list:
            key = item["sensor"]
            value = item["Value"]
            if key in ["humidity", "temperature", "pressure"]:
                sensor_data[key] = float(value)
            elif key in ["lamp_bloom", "lamp_grow", "fan"]:
                sensor_data[key] = "True" if value == 1 else False
            else:
                sensor_data[key] = value
        return sensor_data

    def transform_data(data):
        return [
            {"sensor": k, "Value": v}
            for item in data
            for k, v in item.items()
            if k != "id"
        ]

    def generate_csv(data: list):
        stream = io.StringIO()
        writer = csv.DictWriter(stream, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        stream.seek(0)  # Move this outside the loop
        return stream
