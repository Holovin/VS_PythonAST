class LibState:
    # single chars
    CHAR_SPACE = ' '
    CHAR_SEMICOLON = ';'
    CHAR_SLASH = '/'
    CHAR_EQUAL = '='
    CHAR_MINUS = '-'
    CHAR_PLUS = '+'
    CHAR_MUL = '*'
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
    STATE_SEMICOLON = 'Single: `;`'
    
    # math and arithmetic
    STATE_PLUS = 'Single: `+`'
    STATE_MINUS = 'Single: `-`'
    STATE_MUL = 'Single: `*`'
    STATE_SLASH = 'Single: `/`'

    STATE_EQUAL = 'Single: `=`'

    # numbers
    STATE_NUMBER = 'Integer: value'

    # vars
    STATE_IDENTITY = 'Identity'

    # i - if - int
    STATE_I = STATE_IDENTITY
    STATE_IF = 'IF'

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
