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
    EQUAL = 'EQUAL =='
    NEQUAL = '!EQUAL !='
    OR = 'OR ||'
    AND = 'AND &&'

    # Types
    # Declaration
    VAR_DECLARATION = 'VAR_DECLARATION'

    VAR_LINK = 'VAR_LINK'
    VAL_NUMBER = 'VAL_NUMBER'
    VAL_BOOL = 'VAL_BOOL'

    # Other
    NOOP = 'NOOP'
