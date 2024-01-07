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
            GPIO.output(pin, GPIO.HIGH)

    def operate_relais(self, relais_operations):
        for operation in relais_operations:
                state = relais_operations[operation]
                if operation in self.relaiss:
                    self.relais_states[operation] = state
                    GPIO.output(self.relaiss[operation], GPIO.LOW if state else GPIO.HIGH)
                else:
                    print(f"relais '{operation}' not found.")


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
