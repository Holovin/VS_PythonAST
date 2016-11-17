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
        exit(1)

    def parse(self):
        node = Node(LibParse.PROGRAM, None, op1=self.z_statement())

        if self.get_token_type() is not LibState.STATE_EOF:
            logging.error('Invalid statement! END')

        return node

    # statement: compound-st (check {)
    #            expression-st (all others!)
    #            selection-st (check IF)
    #            iteration-st (check FOR)
    def z_statement(self):

        # compound-st
        if self.get_token_type() is LibState.STATE_BRACE_FIG_OPEN:
            node = self.z_compound_st()

        # selection-st
        elif self.get_token_type() is LibState.STATE_IF:
            node = self.z_selection_st()

        # iteration-st
        elif self.get_token_type() is LibState.STATE_FOR:
            node = self.z_iteration_st()

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
    #                  block-item-list block-item [?]
    def z_block_item_list(self):

        # block-item
        node = self.z_block_item()

        # TODO: refactor
        while self.get_token_type() is not LibState.STATE_BRACE_FIG_CLOSE and node is not None:
            node = Node(LibParse.LIST, None, op1=node, op2=self.z_block_item())

        return node

    # block-item: declaration
    #             statement
    def z_block_item(self):

        # declaration
        if self.get_token_type() in [LibState.STATE_INT, LibState.STATE_DOUBLE]:
            node = self.z_declaration()

        # statement
        else:
            node = self.z_statement()

        return node

    # declaration: int IDENTITY
    #              double IDENTITY
    def z_declaration(self):
        node = None

        # int IDENTITY
        if self.get_token_type() is LibState.STATE_INT:
            # skip `int`
            st = self.get_token_current_and_skip()

            # check id
            if self.get_token_type() is not LibState.STATE_IDENTITY:
                self.error('Wrong identity name (1)')

            # TODO: save context?
            node = Node(LibParse.VAR_INT, self.get_token_current_and_skip()
)
        # double IDENTITY
        elif self.get_token_type() is LibState.STATE_DOUBLE:
            # skip `double`
            st = self.get_token_current_and_skip()

            # check id
            if self.get_token_type() is not LibState.STATE_IDENTITY:
                self.error('Wrong identity name (2)')

            # take id
            node = Node(LibParse.VAR_DOUBLE, self.get_token_current_and_skip())

        # error
        else:
            self.error('Unknown variable declaration')

        return node

    # iteration_st: for (expression [opt]; expression [opt]; expression [opt]) statement
    def z_iteration_st(self):

        # for
        for_st = self.get_token_current_and_skip()

        # check `(`
        if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_OPEN:
            self.error('Waiting `(` for start FOR statement')

        # skip `(`
        self.get_token_next()

        for_init = Node(LibParse.NOOP, None)
        for_condition = Node(LibParse.NOOP, None)
        for_after = Node(LibParse.NOOP, None)

        # for: try parse for_init part
        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            for_init = self.z_expression_logic()

        # skip `;`
        self.get_token_next()

        # for: try parse for_condition part
        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            for_condition = self.z_expression_logic()

        # skip `;`
        self.get_token_next()

        # for: try parse for_after part
        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            for_after = self.z_expression_logic()

        # check `)`
        if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_CLOSE:
            self.error('Waiting `)` for end FOR statement')

        # skip `)`
        self.get_token_next()

        for_body = self.z_statement()

        return Node(LibParse.FOR, for_st, op1=for_init, op2=for_condition, op3=for_after, op4=for_body)

    # selection-st: if (expression) statement
    #               if (expression) statement else statement
    def z_selection_st(self):

        # if
        if_st = self.get_token_current_and_skip()

        # (expression)
        expression = self.y_brace_handler()

        # statement
        statement = self.z_statement()

        # else?
        else_st = None

        # check else
        if self.get_token_type() is LibState.STATE_ELSE:
            # skip else keyword
            self.get_token_next()

            # parse else
            else_st = self.z_statement()

        return Node(LibParse.IF, if_st, op1=expression, op2=statement, op3=else_st)

    # expression-st: expression [opt];
    def z_expression_st(self):
        node = Node(LibParse.EXPRESSION_ST, None, op1=self.z_expression_logic())

        if self.get_token_type() is not LibState.STATE_SEMICOLON:
            self.error('Waiting ; symbol ')

        # skip `;`
        self.get_token_next()

        return node

    # expression_logic: expression_excl == expression_excl
    #                   expression_excl && expression_excl
    #                   expression_excl || expression_excl
    #                   expression_excl >= expression_excl
    #                   expression_excl > expression_excl
    #                   expression_excl <= expression_excl
    #                   expression_excl < expression_excl
    def z_expression_logic(self):
        node = self.z_expression_excl()

        # expression == expression
        if self.get_token_type() is LibState.STATE_EQUAL_TWICE:
            node = Node(LibParse.EXPRESSION_COMPARE, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression && expression
        elif self.get_token_type() is LibState.STATE_AMP_TWICE:
            node = Node(LibParse.EXPRESSION_AND, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression || expression
        elif self.get_token_type() is LibState.STATE_V_LINE_TWICE:
            node = Node(LibParse.EXPRESSION_OR, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression >= expression
        elif self.get_token_type() is LibState.STATE_MORE_EQUAL:
            node = Node(LibParse.EXPRESSION_MORE_EQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression > expression
        elif self.get_token_type() is LibState.STATE_MORE:
            node = Node(LibParse.EXPRESSION_MORE, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression <= expression
        elif self.get_token_type() is LibState.STATE_LESS_EQUAL:
            node = Node(LibParse.EXPRESSION_LESS_EQUAL, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        # expression < expression
        elif self.get_token_type() is LibState.STATE_LESS:
            node = Node(LibParse.EXPRESSION_LESS, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_excl())

        return node

    # expression_excl: expression
    #                  !expression
    def z_expression_excl(self):

        # !expression
        if self.get_token_type() is LibState.STATE_EXCL:
            node = Node(LibParse.EXPRESSION_EXCL, self.get_token_current_and_skip(), op1=self.z_expression())

        # expression
        else:
            node = self.z_expression()

        return node

    # expression: id = expression
    #             expression + term
    #             expression - term
    #             term
    def z_expression(self):
        # term
        node = self.z_term()

        # id = ...
        if node is not None and node.get_name() is LibParse.VARIABLE and self.get_token_type() is LibState.STATE_EQUAL:
            node = Node(LibParse.SET, self.get_token_current_and_skip(), op1=node, op2=self.z_expression_logic())

        # expression + term
        elif node is not None and self.get_token_type() is LibState.STATE_PLUS:
            node = Node(LibParse.ADD, self.get_token_current_and_skip(), op1=node, op2=self.z_term())

        # expression - term
        elif node is not None and self.get_token_type() is LibState.STATE_MINUS:
            node = Node(LibParse.SUB, self.get_token_current_and_skip(), op1=node, op2=self.z_term())

        return node

    # term: term * factor
    #       term / factor
    #       term % factor
    #       factor
    def z_term(self):

        # factor
        node = self.z_factor()

        # term * factor
        if node is not None and self.get_token_type() is LibState.STATE_MUL:
            node = Node(LibParse.MUL, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

        # term / factor
        elif node is not None and self.get_token_type() is LibState.STATE_SLASH:
            node = Node(LibParse.DIV, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

        # term % factor
        elif node is not None and self.get_token_type() is LibState.STATE_PERCENT:
            node = Node(LibParse.MOD, self.get_token_current_and_skip(), op1=node, op2=self.z_factor())

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

        # number: integer
        elif self.get_token_type() is LibState.STATE_INTEGER_NUMBER:
            node = Node(LibParse.INTEGER, self.get_token_current())
            self.get_token_next()
            return node

        elif self.get_token_type() is LibState.STATE_DOUBLE_NUMBER:
            node = Node(LibParse.DOUBLE, self.get_token_current())
            self.get_token_next()
            return node

        # (expression)
        return self.y_brace_handler()

    # (expression)
    # NOTE: helper function for prevent code duplicate
    def y_brace_handler(self):

        # check (
        if self.get_token_type() is LibState.STATE_BRACE_CIRCLE_OPEN:
            # inner expression
            node = Node(LibParse.EXPRESSION_INNER, self.get_token_current_and_skip(), op1=self.z_expression_logic())

            # check )
            if self.get_token_type() is not LibState.STATE_BRACE_CIRCLE_CLOSE:
                self.error('Waiting ) symbol')

            # skip )
            self.get_token_next()

            return node

        # unknown
        else:
            self.error("Unknown state, possible wait ( symbol")

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

        if node.op4 is not None:
            self.show_node(node.op4, level + 1)
