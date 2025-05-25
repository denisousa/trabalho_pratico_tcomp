from GLUD import GLUD
from AFND import AFND

class Convert:
    @staticmethod
    def convert_GLUD_AFND(grammar: GLUD) -> AFND:

        transition_function = []
        for production in grammar.productions:
            for state, chain in production.items():
                if chain[0] == 'ε' and len(chain) == 1:
                    transition_function.append([[state, chain[0]], 'F'])

                elif chain[0].islower() and len(chain) == 1: # Poso ter comente 1? Sim pq é GLUD
                    transition_function.append([[state, chain[0]], 'F'])

                elif chain[0].isupper() and len(chain) == 1: 
                    transition_function.append([[state, 'ε'], chain[1]])

                else:
                    transition_function.append([[state, chain[0]], chain[1]])

        
        return AFND(states=grammar.non_terminals,
             alphabet=grammar.terminals,
             transition_function=transition_function,
             start_state=grammar.start_symbol,
             accept_states='F') 