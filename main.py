from file_operations import GrammarLoader, AutomatonLoader
from cli_operation import CLI_Printer
from AFND import AFND
from convert import Convert

if __name__ == '__main__':
    grammar = GrammarLoader.load_from_file('./grammar.txt')
    AFND_1 = Convert.convert_GLUD_AFND(grammar)

    AFND_1 = AFND(states=[set('S'), set('A'), set('F')],
                  alphabet=['0','1'],
                  transition_function=[[[set('S'),'0'],set('S')], [[set('S'),'1'],set('S')], [[set('S'),'1'],set('A')], [[set('A'), '0'], set('F')], [[set('A'),'ε'], set('F')]],
                  start_state=set('S'),
                  accept_states=[set('F')],
    )

    # AFND_1 = AFND(
    #     states=['S', 'A', 'F'],
    #     alphabet=['0', '1'],
    #     transition_function=[
    #         [['S', '0'], 'S'],
    #         [['S', '1'], 'S'],
    #         [['S', '1'], 'A'],
    #         [['A', '0'], 'F'],
    #         [['A', 'ε'], 'F']
    #     ],
    #     start_state='S',
    #     accept_states=['F'],
    # )

    AFD_1 = Convert.convert_AFND_AFD(AFND_1)
    # AFD_1 = AFND_1.convert_to_AFD()
    COMP_1 = AFD_1.apply_complement()
    REV_1 = AFD_1.apply_reverse()

    AutomatonLoader.write_AFND(AFND_1, 'AFN.txt')
    AutomatonLoader.write_AFD(AFD_1, 'AFD.txt')
    AutomatonLoader.write_AFD(COMP_1, 'COMP.txt')
    AutomatonLoader.write_AFD(REV_1, 'REV.txt')

    CLI_Printer.print_result('aabb', AFD_1)
