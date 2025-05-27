from AFD import AFD

class CLI_Printer:
    @staticmethod
    def print_result(w: str, automaton: AFD):
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
