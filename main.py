#!/usr/bin/python
import codecs


from lex.state_machine import StateMachine


def main():
    f = codecs.open('./data/input.txt', 'r', 'utf-8')

    sm = StateMachine()
    sm.set_data(f.read())
    sm.parse_data()
    sm.show()

    return

if __name__ == "__main__":
    main()
