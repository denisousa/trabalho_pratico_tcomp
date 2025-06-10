from global_variable import GRAMMAR_FINAL_STATE, REVERSE_FINAL_STATE, EPSILON_SYMBOL, NULL_STATE
from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
import copy

class AF(ABC):
    def __init__(self,
                 states: List[Tuple[Set[str], Set[str]]] = [],
                 alphabet: Set[str] = set(),
                 transition_function: List[Tuple[Tuple[Set[str], str], Set[str]]] = [],
                 start_state: Set[str] = set(),
                 accept_states: List[Set[str]] = []) -> None:
    
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transition_function = transition_function

    def check_is_deterministic(self) -> tuple[bool, str]:
        # Check for epsilon transitions
        for transition in self.transition_function:
            if transition[0][1] == EPSILON_SYMBOL:
                return False, "Epsilon transitions are not allowed"
        
        # Check for repeated transitions from same state with same input
        seen_transitions = set()
        for transition in self.transition_function:
            state_input = (frozenset(transition[0][0]), transition[0][1])
            if state_input in seen_transitions:
                return False, "Repeated transitions from same state with same input are not allowed"
            seen_transitions.add(state_input)
        
        # Check if each state has exactly one transition for each symbol in alphabet
        for state in self.states:
            state_transitions = []
            for transition in self.transition_function:
                if transition[0][0] == state:  # Check if transition is from current state
                    state_transitions.append(transition[0][1])
            
            if len(state_transitions) != len(self.alphabet):
                return False, f"State {state} does not have exactly one transition for each symbol in alphabet"
        
        return True, "Deterministic Automaton"


    def apply_complement(self) -> 'AF':
        new_accept_states = [state for state in self.states if state not in self.accept_states]

        return AF(states=self.states,
        alphabet=self.alphabet,
        transition_function=self.transition_function,
        start_state=self.start_state,
        accept_states=new_accept_states)
    
    def apply_reverse(self) -> 'AF':
        new_state = set([REVERSE_FINAL_STATE])
        automaton_rev = copy.deepcopy(self)

        # Add New State
        automaton_rev.states.append(new_state)
        
        # Invert transitions
        new_transitions = []
        for t in automaton_rev.transition_function:
            if t[0][0] == set(NULL_STATE) or t[1] == set(NULL_STATE):
                continue
            new_transitions.append([[t[1],t[0][1]],t[0][0]])
        automaton_rev.transition_function = new_transitions

        # Connect New 'ε' to accept 
        for state in automaton_rev.accept_states:
            state = set(state)
            automaton_rev.transition_function.append([[new_state,'ε'], state])

        automaton_rev.accept_states = [automaton_rev.start_state] 
        automaton_rev.start_state = new_state

        automaton_rev.states.remove(set(NULL_STATE))
        
        return automaton_rev