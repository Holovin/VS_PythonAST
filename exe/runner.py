import logging

from exe.data_store import DataStore
from exe.exe_lib import ExeLib
from exe.scope import Scope
from syn.node import Node
from syn.parse_lib import LibParse


class Runner:
    def __init__(self, syn_tree):
        self.scope = Scope(None)
        self.tree = self.execute(syn_tree, self.scope)

    def error(self, node, message):
        logging.error('[EXE] Error at %d line and %d position: %s', node.get_state().get_line(), node.get_state().get_pos(), message)
        exit()
        return Node(LibParse.NOOP, None)

    def execute(self, node, scope):
        current_scope = scope

        # check if has result > go deeper
        if node.result is None:
            # create new scope
            if node.get_name() is LibParse.COMPOUND_ST:
                current_scope = Scope(scope)
                scope.add_child(current_scope)

            # [END] NO-OP nodes
            # number
            if node.get_name() is ExeLib.TYPE_NUMBER:
                node.result = DataStore(ExeLib.TYPE_NUMBER, int(node.get_value()))
                return node

            # variable
            if node.get_name() is ExeLib.TYPE_VARIABLE:
                node.result = DataStore(ExeLib.TYPE_VARIABLE, node.get_value())
                return node

            # var declaration
            if node.get_name() is LibParse.VAR_DECLARATION:
                node.result = DataStore(ExeLib.TYPE_NUMBER, 0)
                current_scope.add_value(node.get_value(), ExeLib.TYPE_NUMBER, 0)
                return node

            # [EXECUTE NODES]
            # try run 1st operator
            if node.op1 is not None:
                node.op1 = self.execute(node.op1, current_scope)

            # try run 2nd operator
            if node.op2 is not None and node.get_name() is not LibParse.IF:
                node.op2 = self.execute(node.op2, current_scope)

            # IF | if (?) ?
            if node.get_name() is LibParse.IF:
                val_condition, err = self._var_unpack(current_scope, node.op1, LibParse.IF)

                if err is not None:
                    return err

                # try cast result to BOOL and check result
                if val_condition.get_value(ExeLib.TYPE_BOOL):
                    logging.fatal(val_condition.get_value(ExeLib.TYPE_BOOL))
                    node.op2 = self.execute(node.op2, current_scope)

                # fake execute to check scope declarations
                else:
                    self.execute(node.op2, Scope(current_scope, True))

                return node

            # [NON-END] OP1/OP2 nodes
            # (...) <- just transport value
            if node.get_name() in LibParse.EXPRESSION_INNER:
                node.result = node.op1.get_result()
                return node

            # SET | VAR = ?
            if node.get_name() is LibParse.SET:
                # check op1 for var name
                if node.op1.get_name() is not LibParse.VAR_VAR:
                    return self.error(node, 'Incorrect SET statement (need variable name, but take %s)' % node.op1.get_name())

                # check if var exist in scope
                if current_scope.get_value(node.op1.get_result().value) is None:
                    return self.error(node, 'Incorrect SET statement (variable [ %s ] is not exist)' % node.op1.get_result())

                # try get op2 value from scope
                if node.op2.get_name() is LibParse.VAR_VAR:
                    value = current_scope.get_value(node.op2.get_result().value)

                # try get op2 value and check type from result
                elif type(node.op2.get_result()) is DataStore and node.op2.get_result().get_type() is ExeLib.TYPE_NUMBER:
                    value = node.op2.get_result().value

                else:
                    return self.error(node, 'Incorrect SET statement (need ID or VALUE, but take %s)' % node.op2.get_name())

                # TODO: bool support
                node.result = DataStore(ExeLib.TYPE_NUMBER, value)
                current_scope.set_value(node.op1.get_result().value, ExeLib.TYPE_NUMBER, value)

                return node

            # LESS | ? < ?
            if node.get_name() is LibParse.LESS:
                # check op1
                val_op1, err = self._var_unpack(scope, node.op1, LibParse.LESS)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._var_unpack(scope, node.op2, LibParse.LESS)

                if err is not None:
                    return err

                # compare if equal type
                if val_op1.get_type() is val_op2.get_type():
                    result = val_op1.get_value() < val_op2.get_value()

                # else False
                else:
                    result = False

                node.result = DataStore(ExeLib.TYPE_BOOL, result)
                return node

            # ADD | ? + ?
            if node.get_name() is LibParse.ADD:
                # check op1
                val_op1, err = self._var_unpack(scope, node.op1, LibParse.ADD)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._var_unpack(scope, node.op2, LibParse.ADD)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1.get_value(ExeLib.TYPE_NUMBER) + val_op2.get_value(ExeLib.TYPE_NUMBER))
                return node

            # SUB | ? - ?
            if node.get_name() is LibParse.SUB:
                # check op1
                val_op1, err = self._var_unpack(scope, node.op1, LibParse.SUB)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._var_unpack(scope, node.op2, LibParse.SUB)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1.get_value(ExeLib.TYPE_NUMBER) - val_op2.get_value(ExeLib.TYPE_NUMBER))
                return node

            # MUL | ? * ?
            if node.get_name() is LibParse.MUL:
                # check op1
                val_op1, err = self._var_unpack(scope, node.op1, LibParse.MUL)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._var_unpack(scope, node.op2, LibParse.MUL)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1.get_value(ExeLib.TYPE_NUMBER) * val_op2.get_value(ExeLib.TYPE_NUMBER))
                return node

            # DIV | ? / ?
            if node.get_name() is LibParse.DIV:
                # check op1
                val_op1, err = self._var_unpack(scope, node.op1, LibParse.DIV)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._var_unpack(scope, node.op2, LibParse.DIV)

                if err is not None:
                    return err

                # if div by 0
                if val_op2 == 0:
                    self.error(node, 'Division by zero')

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1.get_value(ExeLib.TYPE_NUMBER) // val_op2.get_value(ExeLib.TYPE_NUMBER))
                return node

        # get result
        if node.get_name() is LibParse.PROGRAM:
            self.scope = scope
            return node

        # just skip others
        return node

    def get_scope(self):
        return self.scope

    def _var_unpack(self, scope, op_node, op_name):
        # check if var exist in scope
        if type(op_node.get_result()) is DataStore and op_node.get_result().get_type() is ExeLib.TYPE_VARIABLE:
            value = scope.get_value(op_node.get_result().value)

            if value is None:
                return None, self.error(op_node, 'Incorrect %s statement (variable [ %s ] is not exist)' % (op_name, op_node.get_result()))

            return value, None

        # try get value and check type from result
        elif type(op_node.get_result()) is DataStore and op_node.get_result().get_type() is not ExeLib.TYPE_VARIABLE:
            value = op_node.get_result()
            return value, None

        else:
            return self.error(op_node, 'Incorrect %s statement (need ID or VALUE, but take %s)' % (op_name, op_node.get_name()))
