#!/usr/bin/python
import codecs
import logging

from lex.state_lib import LibState
from lex.state_machine import StateMachine
from syn.parser import Parser


class Config:
    LOG_FORMAT = u'%(levelname)-8s [%(asctime)s] %(message)s'
    LOG_LEVEL = logging.NOTSET # lowest


def main():
    f = codecs.open('./data/input.txt', 'r', 'utf-8')

    sm = StateMachine()
    sm.set_data(f.read())
    sm.parse_data()
    # sm.show()

    pr = Parser(sm.get_tokens([LibState.TYPE_OK]))
    tree = pr.parse()
    pr.show_node(tree, 1)

    return

if __name__ == "__main__":
    logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
    main()
