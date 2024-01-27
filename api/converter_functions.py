import csv
import io


class ConverterFuncitons:
    def convert_to_sensor_data(data_list):
        sensor_data = {}
        for item in data_list:
            key = item["sensor"]
            value = item["Value"]

            if type(value) == int and value >= 0 and value <= 1:
                sensor_data[key] = "True" if value == 1 else False
            elif type(value) == float:
                sensor_data[key] = float(value)
            else:
                sensor_data[key] = value
        print(sensor_data)
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
