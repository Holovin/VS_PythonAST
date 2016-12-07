class LibParse:
    # Core
    PROGRAM = 'APP'
    STATEMENT = 'STATEMENT'

    # Statements
    EXPRESSION = 'EXPRESSION'
    EXPRESSION_ST = 'EXPRESSION_ST'
    EXPRESSION_INNER = 'EXPRESSION ( ... )'
    COMPOUND_ST = 'COMPOUND_ST'
    LIST = 'LIST'
    IF = 'IF'
    WHILE = 'WHILE'

    # Operations: math
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'

    # Logical
    SET = 'SET'
    EXCL = '!'
    LESS = 'LESS <'
    LESS_EQUAL = 'LESS_EQ <='
    MORE = 'MORE >'
    MORE_EQUAL = 'MORE_EQ >='
    EQUAL = 'EQUAL =='
    NEQUAL = '!EQUAL !='
    OR = 'OR ||'
    AND = 'AND &&'

    # Declaration
    VAR_DECLARATION = 'VAR_DECLARATION'

    # Types
    VAR_LINK = 'VAR_LINK'
    VAL_NUMBER = 'VAL_NUMBER'
    VAL_BOOL = 'VAL_BOOL'

    # Other
    NOOP = 'NOOP'
