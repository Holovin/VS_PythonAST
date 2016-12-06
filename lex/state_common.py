import re
from abc import ABC, abstractmethod

from lex.state_lib import LibState


# Core: abstract state for others
class StateAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_next_state(self, char):
        pass

    @abstractmethod
    def get_str_name(self):
        pass

    def get_str_type(self):
        return LibState.TYPE_OK


########################################################################################################################
# Core: base state
class StateStart(StateAbstract):
    def get_next_state(self, char):
        # parse numbers
        if re.search('\d', char):
            return StateInteger()

        # i: [identity] or IF or INT
        if char == 'i':
            return StateLetterI()

        # [identity]
        if re.search('[a-z]', char):
            return StateIdentityInput()

        # [space]
        if char == LibState.CHAR_SPACE:
            return StateSpace()

        # [#]
        if char == LibState.CHAR_SHARP:
            return StateSharp()

        # ;
        if char == LibState.CHAR_SEMICOLON:
            return StateSemicolon()

        # /
        if char == LibState.CHAR_SLASH:
            return StateSlash()

        # = or ==
        if char == LibState.CHAR_EQUAL:
            return StateEqual()

        # +
        if char == LibState.CHAR_PLUS:
            return StatePlus()

        # -
        if char == LibState.CHAR_MINUS:
            return StateMinus()

        # *
        if char == LibState.CHAR_MUL:
            return StateMul()

        # (
        if char == LibState.CHAR_BRACE_CIRCLE_OPEN:
            return StateBraceCircleOpen()

        # )
        if char == LibState.CHAR_BRACE_CIRCLE_CLOSE:
            return StateBraceCircleClose()

        # {
        if char == LibState.CHAR_BRACE_FIG_OPEN:
            return StateBraceFigOpen()

        # }
        if char == LibState.CHAR_BRACE_FIG_CLOSE:
            return StateBraceFigClose()

        # \n
        if char == LibState.CHAR_NEW_LINE:
            return StateNewLine()

        # \r
        if char == LibState.CHAR_CARET:
            return StateCaret()

        # all others
        return StateError()

    def get_str_name(self):
        return LibState.STATE_START


# Core: last token state
class StateEnd(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_END


# Core: err state
class StateError(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_ERROR

    def get_str_type(self):
        return LibState.TYPE_ERROR


########################################################################################################################
class StateSharp(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_NEW_LINE or char == LibState.CHAR_CARET:
            return StateEnd()

        return StateSharp()

    def get_str_name(self):
        return LibState.STATE_COMMENT

    def get_str_type(self):
        return LibState.TYPE_SKIP


########################################################################################################################
# New line parse: \r and \n
class StateCaret(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_NEW_LINE:
            return StateNewLine()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_CARET

    def get_str_type(self):
        return LibState.TYPE_SKIP


class StateNewLine(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_CARET:
            return StateCaret()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_NEW_LINE

    def get_str_type(self):
        return LibState.TYPE_SKIP


########################################################################################################################
# Brace's: { }
class StateBraceFigOpen(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_BRACE_FIG_OPEN


class StateBraceFigClose(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_BRACE_FIG_CLOSE


# Brace's: ( )
class StateBraceCircleOpen(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_BRACE_CIRCLE_OPEN


class StateBraceCircleClose(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_BRACE_CIRCLE_CLOSE


########################################################################################################################
# Single: +
class StatePlus(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_PLUS


# Single: -
class StateMinus(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateInteger()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MINUS


# Single: *
class StateMul(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MUL


# Single: /
class StateSlash(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SLASH


# Single: ";" (semicolon)
class StateSemicolon(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SEMICOLON


# Single: " " (space)
class StateSpace(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SPACE

    def get_str_type(self):
        return LibState.TYPE_SKIP


########################################################################################################################
# Single: =
class StateEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EQUAL


########################################################################################################################
# IF and INT statements
class StateLetterI(StateAbstract):
    def get_next_state(self, char):
        if char == 'f':
            return StateIf()

        if char == 'n':
            return StateIn()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_I


# IF
class StateIf(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_IF


# INT
class StateIn(StateAbstract):
    def get_next_state(self, char):
        if char == 't':
            return StateInt()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_IN


class StateInt(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_INT

########################################################################################################################
# Identity
class StateIdentityInput(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_IDENTITY


def end_keyword_or_id_check(char):
    if re.search('[a-z0-9_]', char):
        return StateIdentityInput()

    return StateEnd()


########################################################################################################################
# Numbers: integer
class StateInteger(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateInteger()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_NUMBER
