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

    # braces
    CHAR_BRACE_CIRCLE_OPEN = '('
    CHAR_BRACE_CIRCLE_CLOSE = ')'
    CHAR_BRACE_FIG_OPEN = '{'
    CHAR_BRACE_FIG_CLOSE = '}'

    # dividers for identity symbols
    CHAR_WORD_BREAKERS = [CHAR_DOT, CHAR_SPACE, CHAR_QUOTE, CHAR_SEMICOLON]

    # --- states ---
    # state machine
    STATE_ERROR = ''
    STATE_START = ''
    STATE_END = ''

    # braces
    STATE_BRACE_FIG_OPEN = ''
    STATE_BRACE_FIG_CLOSE = ''
    STATE_BRACE_CIRCLE_OPEN = ''
    STATE_BRACE_CIRCLE_CLOSE = ''

    # single symbols
    STATE_EXCL = ''  # !
    STATE_ARROW = ''
    STATE_SEMICOLON = ''

    # math and arithmetic
    STATE_PERCENT = ''
    STATE_MUL = ''
    STATE_PLUS = ''
    STATE_MINUS = ''

    # single with pair
    STATE_SLASH = ''
    STATE_SLASH_EQUAL = ''

    STATE_AMP = ''
    STATE_AMP_TWICE = ''

    STATE_V_LINE = ''
    STATE_V_LINE_TWICE = ''

    STATE_EQUAL = ''
    STATE_EQUAL_TWICE = ''

    STATE_DOT = ''
    STATE_DOT_LINE = ''

    STATE_LESS = ''
    STATE_LESS_EQUAL = ''

    STATE_MORE = ''
    STATE_MORE_EQUAL = ''

    # string
    STATE_STR_LAST = ''
    STATE_STR_ESC = None
    STATE_STR_ESC_CHAR = None
    STATE_STR_INPUT = None

    # numbers
    STATE_INT = None
    STATE_FLOAT_START = None
    STATE_FLOAT = None

    # vars
    STATE_IDENTITY = None

    # v - var - var
    STATE_V = ''
    STATE_VA = ''
    STATE_VAR = ''

    # i - if - in
    STATE_I = None
    STATE_IN = None
    STATE_IF = None

    # f - fi
    STATE_F = None
    STATE_FI = None

    # d - do
    STATE_D = None
    STATE_DO = None

    # o - of - od
    STATE_O = None
    STATE_OF = None
    STATE_OD = None

    # t - ty - typ - type
    STATE_T = None
    STATE_TY = None
    STATE_TYP = None
    STATE_TYPE = None

    # other
    STATE_SPACE = None
    STATE_ESCAPE = ''