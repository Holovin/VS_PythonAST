import logging

from exe.exe_lib import ExeLib


class DataStore:
    def __init__(self, data_type, value):
        self.data_type = data_type
        self.value = value

    def __repr__(self):
        return 'Type %s, value: %s' % (self.data_type, self.value)

    def get_type(self):
        return self.data_type

    def get_value(self, data_type=None):
        if data_type is None or self.data_type is data_type:
            return self.value

        return DataStore.cast(self, data_type).value

    def set_value(self, data_type, value):
        self.data_type = data_type
        self.value = value

        return value

    @staticmethod
    def cast(var, new_type):
        if var.get_type() is new_type:
            return var

        if var.get_type() is ExeLib.TYPE_NUMBER:
            return DataStore._cast_raw_int(var, new_type)

        if var.get_type() is ExeLib.TYPE_BOOL:
            return DataStore._cast_raw_bool(var, new_type)

        return None

    @staticmethod
    def _cast_raw_int(var, new_type):
        if new_type is ExeLib.TYPE_BOOL:
            return DataStore(ExeLib.TYPE_BOOL, var.get_value() != 0)

    @staticmethod
    def _cast_raw_bool(var, new_type):
        if new_type is ExeLib.TYPE_NUMBER:
            val = 0 if var.get_value() else 1
            return DataStore(ExeLib.TYPE_NUMBER, val)
