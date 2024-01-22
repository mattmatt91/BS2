class WarningManager:
    def __init__(self) -> None:
        self.id = 4
        self.warnings = {
            1: {
                "id": 1,
                "message": "Warning: System Overheating",
                "type": "hardware",
                "isRead": False,
                "timestamp": "2024-01-22T10:00:00Z",
            },
            2: {
                "id": 2,
                "message": "Alert: Low Battery Level",
                "type": "hardware",
                "isRead": False,
                "timestamp": "2024-01-22T10:30:00Z",
            },
            3: {
                "id": 3,
                "message": "Notice: Scheduled Maintenance Due",
                "type": "system",
                "isRead": False,
                "timestamp": "2024-01-22T11:00:00Z",
            },
        }

    def add_warning(self, warning: str):
        self.warnings[self.id] = warning
        self.id += 1

    def delete_warning(self, id: int):
        self.warnings.pop(id)

    def get_warnings(self):
        return self.warnings
