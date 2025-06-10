from global_variable import REVERSE_FINAL_STATE, EPSILON_SYMBOL, NULL_STATE
from abc import ABC
from typing import Set, Tuple, List
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
        # Verifica transições epsilon
        for transition in self.transition_function:
            if transition[0][1] == EPSILON_SYMBOL:
                return False, "Transições epsilon não são permitidas"
        
        # Verifica transições repetidas do mesmo estado com a mesma entrada
        seen_transitions = set()
        for transition in self.transition_function:
            state_input = (frozenset(transition[0][0]), transition[0][1])
            if state_input in seen_transitions:
                return False, "Transições repetidas do mesmo estado com a mesma entrada não são permitidas"
            seen_transitions.add(state_input)
        
        # Verifica se cada estado tem exatamente uma transição para cada símbolo no alfabeto
        for state in self.states:
            state_transitions = []
            for transition in self.transition_function:
                if transition[0][0] == state:  # Verifica se a transição é do estado atual
                    state_transitions.append(transition[0][1])
            
            if len(state_transitions) != len(self.alphabet):
                return False, f"Estado {state} não tem exatamente uma transição para cada símbolo no alfabeto"
        
        return True, "Autômato Determinístico"


    def apply_complement(self) -> 'AF':
        check, message = self.check_is_deterministic()
        if not check:
            raise ValueError(message)
        
        new_accept_states = [state for state in self.states if state not in self.accept_states]

        return AF(states=self.states,
        alphabet=self.alphabet,
        transition_function=self.transition_function,
        start_state=self.start_state,
        accept_states=new_accept_states)
    
    def apply_reverse(self) -> 'AF':
        check, message = self.check_is_deterministic()
        if not check:
            raise ValueError(message)
        
        new_state = set([REVERSE_FINAL_STATE])
        automaton_rev = copy.deepcopy(self)

        # Adiciona Novo Estado
        automaton_rev.states.append(new_state)
        
        # Inverte transições
        new_transitions = []
        for t in automaton_rev.transition_function:
            if t[0][0] == set(NULL_STATE) or t[1] == set(NULL_STATE):
                continue
            new_transitions.append([[t[1],t[0][1]],t[0][0]])
        automaton_rev.transition_function = new_transitions

        # Conecta Novo 'ε' aos estados de aceitação
        for state in automaton_rev.accept_states:
            state = set(state)
            automaton_rev.transition_function.append([[new_state,'ε'], state])

        # Estados de aceitação são o estado inicial
        automaton_rev.accept_states = [automaton_rev.start_state]

        # Estado inicial é o novo estado
        automaton_rev.start_state = new_state

        # Remove o estado nulo
        automaton_rev.states.remove(set(NULL_STATE))
        
        return automaton_rev