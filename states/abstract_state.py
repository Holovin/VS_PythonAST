from abc import ABCMeta, abstractmethod


class AbstractState(metaclass=ABCMeta):

    @abstractmethod
    def get_next_state(self, char):
        pass

    @abstractmethod
    def is_final_state(self):
        return False
