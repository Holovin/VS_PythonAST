class StateData:
    state_class = None
    type = ''
    text = ''
    start_position = 0
    line = 0
    length = 0

    def __init__(self, state_class, state_type, text, line, start_position, length):
        self.state_class = state_class
        self.state_type = state_type
        self.text = text
        self.line = line
        self.start_position = start_position
        self.length = length

    def get_type(self):
        return self.state_class

    def get_pos(self):
        return self.start_position

    def get_line(self):
        return self.line

    def get_value(self):
        return self.text

    def __str__(self):
        return 'Name: %s, value: %s, display_line: %d, pos: %d, len: %d' % (self.state_class, self.text, self.line, self.start_position, self.length)
