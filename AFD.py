from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
from AF import AF

class AFD(AF):
    def __init__(self, states: Set[str],
                 alphabet: Set[str],
                 transition_function: List[Tuple[Tuple[str, str], str]],
                 start_state: str,
                 accept_states: Set[str]):
        
        super().__init__(states, alphabet, transition_function, start_state, accept_states)

    def apply_complement(self):
        new_accept_states = [state for state in self.states if state not in self.accept_states]

        return AFD(states=self.states,
        alphabet=self.alphabet,
        transition_function=self.transition_function,
        start_state=self.start_state,
        accept_states=new_accept_states)
    
    def apply_reverse(self):
        # Todos os estados finais deixarão de ser finais
        # Todos os estados finais devem ser ligados por ε para um novo F
        # F é o estado inicial | initial state é o estado final
        # inverter todas as funções de transição

        final_state = f'q{len(self.states)}'
        automaton_rev = AFD(states=self.states,
        alphabet=self.alphabet,
        transition_function=self.transition_function,
        start_state=final_state,
        accept_states=self.accept_states)

        for state in automaton_rev.accept_states:
            automaton_rev.transition_function.append([[state,'ε'],final_state])
        
        automaton_rev.accept_states = [final_state]

        new_transitions = []
        for t in automaton_rev.transition_function:
            new_transitions.append([[t[1],t[0][1]],t[0][0]])

        automaton_rev.transition_function = new_transitions
        return automaton_rev