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
        logging.error('[PARSER] Error at %d position: found: %s. %s', self.get_token_current().get_pos(), self.get_token_type(), message)

    def parse(self):
        node = Node(LibParse.PROGRAM, None, op1=self.z_statement())

        if self.get_token_type() is not LibState.STATE_EOF:
            logging.error('Invalid statement at end!')

        return node

    # statement: compound-st (check {)
    #            expression-st (all others!)
    #            selection-st (check IF)
    def z_statement(self):

        # compound-st
        if self.get_token_type() is LibState.STATE_BRACE_FIG_OPEN:
            node = self.z_compound_st()

        # selection-st
        elif self.get_token_type() is LibState.STATE_IF:
            node = self.z_selection_st()

        else:
            # expression-st
            node = Node(LibParse.STATEMENT, None, op1=self.z_expression_st())

        return node

    # compound-st: {block-item-list [opt]}
    def z_compound_st(self):
        body = None

        # check `{`
        if self.get_token_type() is not LibState.STATE_BRACE_FIG_OPEN:
            self.error('Waiting `{` for compound statement')

        # skip `{`
        compound_st = self.get_token_current_and_skip()

        # try parse body (can be empty)
        if self.get_token_type() is not LibState.STATE_BRACE_FIG_CLOSE:
            body = self.z_block_item_list()

        # check `}`
        if self.get_token_type() is not LibState.STATE_BRACE_FIG_CLOSE:
            self.error('Waiting `}` for compound statement')

        # skip `}`
        self.get_token_next()

        return Node(LibParse.COMPOUND_ST, compound_st, op1=body)

    # block-item-list: statement
    #                  block-item-list statement
    def z_block_item_list(self):

        # block-item
        node = self.z_statement()

        # chain mode
        while self.get_token_type() not in [LibState.STATE_BRACE_FIG_CLOSE, LibState.STATE_EOF] and node is not None:
            node = Node(LibParse.LIST, None, op1=node, op2=self.z_statement())

        return node

    # selection-st: if (expression) statement
    def z_selection_st(self):
        
        # if
        if_st = self.get_token_current_and_skip()

        # (expression)
        expression = self.y_brace_handler()

        # statement
        statement = self.z_statement()

        return Node(LibParse.IF, if_st, op1=expression, op2=statement)

    # expression-st: expression [opt];
    def z_expression_st(self):

        # if empty expression
        if self.get_token_type() is LibState.STATE_SEMICOLON:
            self.get_token_next()
            return Node(LibParse.NOOP, None)

        # expression_set
        node = self.z_expression_set()

        # check correct end
        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            self.error('Waiting ; symbol ')

        # skip `;`
        self.get_token_next()

        return node

    # expression_set: id = expression
    #                 expression
    def z_expression_set(self):

        # expression
        node = self.z_expression()

        # id = ...
        if node is not None and node.get_name() is LibParse.VARIABLE and self.get_token_type() is LibState.STATE_EQUAL:
            node = Node(LibParse.SET, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

        return node

    # expression: expression + term
    #             expression - term
    #             term
    def z_expression(self):

        # term
        node = self.z_term()

        # chain mode enable
        while self.get_token_type() in [LibState.STATE_PLUS, LibState.STATE_MINUS] and node is not None:
            # expression + term
            if node is not None and self.get_token_type() is LibState.STATE_PLUS:
                node = Node(LibParse.ADD, self.get_token_current_and_skip(), op1=node, op2=self.z_term())

            # expression - term
            elif node is not None and self.get_token_type() is LibState.STATE_MINUS:
                node = Node(LibParse.SUB, self.get_token_current_and_skip(), op1=node, op2=self.z_term())

        return node

    # term: term * factor
    #       term / factor
    #       factor
    def z_term(self):

        # factor
        node = self.z_factor()

        # chain mode
        while self.get_token_type() in [LibState.STATE_MUL, LibState.STATE_SLASH] and node is not None:
            # term * factor
            if node is not None and self.get_token_type() is LibState.STATE_MUL:
                node = Node(LibParse.MUL, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

            # term / factor
            elif node is not None and self.get_token_type() is LibState.STATE_SLASH:
                node = Node(LibParse.DIV, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

        return node

    # factor: (expression)
    #         id
    #         number
    #
    # NOTE:   Deadlock state
    def z_factor(self):

        # id
        if self.get_token_type() is LibState.STATE_IDENTITY:
            node = Node(LibParse.VARIABLE, self.get_token_current())
            self.get_token_next()
            return node

        # numbers
        elif self.get_token_type() is LibState.STATE_NUMBER:
            node = Node(LibParse.NUMBER, self.get_token_current())
            self.get_token_next()
            return node

        # (expression)
        return self.y_brace_handler()

    # (expression)
    # NOTE: helper function for prevent code duplicate
    def y_brace_handler(self):

        # check (
        if self.get_token_type() is LibState.STATE_BRACE_CIRCLE_OPEN:

            current_token = self.get_token_current_and_skip()

            # err empty state
            if self.get_token_type() is LibState.STATE_BRACE_CIRCLE_CLOSE:
                self.error('Empty (...) state')

            # inner expression
            node = Node(LibParse.EXPRESSION_INNER, current_token, op1=self.z_expression())

            # check )
            if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_CLOSE:
                self.error('Waiting ) symbol')

            # skip )
            self.get_token_next()

            return node

        # unknown
        else:
            self.error('Unknown state, possible wait ( or ; symbols')
            if self.get_token_next() is None:
                return

    def show_node(self, node, level):
        padding = '.' * level * 3
        name = node.get_name()
        value = node.get_state().__str__()

        logging.debug('%s | name: %s | %s', padding, name, value)

        if node.op1 is not None:
            self.show_node(node.op1, level + 1)

        if node.op2 is not None:
            self.show_node(node.op2, level + 1)
