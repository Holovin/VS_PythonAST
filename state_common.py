import re
from abc import ABC, abstractmethod

from state_chars import LibState


class StateAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_next_state(self, char):
        pass


class StateError(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


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

        if char == LibState.CHAR_VLINE:
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

        if char == LibState.CHAR_PERC:
            return StatePerc()

        if char == LibState.CHAR_EXCL:
            return StateExcl()

        if char == LibState.CHAR_ESCAPE:
            return StateEscape()

        if char == LibState.CHAR_BRACE_CIRCLE_OPEN:
            return StateBraceCircleOpen()

        if char == LibState.CHAR_BRACE_CIRCLE_CLOSE:
            return StateBraceCircleClose()

        if char == LibState.CHAR_BRACE_FIG_OPEN:
            return StateBraceFigOpen()

        if char == LibState.CHAR_BRACE_FIG_CLOSE:
            return StateBraceFigClose()

        if char == LibState.CHAR_ENDSYMBOL:
            return _StateReturn()

        return StateError()


class StateEnd(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


def end_keyword_or_id_check(char):
    if char in LibState.CHAR_WORD_BREAKERS:
        return StateEnd()

    return StateIdentityInput()


class _StateReturn(StateAbstract):
    def get_next_state(self, char):
        return _StateReturn()


class StateBraceFigClose(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateBraceFigOpen(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateBraceCircleClose(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateBraceCircleOpen(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateEscape(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateExcl(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StatePerc(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateMul(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StatePlus(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateMinus(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_MORE:
            return StateMinusMore()

        return StateEnd()


class StateMinusMore(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateEqual(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateEqual2()

        return StateEnd()


class StateEqual2(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateDot(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_DOT:
            return StateDotLine()

        return StateEnd()


class StateLess(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateLessEq()

        return StateEnd()


class StateLessEq(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateMore(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateMoreEq()


class StateMoreEq(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateDotLine(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateAmp(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_AMP:
            return StateAmp2()

        return StateEnd()


class StateAmp2(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateSlash(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_EQUAL:
            return StateSlashEq()

        return StateEnd()


class StateSlashEq(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateVLine(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_VLINE:
           return StateVLine2()

        return StateEnd()


class StateVLine2(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateLetterV(StateAbstract):
    def get_next_state(self, char):
        if char == 'a':
            return StateLetterVa()

        return StateIdentityInput()


class StateLetterVa(StateAbstract):
    def get_next_state(self, char):
        if char == 'r':
            return StateVar()

        return StateIdentityInput()


class StateVar(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateLetterT(StateAbstract):
    def get_next_state(self, char):
        if char == 'y':
            return StateLetterTy()

        return StateIdentityInput()


class StateLetterTy(StateAbstract):
    def get_next_state(self, char):
        if char == 'p':
            return StateLetterTyp()

        return StateIdentityInput()


class StateLetterTyp(StateAbstract):
    def get_next_state(self, char):
        if char == 'e':
            return StateType()

        return StateIdentityInput()


class StateType(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateLetterO(StateAbstract):
    def get_next_state(self, char):
        if char == 'd':
            return StateOd()

        if char == 'f':
            return StateOf()

        return StateIdentityInput


class StateOd(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateOf(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateLetterD(StateAbstract):
    def get_next_state(self, char):
        if char == 'd':
            return StateDo()

        return StateIdentityInput()


class StateDo(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateLetterF(StateAbstract):
    def get_next_state(self, char):
        if char == 'i':
            return StateFi()

        return StateIdentityInput()


class StateFi(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateLetterI(StateAbstract):
    def get_next_state(self, char):
        if char == 'f':
            return StateIf()

        if char == 'n':
            return StateIn()

        return StateIdentityInput()


class StateIf(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateIn(StateAbstract):
    def get_next_state(self, char):
        return end_keyword_or_id_check(char)


class StateIdentityInput(StateAbstract):
    def get_next_state(self, char):
        if re.search('[a-z0-9_]', char):
            return StateIdentityInput()

        return StateEnd()


class StateStringInput(StateAbstract):
    def get_next_state(self, char):
        if char == LibState.CHAR_QUOTE:
            return StateString()

        if char == LibState.CHAR_ESCAPE:
            return StateStringEscapePrepare()

        return StateStringInput()


class StateStringEscapePrepare(StateAbstract):
    def get_next_state(self, char):
        return StateStringEscapeIgnore()


class StateStringEscapeIgnore(StateAbstract):
    def get_next_state(self, char):
        return StateStringInput()


class StateString(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateSemicolon(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateSpace(StateAbstract):
    def get_next_state(self, char):
        return StateEnd()


class StateInteger(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateInteger()

        if char == LibState.CHAR_DOT:
            return StateFloatStart()

        return StateEnd()


class StateFloatStart(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        return StateEnd()


class StateFloat(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        return StateEnd()
