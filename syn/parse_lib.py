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

    # Operations: math
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'

    # Logical
    SET = 'SET'
    LESS = 'LESS <'
    MORE = 'MORE >'

    # Types
    # Common for all variables
    VARIABLE = 'VARIABLE'

    # Declaration types
    VAR_INT = 'VAR_INT'
    VAR_BOOL = 'VAR_BOOL'

    # Values
    VAL_NUMBER = 'VAL_NUMBER'
    VAL_BOOL = 'VAL_BOOL'

    # Other
    NOOP = 'NOOP'
