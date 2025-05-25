from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List

class AF(ABC):
    def __init__(self, states: Set[str], alphabet: Set[str], start_state: str,
                 accept_states: Set[str]):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states

    @abstractmethod
    def transition(self, state: str, symbol: str):
        pass

    @abstractmethod
    def accepts(self, input_string: str) -> bool:
        pass
