import RPi.GPIO as GPIO

class Relais:
    def __init__(self, relais_config):
        # relais_config is a dict with relais names and corresponding GPIO pin numbers
        self.relais = relais_config
        # self.relais_states = {relais: False for relais in self.relais}  # False indicates closed

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup all relais as output and initialize them to closed (False)
        for pin in self.relais:
            pin_i = int(self.relais[pin]["pin_i"])
            pin_o = int(self.relais[pin]["pin_o"])
           
            GPIO.setup(pin_o, GPIO.OUT)
            GPIO.output(pin_o, GPIO.HIGH)
            GPIO.setup(pin_i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def operate_relais(self, relais_operations):
        for operation in relais_operations:
                state = relais_operations[operation]
                if operation in self.relais:
                    print(self.relais[operation]["pin_o"])
                    GPIO.output(self.relais[operation]["pin_o"], GPIO.LOW if state else GPIO.HIGH)
                else:
                    print(f"relais '{operation}' not found.")

    def get_states(self):
        relais_states = {}
        for relais in self.relais:
            relais_states[relais] =   not GPIO.input(self.relais[relais]["pin_i"])
        return relais_states

if __name__ == "__main__":
    # Example usage
    relais_config = {"relais_1": 17, "relais_2": 27, "relais_3": 22}
    my_relais = Relais(relais_config)

    # Operate relais
    my_relais.operate_relais([{"relais_1": True}, {"relais_2": False}])

    # Get current states
    print(my_relais.get_relais_states())
    #  [5,6,19,13]