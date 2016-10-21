#!/usr/bin/python
from lex.state_machine import StateMachine


def main():
    input_text = input('Input text to parse: ')
    StateMachine(input_text).take()

    return

if __name__ == "__main__":
    main()
