from AF import AF
from global_variable import NULL_STATE


class CLI_Printer:
    @staticmethod
    def print_result(w: str, automaton: AF):
        result = 'Aceita'
        for i in range(len(w)):
            symbol = w[i]
            if i == 0:
                state = automaton.start_state

            t = [t for t in automaton.transition_function if [state, symbol] == t[0]]
            
            if not t:
                result = 'Rejeita'
                break

            if i == len(w) and state not in automaton.accept_states:
                result = 'Rejeita'

            state = t[0][1] # newt state

        complete_result = f'''
        Cadeia: {w}
        Resultado: {result}
        Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt
        '''
        print(complete_result)

    @staticmethod
    def print_word_steps(w: str, automaton: AF, valid: bool):
        result = 'Aceita'
        for i in range(len(w)):
            symbol = w[i]
            if i == 0:
                state = automaton.start_state

            destination = None
            for t in automaton.transition_function:
                if t[0][0] == set(NULL_STATE) or t[1] == set(NULL_STATE):
                    continue

                if [state, symbol] == t[0]:
                    destination = t[1]
                    break

            if not destination:
                result = 'Rejeita'
                break

            if i == len(w) - 1 and destination not in automaton.accept_states:
                result = 'Rejeita'

            state = t[1] # newt state

        complete_result = f'''Cadeia: {w}\nResultado: {result}'''
        print(complete_result)

        if (result == 'Aceita' and not valid) or (result == 'Rejeita' and valid):
            print('Automato ou análise está errada!') 
