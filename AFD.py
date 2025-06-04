from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
from AF import AF

class AFD(AF):
    def __init__(self, states: List[str]=[],
                 alphabet: List[str]=[],
                 transition_function: List[Tuple[Tuple[str, str], str]]=[],
                 start_state: str='',
                 accept_states: List[str]=[]):
        
        super().__init__(states, alphabet, transition_function, start_state, accept_states)