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

        elif char == LibState.CHAR_SPACE:
            return StateSpace()

        elif char == LibState.CHAR_SEMICOLON:
            return StateSemicolon()

        else:
            return StateError()


class StateEnd(StateAbstract):
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

        elif char == LibState.CHAR_DOT:
            return StateFloatStart()

        else:
            return StateEnd()


class StateFloatStart(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        else:
            return StateError()


class StateFloat(StateAbstract):
    def get_next_state(self, char):
        if re.search('\d', char):
            return StateFloat()

        else:
            return StateEnd()
