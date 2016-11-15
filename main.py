#!/usr/bin/python
import codecs
import logging

from lex.state_machine import StateMachine


class Config:
    LOG_FORMAT = u'%(levelname)-8s [%(asctime)s] %(message)s'
    LOG_LEVEL = logging.NOTSET # lowest


def main():
    f = codecs.open('./data/input.txt', 'r', 'utf-8')

    sm = StateMachine()
    sm.set_data(f.read())
    sm.parse_data()
    sm.show()

    return

if __name__ == "__main__":
    logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
    main()
