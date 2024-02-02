class WaterRelaisMock:
    def __init__(self, relais_config):
        self.relais_states = {relais: False for relais in relais_config}
        self.relais = relais_config

    def operate_relais(self, relais_operations):
        for operation in relais_operations:

            state = relais_operations[operation]
            if operation in self.relais:
                self.relais_states[operation] = state
            else:
                print(f"relais '{operation}' not found.")

    def get_states(self):
        return self.relais_states


if __name__ == "__main__":
    # Example usage
    relais_config = {"relais_1": 17, "relais_2": 27, "relais_3": 22}
    my_relais = WaterRelaisMock(relais_config)

    # Operate relais
    my_relais.operate_relais([{"relais_1": True}, {"relais_2": False}])

    # Get current states
    print(my_relais.get_relais_states())
    #  [5,6,19,13]
