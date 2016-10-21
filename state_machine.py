from state_lib import LibState
from state_common import StateStart, StateError, StateEnd, StateStringEscapePrepare, StateStringInput, \
    StateStringEscapeIgnore


class StateMachine:
    current_state = StateStart()
    current_text = ''
    current_type = 'None'
    start_index = 0
    index = 0
    end_index = 0
    input_text = ''

    def __init__(self, input_text):
        self.input_text = input_text

    def reset(self, new_index=0):
        self.start_index = new_index
        self.current_text = ''
        self.current_state = StateStart()

    def check(self):
        if type(self.current_state) is StateError:
            print('Parse error! Position: [' + str(self.start_index) + '...' + str(self.index) +
                  '], text value: [' + self.current_text + '], this data was skipped')
            self.index += 1
            self.reset(self.index)

        elif type(self.current_state) is StateEnd:
            # don't do +1 because use this symbol again
            print('Detected! Position: [' + str(self.start_index) + '...' + str(self.index - 1) +
                  '], text value: [' + self.current_text + '], type: ' + self.current_type)

            self.start_index = self.index
            self.current_text = ''
            self.current_state = StateStart()

        elif self.index == self.end_index - 1:
            # ending
            self.current_text += self.input_text[self.index]
            self.index += 1

            # check if last token is valid and ended
            if type(self.current_state) not in [StateStringEscapePrepare, StateStringEscapeIgnore, StateStringInput]:
                print('Last detected! Position: [' + str(self.start_index) + '...' + str(self.index) +
                      '], text value: [' + self.current_text + '], type: ' + self.current_type)

                self.current_state = StateEnd()
            else:
                print('Parse error! Position: [' + str(self.start_index) + '...' + str(self.index) +
                      '], text value: [' + self.current_text + '], this data was skipped')
                self.current_state = StateError()

        else:
            self.current_type = str(type(self.current_state))
            self.current_text += self.input_text[self.index]
            self.index += 1

        return

    def take(self):
        self.end_index = len(self.input_text)

        while self.index < len(self.input_text):
            self.current_state = self.current_state.get_next_state(self.input_text[self.index])
            self.check()


        return
