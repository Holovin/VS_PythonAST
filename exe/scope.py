import logging

from config import Config
from exe.data_store import DataStore
from exe.exe_lib import ExeLib


class Scope:
    def __init__(self, parent_scope, read_only=False):
        self.child = []
        self.parent = parent_scope
        self.scope = {}
        self.read_only = read_only

    def error(self, message):
        logging.error('[SCOPE] %s', message)
        return None

    def add_child(self, scope):
        self.child.append(scope)

    def get_parent(self, ignore_errors=False):
        if self.parent is not None:
            return self.parent

        if ignore_errors is False:
            self.error('Get_parent: Error, cant get parent scope')

        return None

    def get_value(self, name, default_value=None, find_in_parents=True):
        if name not in self.scope:
            if not find_in_parents:
                self.error('Get: Unknown variable, name: %s' % name)
                return None

            if self.parent is None:
                self.error('Get: Unknown variable [and no parents], name: %s' % name)
                return None

            return self.parent.get_value(name, default_value, find_in_parents)

        return self.scope.get(name, default_value)

    def set_value(self, name, data_type, value, set_in_parents=True):
        if name not in self.scope:
            if not set_in_parents:
                self.error('Set error: Unknown variable, name: %s' % name)
                return None

            if self.parent is None:
                self.error('Set error: Unknown variable [and no parents], name: %s' % name)
                return None

            if self.read_only is True:
                return None

            return self.parent.set_value(name, data_type, value, set_in_parents)

        if self.read_only is True:
            return None

        return self.scope[name].set_value(data_type, value)

    def add_value(self, name, data_type, init_value):
        if name in self.scope:
            self.error('Variable already declared, name: %s' % name)
            return None

        if data_type not in [ExeLib.TYPE_NUMBER]:
            self.error('Unsupported type, type: %s' % data_type)
            return None

        self.scope[name] = DataStore(data_type, init_value)
        return init_value

    @staticmethod
    def show_scope(scope, level=0):
        padding = Config.LOG_PADDING_CHAR * (level + 1) * Config.LOG_PADDING_MUL

        logging.debug('[SCOPE_OUT] %s L = %d, VARS = %s', padding, level, scope.scope.__str__())
        if len(scope.child) > 0:
            for s in scope.child:
                Scope.show_scope(s, level + 1)
