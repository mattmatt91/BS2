class MockRelais:
    def __init__(self, relais_config:dict):
 
        # relais_config is a dict with relais names and corresponding mock pin numbers
        self.relais = relais_config
        self.relais_states = {relais: False for relais in self.relais}  # False indicates closed

    def operate_relais(self, relais_operations):
        # relais_operations is a list of dicts, each dict contains relais name and a Boolean
        for operation in relais_operations:
                state = relais_operations[operation]
                if operation in self.relais:
                    self.relais_states[operation] = state
                else:
                    print(f"relais '{operation}' not found.")

    def get_states(self):
        return self.relais_states
    
    def close(self):
        pass

if __name__ == "__main__":
    # Example usage
    relais_config = {"relais_1": 1, "relais_2": 2, "relais_3": 3}  # Mock pin numbers
    mock_relais = MockRelais(relais_config)

    # Operate relais
    mock_relais.operate_relais([{"relais_1": True}, {"relais_2": False}])

    # Get current states
    print(mock_relais.get_relais_states())
