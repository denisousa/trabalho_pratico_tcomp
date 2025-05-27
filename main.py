from file_operations import GrammarLoader, AutomatonLoader
from cli_operation import CLI_Printer
from convert import Convert

if __name__ == '__main__':
    grammar = GrammarLoader.load_from_file('./grammar.txt')
    AFND_1 = Convert.convert_GLUD_AFND(grammar)
    AFD_1 = Convert.convert_AFND_AFD(AFND_1)
    COMP_1 = AFD_1.apply_complement()
    REV_1 = AFD_1.apply_reverse()

    AutomatonLoader.write_AFND(AFND_1, 'AFN.txt')
    AutomatonLoader.write_AFD(AFD_1, 'AFD.txt')
    AutomatonLoader.write_AFD(COMP_1, 'COMP.txt')
    AutomatonLoader.write_AFD(REV_1, 'REV.txt')

    CLI_Printer.print_result('aabb', AFD_1)
