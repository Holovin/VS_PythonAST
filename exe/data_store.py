class DataStore:
    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value

    def __repr__(self):
        return 'Type %s, value: %s.' % (self.data_type, self.value)

    def get_type(self):
        return self.data_type

    def set_value(self, data_type, value):
        # TODO: check various types when needed
        self.value = value

        return value
