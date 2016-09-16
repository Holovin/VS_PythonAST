from state_chars import LibState
from state_common import StateStart, StateError, StateEnd, _StateReturn


class StateMachine:
    current_state = StateStart()
    current_text = ''
    current_type = 'None'
    start_index = 0
    index = 0
    input_text = ''

    def __init__(self, input_text):
        self.input_text = input_text + LibState.CHAR_ENDSYMBOL

    def reset(self, new_index=0):
        self.start_index = new_index
        self.current_text = ''
        self.current_state = StateStart()

    def check(self):
        if type(self.current_state) is StateError:
            print('Parse error! Position: [' + str(self.start_index) + '...' + str(self.index - 1) +
                  '], text value: [' + self.current_text + '], this data was skipped')
            self.reset(self.index)

        elif type(self.current_state) is StateEnd:
            print('Detected! Position: [' + str(self.start_index) + '...' + str(self.index - 1) +
                  '], text value: [' + self.current_text + '], type: ' + self.current_type)

            self.start_index = self.index
            self.current_text = ''
            self.current_state = StateStart()

        else:
            self.current_text += self.input_text[self.index]
            self.current_type = str(type(self.current_state))
            self.index += 1

    def take(self):
        while self.index < len(self.input_text):
            self.current_state = self.current_state.get_next_state(self.input_text[self.index])
            self.check()

        else:
            if type(self.current_type) is not _StateReturn and len(self.current_text[:-1]) > 1:
                print('Parse error! Position: [' + str(self.start_index) + '...' + str(self.index - 1) +
                      '], text value: [' + self.current_text[:-1] + '], this data was skipped' + self.current_type)

        return