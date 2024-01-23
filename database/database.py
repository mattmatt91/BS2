import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS measuring_data
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TIMESTAMP,
                            humidity REAL,
                            temperature REAL,
                            pressure REAL,
                            pH REAL,
                            ec REAL,
                            temp_water REAL,
                            lamp_bloom BOOLEAN,
                            lamp_grow BOOLEAN,
                            fan BOOLEAN)
                            """
        )
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS parameters
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              parameter TEXT,
                              datatype TEXT,
                              value TEXT,
                              min_value TEXT,
                              max_value TEXT,
                              entrys TEXT)"""
        )
        self.conn.commit()
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS warnings
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                type TEXT,
                isRead BOOLEAN,
                timestamp TIMESTAMP)
            """
        )
        self.conn.commit()

    # sensordata stuff
    def add_data(self, sensor_data):
        self.conn.execute(
            "INSERT INTO measuring_data (timestamp, humidity, temperature, pressure, lamp_bloom, lamp_grow, fan, pH, ec, temp_water) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                sensor_data["timestamp"],
                sensor_data["humidity"],
                sensor_data["temperature"],
                sensor_data["pressure"],
                sensor_data["lamp_bloom"],
                sensor_data["lamp_grow"],
                sensor_data["fan"],
                sensor_data["pH"],
                sensor_data["ec"],
                sensor_data["temp_water"],
            ),
        )
        self.conn.commit()

    def get_measuring_data(self):
        cursor = self.conn.execute("SELECT * FROM measuring_data")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    # parameter stuff
    def add_parameter(self, parameter_data, init=False):
        parameter_name = parameter_data.parameter
        cursor = self.conn.execute(
            "SELECT id FROM parameters WHERE parameter=?", (parameter_name,)
        )
        existing_param = cursor.fetchone()

        entries_str = ",".join(parameter_data.entrys) if parameter_data.entrys else ""
        if existing_param:
            if not init:
                # Update existing parameter only if init is False
                self.conn.execute(
                    "UPDATE parameters SET datatype=?, value=?, min_value=?, max_value=?, entrys=? WHERE parameter=?",
                    (
                        parameter_data.datatype,
                        parameter_data.value,
                        parameter_data.min_value,
                        parameter_data.max_value,
                        entries_str,
                        parameter_name,
                    ),
                )
        else:
            if init:
                # Insert new parameter only if init is True and the parameter does not exist
                self.conn.execute(
                    "INSERT INTO parameters (parameter, datatype, value, min_value, max_value, entrys) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        parameter_name,
                        parameter_data.datatype,
                        parameter_data.value,
                        parameter_data.min_value,
                        parameter_data.max_value,
                        entries_str,
                    ),
                )

        self.conn.commit()

    def get_parameter(self):
        cursor = self.conn.execute("SELECT * FROM parameters")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        parameters = []
        for row in rows:
            param_dict = dict(zip(columns, row))
            entrys_str = param_dict.get("entrys", "")
            param_dict["entrys"] = entrys_str.split(",") if entrys_str else []
            parameters.append(param_dict)
        return parameters

    # warning stuff
    def warning_exists(self, warning_type: str, warning_message: str) -> bool:
        cursor = self.conn.execute(
            "SELECT COUNT(*) FROM warnings WHERE type = sensordata AND message = ?",
            (
                warning_type,
                warning_message,
            ),
        )
        count = cursor.fetchone()[0]
        return count > 0

    def add_warning(self, warning: dict):
        # Check if a warning with the same type and message already exists
        if self.warning_exists(warning["type"], warning["message"]):
            # Skip adding or update the existing warning
            return

        # Add new warning
        warning["timestamp"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        warning["isRead"] = False
        self.conn.execute(
            "INSERT INTO warnings (message, type, isRead, timestamp) VALUES (?, ?, ?, ?)",
            (
                warning["message"],
                warning["type"],
                warning["isRead"],
                warning["timestamp"],
            ),
        )
        self.conn.commit()

    def delete_warning(self, warning_id):
        self.conn.execute("DELETE FROM warnings WHERE id = ?", (warning_id,))
        self.conn.commit()

    def get_warnings(self):
        cursor = self.conn.execute("SELECT * FROM warnings")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def close(self):
        self.conn.close()
