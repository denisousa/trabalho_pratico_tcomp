from AFD import AFD
from GLUD import GLUD
from AFND import AFND
from itertools import chain, combinations
from collections import deque
from state import State
EPSILON_SYMBOL = 'ε'


class Convert:
    @staticmethod
    def convert_GLUD_AFND(grammar: GLUD) -> AFND:

        transition_function = []
        final_state = f'q{len(grammar.non_terminals)}'
        for production in grammar.productions:
            state, chain = production
            if chain[0] == 'ε' and len(chain) == 1:
                transition_function.append([[state, chain[0]], final_state])

            elif not chain[0].startswith('q') and len(chain) == 1: # Poso ter comente 1? Sim pq é GLUD
                transition_function.append([[state, chain[0]], final_state])

            elif chain[0].startswith('q') and len(chain) == 1: 
                transition_function.append([[state, 'ε'], chain[1]])

            else:
                transition_function.append([[state, chain[0]], chain[1]])

        
        grammar.non_terminals.append(final_state)
        return AFND(states=grammar.non_terminals,
             alphabet=grammar.terminals,
             transition_function=transition_function,
             start_state=grammar.start_symbol,
             accept_states=[final_state]) 
    
    def convert_AFND_AFD(afnd):
        afd = AFD()

        afd.start_state = Convert.epsilon_closure(afnd, State(afnd.start_state))
        afd.alphabet = afnd.alphabet
        afd.states = [afd.start_state]

        queue = deque([afd.start_state])

        while queue:
            current_state = queue.popleft()

            for component in current_state.components:
                if component in afnd.accept_states:
                    afd.accept_states.append(State(current_state))

            for symbol in afnd.alphabet:
                destination = Convert.transition(afnd, current_state, symbol)
                destination = Convert.epsilon_closure(afnd, destination)

                afd.transition_function.append([[current_state, symbol], destination])

                if destination not in afd.states:
                    queue.append(destination)
                    afd.states.append(destination)

        return afd

    @staticmethod
    def epsilon_closure(afnd: AFND, state):
        '''
        Verifico se em algum momento meu estado que estou analisando possui EPLSON
        Se sim, vou pegar todas os todos estados que possuem EPLSON em sequência
        Vou Colocar em uma lista todos os estados
        '''
        if not isinstance(state, State):
            state = State(state)
        closure = state.copy()

        for component in state.components:
            for current_origin, destination in afnd.transition_function:
                origin, symbol = current_origin
                if origin == component and symbol == EPSILON_SYMBOL:
                    closure += Convert.epsilon_closure(afnd, destination)

        return closure

    @staticmethod
    def transition(afnd, origin, symbol):
        '''
        Meu estado atutal lendo symbol, vai para onde?
        Se não for para lugar algum, deve ir para VOID
        Retorna para one vai
        '''
        if not isinstance(origin, State):
            origin = State(origin)

        destination = State([])

        for component in origin.components:
            for (trans_origin, trans_dest) in afnd.transition_function:
                trans_origin, trans_symbol = trans_origin 
                if trans_origin == component and trans_symbol == symbol:
                    destination += State(trans_dest)

        if not destination:
            return State("VOID")

        return destination

    def to_string(afnd):
        return (
            f"Q = {afnd.states}\n"
            f"Sigma = {afnd.alphabet}\n"
            f"delta = {Convert.transitions}\n"
            f"q0 = {afnd.start_state}\n"
            f"F = {afnd.accept_states}\n"
        )