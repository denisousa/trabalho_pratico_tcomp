from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union, List
from AF import AF

class AFND(AF):
    def __init__(self,
                 states: List[str] = None,
                 alphabet: List[str] = None,
                 transition_function: List[Tuple[Tuple[str,str], str]] = None,
                 start_state: str = None,
                 accept_states: List[str] = None):
        
        super().__init__(states, alphabet, transition_function, start_state, accept_states)
        self.transition_function = transition_function
