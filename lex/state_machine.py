import logging
import re

from lex.state_common import StateStart, StateError, StateEnd, StateStringEscapePrepare, StateStringInput, StateStringEscapeIgnore
from lex.state_data import StateData
from lex.state_lib import LibState


class StateMachine:
    # common
    current_state = StateStart()
    index = 0
    index_last = 0
    input_text = ''

    # current lex
    lex_start_position = 0
    lex_length = 0
    lex_text = ''
    lex = None

    # for output
    output = []

    def set_data(self, input_text):
        self.reset_data()
        self.input_text = input_text
        self.index_last = len(self.input_text)

    def reset_data(self):
        self.current_state = StateStart()
        self.index = 0
        self.index_last = 0
        self.input_text = ''
        self.output = []
        self.__clear_lex()

    def __skip_data(self):
        # fill last char if empty
        if self.lex_length == 0:
            self.lex_length = 1
            self.lex_text = self.input_text[self.index]

        data = StateData(self.current_state.get_str_name(), LibState.TYPE_ERROR, self.lex_text, self.lex_start_position, self.lex_length)
        self.output.append(data)
        logging.warning('Skip bad token: %s at %d position (len: %d, type: %s)', self.lex_text, self.lex_start_position, self.lex_length, LibState.TYPE_ERROR)

        self.index += 1
        self.__clear_lex()

    def __clear_lex(self):
        self.lex_length = 0
        self.lex_start_position = self.index
        self.lex_text = ''
        self.lex = None
        self.current_state = StateStart()

    def __end_lex(self):
        data = StateData(self.lex.get_str_name(), self.lex.get_str_type(), self.lex_text, self.lex_start_position, self.lex_length)
        self.output.append(data)
        logging.info('Parse "%s" token: %s at %d position (len: %d, type: %s)', self.lex.get_str_name(), self.lex_text, self.lex_start_position, self.lex_length, self.lex.get_str_type())
        self.__clear_lex()

    def __do_lex(self):
        self.lex = self.current_state
        self.lex_text += self.input_text[self.index]
        self.lex_length += 1
        self.index += 1

    def check(self):
        # something wrong
        if self.current_state.get_str_name() == LibState.STATE_ERROR:
            self.__skip_data()
            return

        # lex end
        if self.current_state.get_str_name() == LibState.STATE_END:
            self.__end_lex()
            return

        self.__do_lex()

        # check if last lex
        if self.index == self.index_last:

            # check if last token is valid and ended
            if self.current_state.get_str_name() not in LibState.STATES_WRONG_END:
                self.__end_lex()

            else:
                self.__skip_data()

    def parse_data(self):
        while self.index < len(self.input_text):
            self.current_state = self.current_state.get_next_state(self.input_text[self.index])
            self.check()

        return

    def get_tokens(self, state=None):
        if state is None:
            return self.output

        return [x for x in self.output if x.state_type in state]

    def show(self):
        print('--- Report --- ')
        p = re.compile('(\\n|\\r)')

        for lex in self.get_tokens():
            print('Pos: ' + str(lex.start_position) + ', len: ' + str(lex.length) + ', text: [' + p.sub('', lex.text) + '], type: ' + lex.state_class + ' | ' + lex.state_type)
