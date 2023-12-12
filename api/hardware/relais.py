import RPi.GPIO as GPIO

class Relais:
    def __init__(self, relais_config):
        # relais_config is a dict with relais names and corresponding GPIO pin numbers
        self.relaiss = relais_config
        self.relais_states = {relais: False for relais in self.relaiss}  # False indicates closed

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup all relaiss as output and initialize them to closed (False)
        for pin in self.relaiss.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def operate_vale(self, relais_operations):
        # relais_operations is a list of dicts, each dict contains relais name and a Boolean
        for operation in relais_operations:
            for relais, state in operation.items():
                if relais in self.relaiss:
                    GPIO.output(self.relaiss[relais], GPIO.HIGH if state else GPIO.LOW)
                    self.relais_states[relais] = state
                else:
                    print(f"relais '{relais}' not found.")

    def get_relais_states(self):
        return self.relais_states
if __name__ == "__main__":
    # Example usage
    relais_config = {"relais_1": 17, "relais_2": 27, "relais_3": 22}
    my_relaiss = Relais(relais_config)

    # Operate relaiss
    my_relaiss.operate_relais([{"relais_1": True}, {"relais_2": False}])

    # Get current states
    print(my_relaiss.get_relais_states())
