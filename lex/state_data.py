class StateData:
    state_class = None
    text = ''
    start_position = 0
    length = 0
    type = ''

    def __init__(self, state_class, state_type, text, start_position, length):
        self.state_class = state_class
        self.state_type = state_type
        self.text = text
        self.start_position = start_position
        self.length = length
