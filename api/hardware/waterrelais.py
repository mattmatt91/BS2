import pcf8574_io


class WaterRelais:
    def __init__(self, relais_config):
        self.expander = pcf8574_io.PCF(0x20)
        self.relais = relais_config
        for pin in self.relais:
            pin_i = int(self.relais[pin]["pin_i"])
            pin_o = int(self.relais[pin]["pin_o"])
            self.expander.pin_mode(f"p{pin_i}", "INPUT")
            self.expander.pin_mode(f"p{pin_o}", "INPUT")

    def operate_relais(self, relais_operations):
        for operation in relais_operations:

            state = relais_operations[operation]
            if operation in self.relais:
                self.expander.write(
                    self.relais[operation]["pin_o"], "HIGH" if state else "LOW"
                )
            else:
                print(f"relais '{operation}' not found.")

    def get_states(self):
        relais_states = {}
        for relais in self.relais:
            relais_states[relais] = not self.expander.read(self.relais[relais]["pin_i"])
        return relais_states
