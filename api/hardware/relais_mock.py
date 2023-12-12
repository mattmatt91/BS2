class MockRelais:
    def __init__(self, relais_config:dict):
 
        # relais_config is a dict with relais names and corresponding mock pin numbers
        self.relaiss = relais_config
        self.relais_states = {relais: False for relais in self.relaiss}  # False indicates closed

    def operate_relais(self, relais_operations):
        # relais_operations is a list of dicts, each dict contains relais name and a Boolean
        for operation in relais_operations:
                state = relais_operations[operation]
                if operation in self.relaiss:
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
    mock_relaiss = MockRelais(relais_config)

    # Operate relaiss
    mock_relaiss.operate_relais([{"relais_1": True}, {"relais_2": False}])

    # Get current states
    print(mock_relaiss.get_relais_states())
