from file_operations import GrammarLoader, AutomatonLoader
from convert import Convert
from test_input import g1

if __name__ == '__main__':
    try:
        grammar = GrammarLoader.load_from_file('./grammar.txt')
    except:
        grammar = g1

    AFND_1 = Convert.convert_GLUD_AFND(grammar)
    AFD_1 = Convert.convert_AFND_AFD(AFND_1)
    COMP_1 = AFD_1.apply_complement()
    REV_1 = AFD_1.apply_reverse()

    GrammarLoader.write_Grammar(grammar)
    AutomatonLoader.write_AF(AFND_1, 'AFN.txt', '#AFN - Fisrt Automaton')
    check, message = AFND_1.check_is_deterministic()
    print(message)
    AutomatonLoader.write_AF(AFD_1, 'AFD.txt', '#AFD - Deterministc Automaton')
    check, message = AFD_1.check_is_deterministic()
    print(message)
    AutomatonLoader.write_AF(COMP_1, 'COMP.txt', '#AFD - Complement')
    check, message = COMP_1.check_is_deterministic()
    print(message)
    AutomatonLoader.write_AF(REV_1, 'REV.txt', '#AFD - Reverse')
    check, message = REV_1.check_is_deterministic()
    print(message)

