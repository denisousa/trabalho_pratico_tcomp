from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union, Set
from AF import AF
from itertools import chain, combinations
from collections import deque
from state import State

EPSILON_SYMBOL = 'ε'


class AFND(AF):
    def __init__(self,
                 states: List[str] = [],
                 alphabet: Set[str] = [],
                 transition_function: List[Tuple[Tuple[str,str], str]] = [],
                 start_state: str = '',
                 accept_states: List[str] = []):
        
        super().__init__(states, alphabet, transition_function, start_state, accept_states)
        self.transition_function = transition_function

