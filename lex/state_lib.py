class LibState:
    # single chars
    CHAR_DOT = '.'
    CHAR_SPACE = ' '
    CHAR_SEMICOLON = ';'
    CHAR_QUOTE = '"'
    CHAR_V_LINE = '|'
    CHAR_SLASH = '/'
    CHAR_EQUAL = '='
    CHAR_AMP = '&'
    CHAR_LESS = '<'
    CHAR_MORE = '>'
    CHAR_MINUS = '-'
    CHAR_PLUS = '+'
    CHAR_MUL = '*'
    CHAR_PERCENT = '%'
    CHAR_EXCL = '!'
    CHAR_ESCAPE = '\\'
    CHAR_CARET = '\r'
    CHAR_NEW_LINE = '\n'

    # braces
    CHAR_BRACE_CIRCLE_OPEN = '('
    CHAR_BRACE_CIRCLE_CLOSE = ')'
    CHAR_BRACE_FIG_OPEN = '{'
    CHAR_BRACE_FIG_CLOSE = '}'

    # dividers for identity symbols
    CHAR_WORD_BREAKERS = [CHAR_DOT, CHAR_SPACE, CHAR_QUOTE, CHAR_SEMICOLON, CHAR_NEW_LINE]

    # --- states ---
    # state machine
    STATE_START = '[START]'
    STATE_ERROR = '[ERROR]'
    STATE_END = '[END]'

    # braces
    STATE_BRACE_FIG_OPEN = 'Brace: fig open'
    STATE_BRACE_FIG_CLOSE = 'Brace: fig close'
    STATE_BRACE_CIRCLE_OPEN = 'Brace: circle open'
    STATE_BRACE_CIRCLE_CLOSE = 'Brace: circle close'

    # single symbols
    STATE_EXCL = 'Single: !'  # !
    STATE_ARROW = 'Single: arrow'
    STATE_SEMICOLON = 'Single: semicolon'

    # math and arithmetic
    STATE_PERCENT = 'Single: percent'
    STATE_MUL = 'Single: multiply'
    STATE_PLUS = 'Single: plus'
    STATE_MINUS = 'Single: minus'

    # single with pair
    STATE_SLASH = 'Single: slash'
    STATE_SLASH_EQUAL = 'Double: slash eq'

    STATE_AMP = 'Single: amp'
    STATE_AMP_TWICE = 'Double: amp amp'

    STATE_V_LINE = 'Single: v line'
    STATE_V_LINE_TWICE = 'Double: v line v line'

    STATE_EQUAL = 'Single: eq'
    STATE_EQUAL_TWICE = 'Double: eq eq'

    STATE_DOT = 'Single: dot'
    STATE_DOT_LINE = 'Double: dot line'

    STATE_LESS = 'Single: less'
    STATE_LESS_EQUAL = 'Double: less eq'

    STATE_MORE = 'Single: more'
    STATE_MORE_EQUAL = 'Double: more eq'

    # string
    STATE_STR_LAST = 'String'
    STATE_STR_ESC_CHAR = 'String (*1)'
    STATE_STR_ESC = 'String (*2)'
    STATE_STR_INPUT = 'String (*3)'

    # numbers
    STATE_INT = 'Integer'
    STATE_FLOAT_START = STATE_INT  # 12. = 12
    STATE_FLOAT = 'Float'

    # vars
    STATE_IDENTITY = 'ID'

    # v - var - var
    STATE_V = STATE_IDENTITY
    STATE_VA = STATE_IDENTITY
    STATE_VAR = 'VAR'

    # i - if - in
    STATE_I = STATE_IDENTITY
    STATE_IN = 'IN'
    STATE_IF = 'IF'

    # f - fi
    STATE_F = STATE_IDENTITY
    STATE_FI = 'FI'

    # d - do
    STATE_D = STATE_IDENTITY
    STATE_DO = 'DO'

    # o - of - od
    STATE_O = STATE_IDENTITY
    STATE_OF = 'OF'
    STATE_OD = 'OD'

    # t - ty - typ - type
    STATE_T = STATE_IDENTITY
    STATE_TY = STATE_IDENTITY
    STATE_TYP = STATE_IDENTITY
    STATE_TYPE = 'TYPE'

    # other
    STATE_SPACE = '[SPACE]'
    STATE_NEW_LINE = '[NEW LINE 1]'
    STATE_CARET = '[NEW LINE 2]'
    STATE_ESCAPE = 'Escape?'

    #
    STATES_WRONG_END = [STATE_STR_ESC, STATE_STR_ESC_CHAR, STATE_STR_INPUT]

    # --- types ---
    TYPE_OK = 'OK'
    TYPE_SKIP = 'SKIP'
    TYPE_ERROR = 'ERR'
