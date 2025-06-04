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

        
        grammar.non_terminals.append(final_state)
        return AFND(states=grammar.non_terminals,
             alphabet=grammar.terminals,
             transition_function=transition_function,
             start_state=grammar.start_symbol,
             accept_states=[final_state]) 
    
    @staticmethod
    def get_all_transitions_from_state(state, transitions):
        return [t for t in transitions if t[0][0] == set(state)]

    @staticmethod
    def convert_AFND_AFD(automaton: AFND) -> AFD:
        final_transition = []
        states_stack = [automaton.start_state]

        while len(states_stack) != 0:
            current_state = states_stack.pop()
            transistions = Convert.get_all_transitions_from_state(current_state, automaton.transition_function)

            for symbol in automaton.alphabet:
                trasition_match_list = [t for t in transistions if symbol == t[0][1]]

                for transition_match in trasition_match_list:
                    test, new_state = check_neighbor_state_has_void(current_state, automaton)
                    if test:
                        states_stack.append(new_state)

                    test, new_state = check_the_same_symbol_in_state(current_state, transition_match)
                    if test:
                        print('problem 2')

                    test, new_state = check_void_in_state(transition_match, automaton)
                    if test:
                        print('problem 3')
                
                    final_transition.append()

        
        # print(transistions)

        # [states_stack.append(t) for t in transistions]
        # [new_transition_function.append(t) for t in transistions]

        # while len(states_stack) != 0:
        #     current_transition = states_stack.pop()
        #     test, new_state = check_neighbor_state_has_void(automaton.start_state, automaton)
        #     if test:
        #         states_stack.append(new_state)

        #     if check_the_same_symbol_in_state(current_transition):
        #         print('problem 2')

        #     if check_void_in_state(current_transition, automaton):
        #         print('problem 3')
            


    @staticmethod
    def OLD_convert_AFND_AFD(automaton: AFND) -> AFD:
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


def check_void_in_state(transition):
    if transition[0][1] == 'ε':
        return True, set([transition[0][0], transition[1]])

    return False, None

def check_the_same_symbol_in_state(transition, automaton: AFD):
    all_transitions_from_current_state = Convert.get_all_transitions_from_state(transition[0][0], automaton.transition_function)
    
    symbols_list = [t[0][1] for t in all_transitions_from_current_state]
    repeat_symbol = len(symbols_list) != len(set(symbols_list))

    if repeat_symbol:
        return True, 
    
    return False, None

def check_neighbor_state_has_void(current_state: str, automaton: AFD):
    all_transitions_from_start = Convert.get_all_transitions_from_state(current_state, automaton.transition_function)

    neighbors_states_from_start = set()
    [neighbors_states_from_start.update(t[1]) for t in all_transitions_from_start]
    
    for neighbor_1 in neighbors_states_from_start:
        if set(neighbor_1) == current_state:
            continue

        all_trasitinos_from_neighbors = Convert.get_all_transitions_from_state(neighbor_1, automaton.transition_function)

        for transitions_neighbor in all_trasitinos_from_neighbors:
            if transitions_neighbor[0][1] == 'ε':
                new_state = set([current_state, transitions_neighbor[0][0], transitions_neighbor[1]])
                return True, new_state 
            
    return False



def convert_to_deterministic(afnd: AFND) -> AFD:
    afd = AFD(afnd)
    afd.alphabet = afnd.alphabet.copy()

    afd.start = afnd.epsilon_closure(afnd.start)
    afd.states.add(afd.start)

    queue = deque()
    queue.append(afd.start)

    while queue:
        current_state = queue.popleft()

        for component in current_state.components:
            if component in afnd.final_states:
                afd.final_states.add(current_state)

        for symbol in afnd.alphabet:
            destination = afnd.transition(current_state, symbol)
            destination = afnd.epsilon_closure(destination)

            afd.transitions.add((current_state, symbol, destination))

            if not afd.contain_state(destination):
                queue.append(destination)
                afd.states.add(destination)

    afd.rename_states()
    return afd

def epsilon_closure(afnd, state):
    closure = state.copy()
    for component in state.components:
        for origin, symbol, destination in afnd.transitions:
            if origin == component and symbol == EPSILON_SYMBOL:
                closure += afnd.epsilon_closure(State(destination))
    return closure

def transition(afnd, origin, symbol):
    destination = State()

    for component in origin.components:
        for (o, sym, d) in afnd.transitions:
            if o == component and sym == symbol:
                destination += State(d)

    if not destination.components:
        return State(VOID_STATE)

    return destination

def to_string(afnd):
    return (
        f"Q = {afnd.states}\n"
        f"Sigma = {afnd.alphabet}\n"
        f"delta = {afnd.transitions}\n"
        f"q0 = {afnd.start}\n"
        f"F = {afnd.final_states}\n"
    )
