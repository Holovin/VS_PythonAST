import logging

from exe.data_store import DataStore
from exe.exe_lib import ExeLib
from syn.node import Node
from syn.parse_lib import LibParse


class Runner:
    def __init__(self, syn_tree):
        self.scope = {}
        self.tree = self.execute(syn_tree)

    def error(self, node, message):
        logging.error('[EXE] Error at %d line and %d position: %s', node.get_state().get_line(), node.get_state().get_pos(), message)
        exit()
        return Node(LibParse.NOOP, None)

    def execute(self, node):
        # check if has result > go deeper
        if node.result is None:

            # [END] NO-OP nodes
            # number
            if node.get_name() is LibParse.NUMBER:
                node.result = DataStore(ExeLib.TYPE_NUMBER, int(node.get_value()))
                return node

            # variable
            if node.get_name() is LibParse.VARIABLE:
                node.result = DataStore(ExeLib.TYPE_VARIABLE, node.get_value())
                return node

            # int declaration
            if node.get_name() is LibParse.VAR_INT:
                node.result = DataStore(ExeLib.TYPE_NUMBER, 0)
                self.scope[node.get_value()] = DataStore(ExeLib.TYPE_NUMBER, 0)
                return node

            # [EXECUTE NODES]
            # try run 1st operator
            if node.op1 is not None:
                node.op1 = self.execute(node.op1)

            # try run 2nd operator
            if node.op2 is not None and node.get_name() is not LibParse.IF:
                node.op2 = self.execute(node.op2)

            # IF | if (?) ?
            if node.get_name() is LibParse.IF:
                logging.fatal(node.op1.get_result())
                val_condition, err = self._check_var_calc(node.op1, LibParse.IF)

                if err is not None:
                    return err

                if val_condition != 0:
                    node.op2 = self.execute(node.op2)

                return node

            # [NON-END] OP1/OP2 nodes
            # (...) <- just transport value
            if node.get_name() in LibParse.EXPRESSION_INNER:
                node.result = node.op1.get_result()
                return node

            # SET | VAR = ?
            if node.get_name() is LibParse.SET:
                # check op1 for var name
                if node.op1.get_name() is not LibParse.VARIABLE:
                    return self.error(node, 'Incorrect SET statement (need variable name, but take %s)' % node.op1.get_name())

                # check if var exist in scope
                if self.scope.get(node.op1.get_result().value) is None:
                    return self.error(node, 'Incorrect SET statement (variable [ %s ] is not exist)' % node.op1.get_result())

                # try get op2 value from scope
                if node.op2.get_name() is LibParse.VARIABLE:
                    value = self.scope[node.op2.get_result().value]

                # try get op2 value and check type from result)
                elif type(node.op2.get_result()) is DataStore and node.op2.get_result().get_type() is ExeLib.TYPE_NUMBER:
                    value = node.op2.get_result().value

                else:
                    return self.error(node, 'Incorrect SET statement (need DataStore value, but take %s)' % node.op2.get_name())

                node.result = DataStore(ExeLib.TYPE_NUMBER, value)
                self.scope[node.op1.get_result().value] = DataStore(ExeLib.TYPE_NUMBER, value)
                return node

            # ADD | ? + ?
            if node.get_name() is LibParse.ADD:
                # check op1
                val_op1, err = self._check_var_calc(node.op1, LibParse.ADD)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._check_var_calc(node.op2, LibParse.ADD)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1 + val_op2)
                return node

            # SUB | ? - ?
            if node.get_name() is LibParse.SUB:
                # check op1
                val_op1, err = self._check_var_calc(node.op1, LibParse.SUB)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._check_var_calc(node.op2, LibParse.SUB)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1 - val_op2)
                return node

            # MUL | ? * ?
            if node.get_name() is LibParse.MUL:
                # check op1
                val_op1, err = self._check_var_calc(node.op1, LibParse.MUL)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._check_var_calc(node.op2, LibParse.MUL)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1 * val_op2)
                return node

            # DIV | ? / ?
            if node.get_name() is LibParse.DIV:
                # check op1
                val_op1, err = self._check_var_calc(node.op1, LibParse.DIV)

                if err is not None:
                    return err

                # check op2
                val_op2, err = self._check_var_calc(node.op2, LibParse.DIV)

                if err is not None:
                    return err

                # if div by 0
                if val_op2 == 0:
                    self.error(node, 'Division by zero')

                node.result = DataStore(ExeLib.TYPE_NUMBER, val_op1 // val_op2)
                return node

        # TODO: remove it
        return node

        # get result
        if node.get_name() is LibParse.PROGRAM:
            return node

    def _check_var_calc(self, op_node, op_name):
        # check if var exist in scope
        if type(op_node.get_result()) is DataStore and op_node.get_result().get_type() is ExeLib.TYPE_VARIABLE:
            if self.scope.get(op_node.get_result().value) is None:
                return None, self.error(op_node, 'Incorrect %s statement (variable [ %s ] is not exist)' % (op_name, op_node.get_result()))

            value = self.scope[op_node.get_result().value].value
            return value, None

        # try get value and check type from result
        elif type(op_node.get_result()) is DataStore and op_node.get_result().get_type() is ExeLib.TYPE_NUMBER:
            value = op_node.get_result().value
            return value, None

        else:
            return self.error(op_node, 'Incorrect %s statement (need DataStore value, but take %s)' % (op_name, op_node.get_name()))
