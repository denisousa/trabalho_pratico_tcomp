from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
from AF import AF

class AFD(AF):
    def __init__(self, states: Set[str], alphabet: Set[str], start_state: str,
                 accept_states: Set[str], transition_function: Dict[Tuple[str, str], str]):
        super().__init__(states, alphabet, start_state, accept_states)
        self.transition_function = transition_function

    def transition(self, state: str, symbol: str) -> str:
        return self.transition_function.get((state, symbol))

    def accepts(self, input_string: str) -> bool:
        current_state = self.start_state
        for symbol in input_string:
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False
        return current_state in self.accept_states
