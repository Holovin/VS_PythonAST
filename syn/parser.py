import logging

from lex.state_lib import LibState
from syn.node import Node
from syn.parse_lib import LibParse


class Parser:
    tokens = None
    tokens_size = 0
    index = 0

    token_type = None

    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens_size = len(self.tokens)
        self.index = -1
        self.get_token_next()

    def get_token_next(self):
        if self.tokens_size <= self.index + 1:
            logging.debug("Trying take next, when is empty (size: %d <= try take: %d)", self.tokens_size, self.index+1)
            return None

        self.index += 1
        self.token_type = self.get_token_current().get_type()

        return self.get_token_current()

    def get_token_type(self):
        return self.token_type

    def get_token_current(self):
        return self.tokens[self.index]

    def get_token_current_and_skip(self):
        current = self.get_token_current()

        self.get_token_next()

        return current

    def error(self, message):
        logging.error("Error at %d position: found: %s. %s", self.get_token_current().get_pos(), self.get_token_type(), message)

    def parse(self):
        node = Node(LibParse.STATEMENT, None, op1=self.z_statement())

        if self.get_token_type() is not LibState.STATE_EOF:
            logging.error('Invalid statement!')

        return node

    # statement: TODO: compound-st (check {)
    #            expression-st (all others!)
    #            TODO: selection-st (check IF)
    #            TODO: iteration-st (check FOR)
    def z_statement(self):
        if False:
            # TODO
            node = ''

        else:
            # expression-st
            node = Node(LibParse.STATEMENT, None, op1=self.z_expression_st())
            self.get_token_next()

        return node

    # expression-st: expression [opt];
    def z_expression_st(self):
        node = Node(LibParse.EXPRESSION_ST, None, op1=self.z_expression())

        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            self.error('Waiting ; symbol ')

        self.get_token_next()

        return node

    # expression: id = expression
    #             TODO: do much others
    def z_expression(self):
        node = self.z_term()

        # id = ...
        if node.get_name() is LibParse.VARIABLE and self.get_token_type() is LibState.STATE_EQUAL:
            node = Node(LibParse.SET, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

        # expression + term
        if node is not None and self.get_token_type() is LibState.STATE_PLUS:
            node = Node(LibParse.ADD, self.get_token_current_and_skip(), op1=node, op2=self.z_term())

        return node

    # term: term * factor
    #       term / factor
    #       term % factor
    #       factor
    def z_term(self):
        node = self.z_factor()

        # term * factor
        if node is not None and self.get_token_type() is LibState.STATE_MUL:
            node = Node(LibParse.MUL, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

        elif self.get_token_type() is LibState.STATE_SLASH:
            pass

        elif self.get_token_type() is LibState.STATE_PERCENT:
            pass

        return node

    # factor: (expression)
    #         id
    #         number
    def z_factor(self):
        # id
        if self.get_token_type() is LibState.STATE_IDENTITY:
            node = Node(LibParse.VARIABLE, self.get_token_current())
            self.get_token_next()
            return node

        # number: integer
        elif self.get_token_type() is LibState.STATE_INT:
            node = Node(LibParse.INTEGER, self.get_token_current())
            self.get_token_next()
            return node

        elif self.get_token_type() is LibState.STATE_FLOAT:
            node = Node(LibParse.FLOAT, self.get_token_current())
            self.get_token_next()
            return node

        elif self.get_token_type() is LibState.STATE_BRACE_CIRCLE_OPEN:
            if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_OPEN:
                self.error('Waiting ( symbol')

            # skip (
            self.get_token_next()

            # inner expression
            node = Node('WTF', None)

            # check )
            while self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_CLOSE:
                node = Node('IDK', None, op1=node, op2=self.z_expression())
                #self.error('Waiting ) symbol')

            # skip )
            self.get_token_next()

            return node

        return

    # common wrapper for (expression) in ANY place
    def y_brace_circle_inner_expression(self):
        if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_OPEN:
            self.error('Waiting ( symbol')

        # skip (
        self.get_token_next()

        # inner expression
        node = self.z_expression()

        # check )
        if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_CLOSE:
            self.error('Waiting ) symbol')

        # skip )
        self.get_token_next()

        return node

    def show_node(self, node, level):
        padding = '.' * level
        name = node.get_name()
        value = node.get_state().__str__()

        logging.debug('%s | name: %s | %s', padding, name, value)

        if node.op1 is not None:
            self.show_node(node.op1, level + 1)

        if node.op2 is not None:
            self.show_node(node.op2, level + 1)

        if node.op3 is not None:
            self.show_node(node.op3, level + 1)
