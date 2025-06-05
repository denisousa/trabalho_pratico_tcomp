from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
from AF import AF
import copy
from AFND import AFND

class AFD(AF):
    def __init__(self, states: List[str]=[],
                 alphabet: List[str]=[],
                 transition_function: List[Tuple[Tuple[str, str], str]]=[],
                 start_state: str='',
                 accept_states: List[str]=[]):
        
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

        new_state = set(['$'])
        automaton_rev = copy.deepcopy(self)

        # Add New State
        automaton_rev.states.append(new_state)
        # automaton_rev.states = [s for s in automaton_rev.states]
        
        # Connect New 'ε' to accept 
        for state in automaton_rev.accept_states:
            state = set(state)
            automaton_rev.transition_function.append([[state,'ε'], new_state])

        # New Accept State
        automaton_rev.accept_states = automaton_rev.start_state

        # New Start
        automaton_rev.start_state = new_state
        
        # Remove dead state
        automaton_rev.states.remove(set('@'))
        
        # Invert transitions
        new_transitions = []
        for t in automaton_rev.transition_function:
            if t[0][0] == set("@") or t[1] == set("@"):
                continue
            new_transitions.append([[t[1],t[0][1]],t[0][0]])

        return automaton_rev