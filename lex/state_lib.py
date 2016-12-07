class LibState:
    # single chars
    CHAR_SPACE = ' '
    CHAR_SEMICOLON = ';'
    CHAR_SLASH = '/'
    CHAR_EQUAL = '='
    CHAR_MINUS = '-'
    CHAR_PLUS = '+'
    CHAR_MUL = '*'
    CHAR_LESS = '<'
    CHAR_MORE = '>'
    CHAR_SHARP = '#'
    CHAR_EXCL = '!'
    CHAR_AND = '&'
    CHAR_OR = '|'
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
    STATES_WRONG_END = []

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

    # logic
    STATE_CMP_LESS = 'Single: `<`'
    STATE_CMP_LESS_EQUAL = 'Twice: `<=`'

    STATE_CMP_MORE = 'Single: `>`'
    STATE_CMP_MORE_EQUAL = 'Twice: `>=`'

    STATE_CMP_EQUAL = 'Twice: `==`'

    STATE_CMP_EXCL = 'Single: `!`'
    STATE_CMP_NEQUAL = 'Twice: `!=`'

    STATE_OR = 'Single: `|`'
    STATE_CMP_OR = 'Twice: `||`'

    STATE_AND = 'Single: `&`'
    STATE_CMP_AND = 'Twice: `&&`'

    STATE_SET = 'Single: `=`'

    # value
    STATE_NUMBER = 'Integer: value'
    STATE_BOOL = 'Bool: value'

    # vars
    STATE_IDENTITY = 'Identity'

    # v - va - var
    STATE_V = STATE_IDENTITY
    STATE_VA = STATE_IDENTITY
    STATE_VAR = 'VAR'

    # true
    STATE_T = STATE_IDENTITY
    STATE_TR = STATE_IDENTITY
    STATE_TRU = STATE_IDENTITY
    STATE_TRUE = 'Bool: true'

    # false
    WORD_FALSE = 'false'
    STATE_F = STATE_IDENTITY
    STATE_FA = STATE_IDENTITY
    STATE_FAL = STATE_IDENTITY
    STATE_FALS = STATE_IDENTITY
    STATE_FALSE = 'Bool: false'

    # i - if
    STATE_I = STATE_IDENTITY
    STATE_IN = STATE_IDENTITY
    STATE_IF = 'IF'

    # other
    STATE_SPACE = 'Single: ` `'
    STATE_NEW_LINE = 'Single: `\\n`'
    STATE_CARET = 'Single: `\\r`'
    STATE_COMMENT = 'Comment'

    # --- types ---
    TYPE_OK = 'OK'
    TYPE_SKIP = 'SKIP'
    TYPE_ERROR = 'ERR'
