import re
from abc import ABC, abstractmethod

from lex.state_lib import LibState


class StateAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_next_state(self, char):
        pass

    @abstractmethod
    def get_str_name(self):
        pass


class StateError(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_ERROR

class StateStart(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateInteger()

        if char == 'i':
            return StateLetterI()

        if char == 'f':
            return StateLetterF()

        if char == 'd':
            return StateLetterD()

        if char == 'o':
            return StateLetterO()

        if char == 't':
            return StateLetterT()

        if char == 'v':
            return StateLetterV()

        if re.search('[a-z]', char):
            return StateIdentityInput()

        if char == LibState.CHAR_SPACE:
            return StateSpace()

        if char == LibState.CHAR_SEMICOLON:
            return StateSemicolon()

        if char == LibState.CHAR_QUOTE:
            return StateStringInput()

        if char == LibState.CHAR_V_LINE:
            return StateVLine()

        if char == LibState.CHAR_SLASH:
            return StateSlash()

        if char == LibState.CHAR_AMP:
            return StateAmp()

        if char == LibState.CHAR_DOT:
            return StateDot()

        if char == LibState.CHAR_LESS:
            return StateLess()

        if char == LibState.CHAR_MORE:
            return StateMore()

        if char == LibState.CHAR_EQUAL:
            return StateEqual()

        if char == LibState.CHAR_MINUS:
            return StateMinus()

        if char == LibState.CHAR_PLUS:
            return StatePlus()

        if char == LibState.CHAR_MUL:
            return StateMul()

        if char == LibState.CHAR_PERCENT:
            return StatePercent()

        if char == LibState.CHAR_EXCL:
            return StateExcl()

        if char == LibState.CHAR_ESCAPE:
            # TODO: escape must be only from string classes?
            print("possible error?")
            return StateEscape()

        if char == LibState.CHAR_BRACE_CIRCLE_OPEN:
            return StateBraceCircleOpen()

        if char == LibState.CHAR_BRACE_CIRCLE_CLOSE:
            return StateBraceCircleClose()

        if char == LibState.CHAR_BRACE_FIG_OPEN:
            return StateBraceFigOpen()

        if char == LibState.CHAR_BRACE_FIG_CLOSE:
            return StateBraceFigClose()

        return StateError()

    def get_str_name(self):
        return LibState.STATE_START


class StateEnd(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_END


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


class StateEscape(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_ESCAPE


class StateExcl(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EXCL


class StatePercent(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_PERCENT


class StateMul(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MUL


class StatePlus(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_PLUS


class StateMinus(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_MORE:
            return StateArrow()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MINUS


class StateArrow(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_ARROW


class StateEqual(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateEqualTwice()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EQUAL


class StateEqualTwice(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_EQUAL_TWICE


class StateDot(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_V_LINE:
            return StateDotLine()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_DOT


class StateLess(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateLessEqual()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_LESS


class StateLessEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_LESS_EQUAL


class StateMore(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateMoreEqual()

    def get_str_name(self):
        return LibState.STATE_MORE


class StateMoreEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_MORE_EQUAL


class StateDotLine(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_DOT_LINE


class StateAmp(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_AMP:
            return StateAmpTwice()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_AMP


class StateAmpTwice(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_AMP_TWICE


class StateSlash(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateSlashEqual()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SLASH


class StateSlashEqual(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SLASH_EQUAL


class StateVLine(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_V_LINE:
           return StateVLine2()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_V_LINE


class StateVLine2(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_V_LINE_TWICE


class StateLetterV(StateAbstract):
    def get_next_state(self, char):
        if char == 'a':
            return StateLetterVa()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_V


class StateLetterVa(StateAbstract):
    def get_next_state(self, char):
        if char == 'r':
            return StateVar()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_VA


class StateVar(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_VAR


class StateLetterT(StateAbstract):
    def get_next_state(self, char):
        if char == 'y':
            return StateLetterTy()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_T


class StateLetterTy(StateAbstract):
    def get_next_state(self, char):
        if char == 'p':
            return StateLetterTyp()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_TY


class StateLetterTyp(StateAbstract):
    def get_next_state(self, char):
        if char == 'e':
            return StateType()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_TYP


class StateType(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_TYPE


class StateLetterO(StateAbstract):
    def get_next_state(self, char):
        if char == 'd':
            return StateOd()

        if char == 'f':
            return StateOf()

        return StateIdentityInput

    def get_str_name(self):
        return LibState.STATE_O


class StateOd(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_OD


class StateOf(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_OF


class StateLetterD(StateAbstract):
    def get_next_state(self, char):
        if char == 'd':
            return StateDo()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_D


class StateDo(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_DO


class StateLetterF(StateAbstract):
    def get_next_state(self, char):
        if char == 'i':
            return StateFi()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_F


class StateFi(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_FI


class StateLetterI(StateAbstract):
    def get_next_state(self, char):
        if char == 'f':
            return StateIf()

        if char == 'n':
            return StateIn()

        return StateIdentityInput()

    def get_str_name(self):
        return LibState.STATE_I


class StateIf(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_IF


class StateIn(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)

    def get_str_name(self):
        return LibState.STATE_IN


class StateIdentityInput(StateAbstract):
    def get_next_state(self, char):
        if re.search('[a-z0-9_]', char):
            return StateIdentityInput()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_IDENTITY


class StateStringInput(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_QUOTE:
            return StateStringLast()

        if char == LibState.CHAR_ESCAPE:
            return StateStringEscapePrepare()

        return StateStringInput()

    def get_str_name(self):
        return LibState.STATE_STR_INPUT


class StateStringEscapePrepare(StateAbstract):
    def get_next_state(self, char):
        return StateStringEscapeIgnore()

    def get_str_name(self):
        return LibState.STATE_STR_ESC_CHAR


class StateStringEscapeIgnore(StateAbstract):
    def get_next_state(self, char):
        return StateStringInput()

    def get_str_name(self):
        return LibState.STATE_STR_ESC


class StateStringLast(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_STR_LAST


class StateSemicolon(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SEMICOLON


class StateSpace(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_SPACE


class StateInteger(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateInteger()

        if char == LibState.CHAR_DOT:
            return StateFloatStart()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_INT


class StateFloatStart(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_FLOAT_START


class StateFloat(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        return StateEnd()

    def get_str_name(self):
        return LibState.STATE_FLOAT


def end_keyword_or_id_check(char):
    if char in LibState.CHAR_WORD_BREAKERS:
        return StateEnd()

    return StateIdentityInput()
