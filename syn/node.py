class Node:
    name = None

    # class
    state = None

    # value
    result = None

    # nodes
    op1 = None
    op2 = None
    op3 = None
    op4 = None

    def __init__(self, name, state, result=None, op1=None, op2=None):
        self.name = name                # Parser.*
        self.state = state              # instance of [StateData] class
        self.result = result            # save result after evaluating expr

        self.op1 = op1
        self.op2 = op2

    def get_name(self):
        return self.name

    def get_state(self):
        return self.state
