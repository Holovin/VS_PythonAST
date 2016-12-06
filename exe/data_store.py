class DataStore:
    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value

    def __repr__(self):
        return 'Type %s, value: %s' % (self.data_type, self.value)

    def get_type(self):
        return self.data_type

    def get_value(self, data_type=None):
        if data_type is None:
            return self.value

        if self.data_type is data_type:
            return self.value

        raise Exception('Cant cast to %s' % data_type)

    def set_value(self, data_type, value):
        self.data_type = data_type
        self.value = value

        return value
