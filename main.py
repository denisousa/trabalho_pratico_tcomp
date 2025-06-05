from file_operations import GrammarLoader, AutomatonLoader
from cli_operation import CLI_Printer
from AFND import AFND
from convert import Convert

if __name__ == '__main__':
    try:
        grammar = GrammarLoader.load_from_file('./grammar.txt')
    except:
        AFND_1 = AFND(states=[set('S'), set('A'), set('F')],
                    alphabet=set(['0','1']),
                    transition_function=[[[set('S'),'0'],set('S')], [[set('S'),'1'],set('S')], [[set('S'),'1'],set('A')], [[set('A'), '0'], set('F')], [[set('A'),'ε'], set('F')]],
                    start_state=set('S'),
                    accept_states=[set('F')],
        )

    AFND_1 = Convert.convert_GLUD_AFND(grammar)
    AFD_1 = Convert.convert_AFND_AFD(AFND_1)
    COMP_1 = AFD_1.apply_complement()
    REV_1 = AFD_1.apply_reverse()

    AutomatonLoader.write_AF(AFND_1, 'AFN.txt', '#AFN - Fisrt Automaton')
    AutomatonLoader.write_AF(AFD_1, 'AFD.txt', '#AFD - Deterministc Automaton')
    AutomatonLoader.write_AF(COMP_1, 'COMP.txt', '#AFD - Complement')
    AutomatonLoader.write_AF(REV_1, 'REV.txt', '#AFD - Reverse')

    

    # CLI_Printer.print_result('aabb', AFD_1)

    # verificar palavras de aceitação
    # 
