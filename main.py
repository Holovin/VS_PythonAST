#!/usr/bin/python
from state_common import StateStart, StateEnd, StateError


def main():
    input_text = input('Input text to parse: ')

    current_state = StateStart()
    current_text = ''
    current_type = 'None'
    start_index = 0
    index = 0

    while index < len(input_text):
        current_state = current_state.get_next_state(input_text[index])

        if type(current_state) is StateError:
            print('Parse error! Position: [' + str(start_index) + '...' + str(index - 1) + '], text value: [' +
                  current_text + '], this data was skipped')
            start_index = index
            current_text = ''
            current_state = StateStart()

        elif type(current_state) is StateEnd:
            print('Detected! Position: [' + str(start_index) + '...' + str(index - 1) + '], text value: [' +
                  current_text + '], type: ' + current_type)

            start_index = index
            current_text = ''
            current_state = StateStart()

        else:
            #deubg: print(input_text[index], current_state)
            current_text += input_text[index]
            current_type = str(type(current_state))
            index += 1

    print('Detected! Position: [' + str(start_index) + '...' + str(index - 1) + '], text value: [' + current_text +
          '], type: ' + current_type)

    return


if __name__ == "__main__":
    main()
