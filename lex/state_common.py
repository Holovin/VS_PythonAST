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

        # i: INT or [identity]
        if char == 'i':
            return StateLetterI()

        # f: FOR or [identity]
        if char == 'f':
            return StateLetterF()

        # d: DOUBLE or [identity]
        if char == 'd':
            return StateLetterD()

        # e: ELSE or [identity]
        if char == 'e':
            return StateLetterE()

        # [identity]
        if re.search('[a-z]', char):
            return StateIdentityInput()

        # [space]
        if char == LibState.CHAR_SPACE:
            return StateSpace()

        # ;
        if char == LibState.CHAR_SEMICOLON:
            return StateSemicolon()

        # | or ||
        if char == LibState.CHAR_V_LINE:
            return StateVLine()

        # /
        if char == LibState.CHAR_SLASH:
            return StateSlash()

        # & or &&
        if char == LibState.CHAR_AMP:
            return StateAmp()

        # < or <=
        if char == LibState.CHAR_LESS:
            return StateLess()

        # > or >=
        if char == LibState.CHAR_MORE:
            return StateMore()

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

        # %
        if char == LibState.CHAR_PERCENT:
            return StatePercent()

        # !
        if char == LibState.CHAR_EXCL:
            return StateExcl()

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


# Single: !
class StateExcl(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EXCL


# Single: %
class StatePercent(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_PERCENT


# Single: ":" (semicolon)
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
        if char == LibState.CHAR_EQUAL:
            return StateEqualTwice()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EQUAL


# Twice: ==
class StateEqualTwice(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EQUAL_TWICE


# Single: <
class StateLess(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateLessEqual()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_LESS


# Twice: <=
class StateLessEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_LESS_EQUAL


# Single: >
class StateMore(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateMoreEqual()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MORE


# Twice: >=
class StateMoreEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MORE_EQUAL


# Single: &
class StateAmp(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_AMP:
            return StateAmpTwice()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_AMP


# Twice: &&
class StateAmpTwice(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_AMP_TWICE


# Single: |
class StateVLine(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_V_LINE:
            return StateVLineTwice()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_V_LINE


# Twice: ||
class StateVLineTwice(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_V_LINE_TWICE


########################################################################################################################
# For statement
class StateLetterF(StateAbstract):
    def get_next_state(self, char):
        if char == 'o':
            return StateFo()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_F


class StateFo(StateAbstract):
    def get_next_state(self, char):
        if char == 'r':
            return StateFor()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_FO


class StateFor(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_FOR


########################################################################################################################
# Double statement
class StateLetterD(StateAbstract):
    def get_next_state(self, char):
        if char == 'o':
            return StateDo()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_D


class StateDo(StateAbstract):
    def get_next_state(self, char):
        if char == 'u':
            return StateDou()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DO


class StateDou(StateAbstract):
    def get_next_state(self, char):
        if char == 'b':
            return StateDoub()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DOU


class StateDoub(StateAbstract):
    def get_next_state(self, char):
        if char == 'l':
            return StateDoubl()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DOUB


class StateDoubl(StateAbstract):
    def get_next_state(self, char):
        if char == 'e':
            return StateDouble()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DOUBL


class StateDouble(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DOUBLE


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
# ELSE statements
class StateLetterE(StateAbstract):
    def get_next_state(self, char):
        if char == 'l':
            return StateEl()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_EL


class StateEl(StateAbstract):
    def get_next_state(self, char):
        if char == 's':
            return StateEls()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_EL


class StateEls(StateAbstract):
    def get_next_state(self, char):
        if char == 'e':
            return StateElse()

        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_ELS


class StateElse(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_ELSE


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

        if char == LibState.CHAR_DOT:
            return StateDoubleNumberStart()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_INTEGER_NUMBER


# Numbers: integer with .
class StateDoubleNumberStart(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateDoubleNumber()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_DOUBLE_NUMBER_START


# Numbers: double
class StateDoubleNumber(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateDoubleNumber()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_DOUBLE_NUMBER
