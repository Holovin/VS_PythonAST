class LibState:
    # single chars
    CHAR_DOT = '.'
    CHAR_SPACE = ' '
    CHAR_SEMICOLON = ';'
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
    CHAR_CARET = '\r'
    CHAR_NEW_LINE = '\n'

    # braces
    CHAR_BRACE_CIRCLE_OPEN = '('
    CHAR_BRACE_CIRCLE_CLOSE = ')'
    CHAR_BRACE_FIG_OPEN = '{'
    CHAR_BRACE_FIG_CLOSE = '}'

    # --- states ---
    # state machine
    STATE_START = '[START]'
    STATE_ERROR = '[ERROR]'
    STATE_END = '[END]'
    STATE_EOF = '[EOF]'

    # braces
    STATE_BRACE_FIG_OPEN = 'Brace: `{` (fig open)'
    STATE_BRACE_FIG_CLOSE = 'Brace: `}` (fig close)'
    STATE_BRACE_CIRCLE_OPEN = 'Brace: `(` (circle open)'
    STATE_BRACE_CIRCLE_CLOSE = 'Brace: `)` (circle close)'

    # single symbols
    STATE_EXCL = 'Single: `!`'
    STATE_SEMICOLON = 'Single: `;`'
    STATE_SLASH = 'Single: `/`'

    # math and arithmetic
    STATE_PERCENT = 'Single: `%`'
    STATE_MUL = 'Single: `*`'
    STATE_PLUS = 'Single: `+`'
    STATE_MINUS = 'Single: `-`'

    # single with pair
    STATE_AMP = 'Single: `&`'
    STATE_AMP_TWICE = 'Double: `&&`'

    STATE_V_LINE = 'Single: `|`'
    STATE_V_LINE_TWICE = 'Double: `||`'

    STATE_EQUAL = 'Single: `=`'
    STATE_EQUAL_TWICE = 'Double: `==`'

    STATE_LESS = 'Single: `<`'
    STATE_LESS_EQUAL = 'Double: `<=`'

    STATE_MORE = 'Single: `>`'
    STATE_MORE_EQUAL = 'Double: `>=`'

    # numbers
    STATE_INTEGER_NUMBER = 'Integer: value'
    STATE_DOUBLE_NUMBER_START = STATE_INTEGER_NUMBER  # 12. = 12
    STATE_DOUBLE_NUMBER = 'Double: value'

    # vars
    STATE_IDENTITY = 'Identity'

    # i - if - int
    STATE_I = STATE_IDENTITY
    STATE_IF = 'IF'
    STATE_IN = STATE_IDENTITY
    STATE_INT = 'INT'

    # e - el - els - else
    STATE_E = STATE_IDENTITY
    STATE_EL = STATE_IDENTITY
    STATE_ELS = STATE_IDENTITY
    STATE_ELSE = 'ELSE'

    # f - fo - for
    STATE_F = STATE_IDENTITY
    STATE_FO = STATE_IDENTITY
    STATE_FOR = 'FOR'

    # d - do - dou - doub - doubl - double
    STATE_D = STATE_IDENTITY
    STATE_DO = STATE_IDENTITY
    STATE_DOU = STATE_IDENTITY
    STATE_DOUB = STATE_IDENTITY
    STATE_DOUBL = STATE_IDENTITY
    STATE_DOUBLE = 'DOUBLE'

    # other
    STATE_SPACE = 'Single: ` `'
    STATE_NEW_LINE = 'Single: `\\n`'
    STATE_CARET = 'Single: `\\r`'

    #
    STATES_WRONG_END = []

    # --- types ---
    TYPE_OK = 'OK'
    TYPE_SKIP = 'SKIP'
    TYPE_ERROR = 'ERR'
