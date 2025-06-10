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
        Para cada produção da gramática, irei verficar:
        Se gera somente um símbolo vazio, adciiona uma transição para o estado final.
        Se gera somente um terminal, adciiona uma transição para o estado final.
        Se gera somente uma variável, adciiona uma transição com vazio para a variável gerada.
        Se gera variável e terminal, adciiona uma transição com o terminal para a variável gerada.
        """
        transition_function = []
        for production in grammar.productions:
            variable, chain = production
            if chain[0] == EPSILON_SYMBOL and len(chain) == 1:
                transition_function.append([[set(variable), EPSILON_SYMBOL], set(GRAMMAR_FINAL_STATE)])

            elif chain[0].islower() and len(chain) == 1:
                transition_function.append([[set(variable), chain[0]], set(GRAMMAR_FINAL_STATE)])

            elif chain[0].isupper() and len(chain) == 1: 
                transition_function.append([[set(variable), EPSILON_SYMBOL], set(chain[1])])

            else:
                transition_function.append([[set(variable), chain[0]], set(chain[1])])

        
        states = [*grammar.non_terminals, GRAMMAR_FINAL_STATE]
        return AF(states=[set(s) for s in states],
             alphabet=set([t for t in grammar.terminals]),
             transition_function=transition_function,
             start_state=set(grammar.start_symbol),
             accept_states=[set([GRAMMAR_FINAL_STATE])]) 
    
    def convert_AFND_AFD(afnd: AF) -> AF:
        """
        Essa função consiste em utilizar a função "epsilon_closure" para computar o fecho-ε de cada estado.
        Essa função também utiliza a função "transition" para computar o próximo estado.
        A cada iteração, irei adicionar os estados de destino a uma fila e adicionar os estados de destino a uma fila.
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
        Irei procurar pelas transições vazias que estão saindo do meu estado.
        Caso eu encontre uma transição vazia, irei chamar a função recursivamente.
        A ideia é unir todos os estados alcançãveis pelo estado atual usando vazio.
        """
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
        Componente - Cada estdo individual da minha nova transição

        Lógica:
        Para cada componente irei procurar na AFND uma transição correspondente com o símbolo.
        Isso é feito para criar um novo estado destino.
        O estado destino será a união dos estados da AFND para o componente e o símbolo que passo como parâmetro.
        Caso não exista esse estado destino, irei retornar o estado nulo.
        """
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

