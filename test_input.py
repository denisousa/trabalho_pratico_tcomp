from GLUD import GLUD
from global_variable import EPSILON_STRING
from convert import Convert
from cli_operation import CLI_Printer
from file_operations import AutomatonLoader

def check_word(word: str, grammar: GLUD, valid: bool):
    print()
    afnd = Convert.convert_GLUD_AFND(grammar)
    afd = Convert.convert_AFND_AFD(afnd)
    rev = afd.apply_reverse()
    rev_afd = Convert.convert_AFND_AFD(rev)

    CLI_Printer.print_word_steps(word, afd, valid)
    CLI_Printer.print_word_steps(word[::-1], rev_afd, valid)

def print_conversions(grammar: GLUD):
    afnd = Convert.convert_GLUD_AFND(grammar)
    afd = Convert.convert_AFND_AFD(afnd)
    rev = afd.apply_reverse()
    rev_afd = Convert.convert_AFND_AFD(rev)
    comp = afd.apply_complement()

    print('AFND')
    AutomatonLoader.write_AF(afnd)
    print('AFD')
    AutomatonLoader.write_AF(afd)
    print('REV')
    AutomatonLoader.write_AF(rev)
    print('REV -> AFD')
    AutomatonLoader.write_AF(rev_afd)
    print('COMP')
    AutomatonLoader.write_AF(comp)

g1 = GLUD(non_terminals=['S', 'A'],
         terminals=['a', 'b'],
         start_symbol='S',
         productions=[
            ('S', ['a', 'A']),
            ('S', EPSILON_STRING), 
            ('A', ['a', 'A']),
            ('A', ['b'])
        ])


if __name__ in '__main__':
    print_conversions(g1)
    check_word("", g1, True)
    check_word("a", g1, False)
    check_word("b", g1, False)
    check_word("ab", g1, True)
    check_word("ba", g1, False)
    check_word("aab", g1, True)
    check_word("aabb", g1, False)
    check_word("aaaaaaaab", g1, True)
    check_word("aaaaaaaaaabb", g1, False)
    check_word("aaaaaabaaab", g1, False)

