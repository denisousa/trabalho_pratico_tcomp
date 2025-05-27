from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List

class AF(ABC):
    def __init__(self,
                 states: Set[str],
                 alphabet: Set[str],
                 transition_function: List[Tuple[str, List[str]]],
                 start_state: str,
                 accept_states: Set[str]):
    
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transition_function = transition_function
