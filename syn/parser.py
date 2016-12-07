import logging

from config import Config
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
            logging.debug('[SYN] Trying take next, when is empty (size: %d <= try take: %d)', self.tokens_size, self.index + 1)
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
        logging.error('[SYN] Error at %d line and %d position: found: %s. %s', self.get_token_current().get_line(), self.get_token_current().get_pos(), self.get_token_type(), message)
        exit()

    def parse(self):
        node = Node(LibParse.PROGRAM, None, op1=self.z_statement())

        if self.get_token_type() is not LibState.STATE_EOF:
            logging.error('[SYN] Invalid statement at end!')

        return node

    # statement: compound-st (check {)
    #            expression-st (all others!)
    #            selection-st (check IF)
    #            while-st (while)
    def z_statement(self):

        # compound-st
        if self.get_token_type() is LibState.STATE_BRACE_FIG_OPEN:
            node = self.z_compound_st()

        # selection-st
        elif self.get_token_type() is LibState.STATE_IF:
            node = self.z_selection_st()

        # while-st
        elif self.get_token_type() is LibState.STATE_WHILE:
            node = self.z_while_st()

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

    # block-item-list: block-item
    #                  block-item-list statement
    def z_block_item_list(self):

        # block-item
        node = self.z_block_item()

        # chain mode
        while self.get_token_type() not in [LibState.STATE_BRACE_FIG_CLOSE, LibState.STATE_EOF] and node is not None:
            node = Node(LibParse.LIST, None, op1=node, op2=self.z_block_item())

        return node

    # block-item: declaration
    #             statement
    def z_block_item(self):

        # declaration
        if self.get_token_type() is LibState.STATE_VAR:
            node = self.z_declaration()

        # statement
        else:
            node = self.z_statement()

        return node

    # declaration: var IDENTITY
    def z_declaration(self):
        node = None

        # var IDENTITY
        if self.get_token_type() is LibState.STATE_VAR:
            # skip `int`
            st = self.get_token_current_and_skip()

            # check id
            if self.get_token_type() is not LibState.STATE_IDENTITY:
                self.error('Wrong identity name (1)')

            node = Node(LibParse.VAR_DECLARATION, self.get_token_current_and_skip())

            # check `;`
            if self.get_token_type() is not LibState.STATE_SEMICOLON:
                self.error('Wait `;` after var declaration')

            # skip `;`
            self.get_token_next()

        # error
        else:
            self.error('Unknown variable declaration')

        return node

    # selection-st: if (expression_less_more) statement
    def z_selection_st(self):

        # if
        if_st = self.get_token_current_and_skip()

        # (z_expression_or)
        expression = self.y_brace_handler()

        # statement
        statement = self.z_statement()

        return Node(LibParse.IF, if_st, op1=expression, op2=statement)

    # while-st: while (expression_less_more) statement
    def z_while_st(self):

        # while
        while_st = self.get_token_current_and_skip()

        # (z_expression_or)
        expression = self.y_brace_handler()

        # statement
        statement = self.z_statement()

        return Node(LibParse.WHILE, while_st, op1=expression, op2=statement)

    # expression-st: expression_set [opt];
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

    # expression_set: id = expression_equal
    #                 expression_equal
    def z_expression_set(self):

        # expression_equal
        node = self.z_expression_or()

        # [result == id] = ...
        if node is not None and node.get_name() is LibParse.VAR_LINK and self.get_token_type() is LibState.STATE_SET:
            node = Node(LibParse.SET, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_or())

        return node

    # expression_or: expression_and || expression_and
    #                expression_and
    def z_expression_or(self):

        # expression_equal
        node = self.z_expression_and()

        # expression_and || expression_and
        while self.get_token_type() is LibState.STATE_CMP_OR and node is not None:
            if self.get_token_type() is LibState.STATE_CMP_OR:
                node = Node(LibParse.OR, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_and())

        return node

    # expression_and: expression_equal && expression_equal
    #                 expression_equal
    def z_expression_and(self):

        # expression_equal
        node = self.z_expression_equal()

        # expression_and && expression_and
        while self.get_token_type() is LibState.STATE_CMP_AND and node is not None:
            if self.get_token_type() is LibState.STATE_CMP_AND:
                node = Node(LibParse.AND, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_equal())

        return node

    # expression_equal: expression_cmp_less_more != expression_cmp_less_more
    #                   expression_cmp_less_more == expression_cmp_less_more
    def z_expression_equal(self):

        # expression_cmp_less_more
        node = self.z_expression_less_more()

        # [expression_cmp_less_more] == [expression_cmp_less_more]
        if self.get_token_type() is LibState.STATE_CMP_EQUAL:
            node = Node(LibParse.EQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_less_more())

        # [expression_cmp_less_more] != [expression_cmp_less_more]
        elif self.get_token_type() is LibState.STATE_CMP_NEQUAL:
            node = Node(LibParse.NEQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_less_more())

        return node

    # expression_cmp_less_more: expression < expression
    #                           expression > expression
    #                           expression >= expression
    #                           expression <= expression
    #                           expression
    def z_expression_less_more(self):

        # expression_cmp_less_more
        node = self.z_expression()

        # [expression] < [expression]
        if self.get_token_type() is LibState.STATE_CMP_LESS:
            node = Node(LibParse.LESS, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

        # [expression] <= [expression]
        elif self.get_token_type() is LibState.STATE_CMP_LESS_EQUAL:
            node = Node(LibParse.LESS_EQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

        # [expression] > [expression]
        elif self.get_token_type() is LibState.STATE_CMP_MORE:
            node = Node(LibParse.MORE, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

        # [expression] >= [expression]
        elif self.get_token_type() is LibState.STATE_CMP_MORE_EQUAL:
            node = Node(LibParse.MORE_EQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression())

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

    # term: term * factor_excl
    #       term / factor_excl
    #       factor_excl
    def z_term(self):

        # factor
        node = self.z_factor_excl()

        # chain mode
        while self.get_token_type() in [LibState.STATE_MUL, LibState.STATE_SLASH] and node is not None:
            # term * factor
            if node is not None and self.get_token_type() is LibState.STATE_MUL:
                node = Node(LibParse.MUL, self.get_token_current_and_skip(), op1=node, op2=self.z_factor_excl())

            # term / factor
            elif node is not None and self.get_token_type() is LibState.STATE_SLASH:
                node = Node(LibParse.DIV, self.get_token_current_and_skip(), op1=node, op2=self.z_factor_excl())

        return node

    # factor_excl: !factor
    #              factor
    def z_factor_excl(self):

        # !expression
        if self.get_token_type() is LibState.STATE_CMP_EXCL:
            node = Node(LibParse.EXCL, self.get_token_current_and_skip(), op1=self.z_factor())

        # expression
        else:
            node = self.z_factor()

        return node

    # factor: (expression)
    #         id
    #         number
    #
    # NOTE:   Deadlock state
    def z_factor(self):

        # id
        if self.get_token_type() is LibState.STATE_IDENTITY:
            node = Node(LibParse.VAR_LINK, self.get_token_current())
            self.get_token_next()
            return node

        # numbers
        elif self.get_token_type() is LibState.STATE_NUMBER:
            node = Node(LibParse.VAL_NUMBER, self.get_token_current())
            self.get_token_next()
            return node

        # bool
        elif self.get_token_type() in [LibState.STATE_FALSE, LibState.STATE_TRUE]:
            node = Node(LibParse.VAL_BOOL, self.get_token_current())
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
            node = Node(LibParse.EXPRESSION_INNER, current_token, op1=self.z_expression_or())

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

    @staticmethod
    def show_node(node, level, op_id=0):
        padding = Config.LOG_PADDING_CHAR * level * Config.LOG_PADDING_MUL

        name = node.get_name()
        value = node.get_state().__str__()
        result = node.get_result()

        logging.debug('[SYN] (%d) %s | name: %s | %s | result: %s', op_id, padding, name, value, result)

        if node.op1 is not None:
            Parser.show_node(node.op1, level + 1, 1)

        if node.op2 is not None:
            Parser.show_node(node.op2, level + 1, 2)
