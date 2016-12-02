import logging

from exe.data_store import DataStore
from exe.exe_lib import ExeLib


class Scope:
    def __init__(self, parent_scope):
        self._parent = parent_scope
        self._child = []
        self._scope = {}

    def error(self, message):
        logging.error('[SCOPE] %s', message)
        return None

    def add_child(self, scope):
        self._child.append(scope)

    def get_value(self, name, default_value=None, find_in_parents=True):
        if name not in self._scope:
            if not find_in_parents:
                return None, self.error('Get: Unknown variable, name: %s' % name)

            if self._parent is None:
                return None, self.error('Get: Unknown variable [and no parents], name: %s' % name)

            return self._parent.get_value(name, default_value, find_in_parents)

        return self._scope.get(name, default_value), None

    def set_value(self, name, data_type, value, set_in_parents=True):
        if name not in self._scope:
            if not set_in_parents:
                return None, self.error('Set: Unknown variable, name: %s' % name)

            if self._parent is None:
                return None, self.error('Set: Unknown variable [and no parents], name: %s' % name)

            return self._parent.set_value(name, data_type, value, set_in_parents)

        return self._scope[name].set_value(data_type, value), None

    def add_value(self, name, data_type, init_value):
        if name in self._scope:
            return None, self.error('Variable already declared, name: %s' % name)

        if data_type not in [ExeLib.TYPE_NUMBER]:
            return None, self.error('Unsupported type, type: %s' % data_type)

        self._scope[name] = DataStore(data_type, init_value)
        return init_value, None
