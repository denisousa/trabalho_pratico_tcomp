from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union, List
from AF import AF

class AFND(AF):
    def __init__(self, states: List[str],
                 alphabet: List[str],
                 transition_function: Tuple[Tuple[str,str], str],
                 start_state: str,
                 accept_states: List[str]):
        super().__init__(states, alphabet, start_state, accept_states)
        self.transition_function = transition_function

    def transition(self, state: str, symbol: str) -> List[str]:
        return self.transition_function.get((state, symbol), [])

    def accepts(self, input_string: str) -> bool:
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = []
            for state in current_states:
                next_states.update(self.transition(state, symbol))
            current_states = next_states
            if not current_states:
                return False
        return bool(current_states & self.accept_states)
