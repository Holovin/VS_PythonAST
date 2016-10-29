class Node:
    # class name
    state_type = ''

    # value
    data = ''

    # nodes
    left_node = None
    right_node = None

    def __init__(self, state_type, data, left_node, right_node):
        self.state_type = state_type    # LibState.STATE_*
        self.data = data                # save data after evaluating expr
        self.left_node = left_node      # another instance of [Node]
        self.right_node = right_node    # another instance of [Node]

        return