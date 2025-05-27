from AFD import AFD
from GLUD import GLUD
from AFND import AFND
from itertools import chain, combinations
from collections import deque

def remove_unreachable_states(transitions, start_state):
    reachable = set()
    queue = deque([start_state])
    
    while queue:
        current = queue.popleft()
        if current in reachable:
            continue
        reachable.add(current)
        for [x, y], z in transitions:
            if x == current and z not in reachable:
                queue.append(z)

    return [[[x, y], z] for [[x, y], z] in transitions if x in reachable and z in reachable]


def all_subsets(s: str):
    chars = list(s)
    subs = list(chain.from_iterable(combinations(chars, r) for r in range(len(chars)+1)))
    return [''.join(sub) for sub in subs]

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

        
        return AFND(states=grammar.non_terminals,
             alphabet=grammar.terminals,
             transition_function=transition_function,
             start_state=grammar.start_symbol,
             accept_states=[final_state]) 
    
    @staticmethod
    def convert_AFND_AFD(automaton: AFND) -> AFD:
        states_without_q = [state.replace('q', '') for state in automaton.states]

        states_without_q_str = ''.join(states_without_q)
        all_states = all_subsets(states_without_q_str)[1:]
        all_states = [f'q{state}' for state in all_states]

        new_transition_fuction_list = []
        for collumn_state in all_states:
            collumn_state_unique_list = [f'q{s}' for s in collumn_state[1:]]
            
            if len(collumn_state_unique_list) == 1:
                for state in collumn_state_unique_list:
                    for symbol in automaton.alphabet:
                        current_cell = []
                        for original_state in automaton.transition_function:            
                            if [state, symbol] == original_state[0]:
                                current_cell.append([[state, symbol], original_state[1]])
                    
                        if len(current_cell) == 0:
                            continue

                        sorted_transition = sorted(list(set([int(i[1].replace('q','')) for i in current_cell])))
                        str_transition = [str(i) for i in sorted_transition]
                        new_state = 'q' + ''.join(str_transition)
                        new_trasition = [[collumn_state, symbol], new_state]
                        new_transition_fuction_list.append(new_trasition)
        
            elif len(collumn_state_unique_list) >= 1:
                for symbol in automaton.alphabet:
                    current_cell = []
                    for state in collumn_state_unique_list:
                        for original_state in automaton.transition_function:            
                            if [state, symbol] == original_state[0]:
                                current_cell.append(original_state)
                    
                    if len(current_cell) == 0:
                        continue

                    sorted_transition = sorted(list(set([int(i[1].replace('q','')) for i in current_cell])))
                    str_transition = [str(i) for i in sorted_transition]
                    new_state = 'q' + ''.join(str_transition)
                    new_trasition = [[collumn_state, symbol], new_state]
                    new_transition_fuction_list.append(new_trasition)

        new_transition_fuction_list = remove_unreachable_states(new_transition_fuction_list, 
                                                                automaton.start_state)

        states_set = {state[1] for state in new_transition_fuction_list}
        states_set.add(automaton.start_state)
        AFD_states = list(states_set)

        number_accept_state = automaton.accept_states[0][1]
        AFD_accept_states = [state for state in AFD_states if number_accept_state in state]

        return AFD(states=AFD_states,
        alphabet=automaton.alphabet,
        transition_function=new_transition_fuction_list,
        start_state=automaton.start_state,
        accept_states=AFD_accept_states)

