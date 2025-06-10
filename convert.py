from AF import AF
from GLUD import GLUD
from collections import deque
from global_variable import EPSILON_SYMBOL, GRAMMAR_FINAL_STATE, NULL_STATE
from typing import Set


class Convert:
    @staticmethod
    def unique_item_list(list_item: list) -> list:
        """
        Remove itens duplicados de uma lista mantendo a ordem original.
        Args:
            list_item: Lista que terá seus itens duplicados removidos
        Returns:
            Lista sem itens duplicados
        """
        new_list = []
        for item in list_item:
            if item in new_list:
                continue
            
            new_list.append(item)

        return new_list

    @staticmethod
    def convert_GLUD_AFND(grammar: GLUD) -> AF:
        """
        Converte uma Gramática Linear Unitária à Direita (GLUD) em um Autômato Finito Não Determinístico (AFND).
        Args:
            grammar: Gramática GLUD a ser convertida
        Returns:
            AFND equivalente à gramática
        """
        transition_function = []
        for production in grammar.productions:
            state, chain = production
            if chain[0] == 'ε' and len(chain) == 1:
                transition_function.append([[set(state), chain[0]], set(GRAMMAR_FINAL_STATE)])

            elif not chain[0] and len(chain) == 1: # Poso ter comente 1? Sim pq é GLUD
                transition_function.append([[set(state), chain[0]], set(GRAMMAR_FINAL_STATE)])

            elif chain[0] and len(chain) == 1: 
                transition_function.append([[set(state), chain[0]], set(GRAMMAR_FINAL_STATE)])

            else:
                transition_function.append([[set(state), chain[0]], set(chain[1])])

        
        states = [*grammar.non_terminals, GRAMMAR_FINAL_STATE]
        return AF(states=[set(s) for s in states],
             alphabet=set([t for t in grammar.terminals]),
             transition_function=transition_function,
             start_state=set(grammar.start_symbol),
             accept_states=[set([GRAMMAR_FINAL_STATE])]) 
    
    def convert_AFND_AFD(afnd: AF) -> AF:
        """
        Converte um Autômato Finito Não Determinístico (AFND) em um Autômato Finito Determinístico (AFD).
        Args:
            afnd: AFND a ser convertido
        Returns:
            AFD equivalente ao AFND
        """
        afd = AF()

        afd.start_state = Convert.epsilon_closure(afnd, set(afnd.start_state))
        afd.alphabet = afnd.alphabet
        afd.states = [afd.start_state]

        queue = deque([afd.start_state])

        while queue:

            current_state = queue.popleft()

            for component in current_state:
                component = set(component)
                if component in afnd.accept_states:
                    afd.accept_states.append(current_state)

            for symbol in afnd.alphabet:
                destination = Convert.transition(afnd, current_state, symbol)
                destination = Convert.epsilon_closure(afnd, destination)

                afd.transition_function.append([[current_state, symbol], destination])

                if destination not in afd.states:
                    queue.append(destination)
                    afd.states.append(destination)

        afd.transition_function.sort(key=lambda item: len(item[0][0]))
        afd.transition_function = Convert.unique_item_list(afd.transition_function)
        afd.accept_states = Convert.unique_item_list(afd.accept_states)

        new_transitions = []
        for t in afd.transition_function:
            if t[0][0] in afd.states:
                  new_transitions.append(t)

        afd.transition_function = new_transitions
        return afd

    def epsilon_closure(afnd: AF, state: Set[str]) -> Set[str]:
        """
        Calcula o fecho-ε de um estado no AFND.
        O fecho-ε é o conjunto de todos os estados alcançáveis a partir do estado atual
        usando apenas transições ε.
        Args:
            afnd: AFND onde o fecho-ε será calculado
            state: Estado inicial para calcular o fecho-ε
        Returns:
            Conjunto de estados alcançáveis via transições ε
        """
        if not isinstance(state, set):
            state = set([state])
        closure = state.copy()

        for component in state:
            component = set([component])
            for current_origin, destination in afnd.transition_function:
                origin, symbol = current_origin
                if origin == component and symbol == EPSILON_SYMBOL:
                    closure.update(Convert.epsilon_closure(afnd, destination))

        return closure

    def transition(afnd: AF, origin: Set[str], symbol: str) -> Set[str]:
        """
        Calcula o conjunto de estados de destino a partir de um estado de origem
        e um símbolo de entrada no AFND.
        Args:
            afnd: AFND onde a transição será calculada
            origin: Estado de origem
            symbol: Símbolo de entrada
        Returns:
            Conjunto de estados de destino (ou {NULL_STATE} se não houver transição)
        """
        if not isinstance(origin, set):
            origin = set(origin)

        destination = set()

        for component in origin:
            component = set([component])
            for (trans_origin, trans_dest) in afnd.transition_function:
                trans_origin, trans_symbol = trans_origin 
                if trans_origin == component and trans_symbol == symbol:
                    destination.update(set(trans_dest))

        if not destination:
            return set(NULL_STATE)

        return destination


