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
        logging.error('[EXE] Error at %d position: %s', node.get_state().get_pos(), message)
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
            if node.op2 is not None:
                node.op2 = self.execute(node.op2)

            # [NON-END] OP1/OP2 nodes
            # set
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

            # ? + ?
            if node.get_name() is LibParse.ADD:
                # check op1
                op1, err = self._check_var_calc(node.op1, 1)

                if err is not None:
                    return err

                # check op2
                op2, err = self._check_var_calc(node.op2, 1)

                if err is not None:
                    return err

                node.result = DataStore(ExeLib.TYPE_NUMBER, op1 + op2)
                return node

        # TODO: remove it
        return node

        # get result
        if node.get_name() is LibParse.PROGRAM:
            return node

    def _check_var_calc(self, op_node, op_debug_index=0):
        # if op_node is
        if op_node.get_name() is LibParse.NUMBER:
            op1 = int(op_node.get_value())
            return op1, None

        # if op_node is variable
        elif op_node.get_name() is LibParse.VARIABLE:
            op1 = self.scope.get(op_node.get_value()).value

            if op1 is None:
                return None, self.error(op_node, ('Variable %s not defined' % op_node.get_value()))

            return op1, None

        # wrong op_node
        else:
            return None, self.error(op_node, 'Incorrect ADD statement (wrong op%d type %s)' % (op_debug_index, op_node.get_name()))
