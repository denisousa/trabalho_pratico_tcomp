from GLUD import GLUD
from global_variable import EPSILON_STRING
from convert import Convert
from cli_operation import CLI_Printer
from file_operations import AutomatonLoader

def check_word(word: str, grammar: GLUD, valid: bool):
    print()
    afnd = Convert.convert_GLUD_AFND(grammar)
    afd = Convert.convert_AFND_AFD(afnd)

    CLI_Printer.print_word_steps(word, afd, valid)

    rev_afd = afd.apply_reverse()
    CLI_Printer.print_word_steps(word[::-1], rev_afd, valid)


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



# check_word('aa', g, True)

# g.non_terminals = {'S', 'C'}
# g.terminals = {'a', 'b', 'c'}
# g.start_symbol = 'S'
# g.productions = [
#     ('S', ['a', 'A']),
#     ('S', EPSILON_STRING),   # ε-produção
#     ('A', ['a', 'A']),
#     ('A', ['b'])
# ]



# COMP_1 = AFD_1.apply_complement()
# REV_1 = AFD_1.apply_reverse()



# Test_Input{
#     {"", true},
#     {"a", false},
#     {"b", false},
#     {"ab", true},
#     {"ba", false},
#     {"aab", true},
#     {"aabb", false},
#     {"aaaaaaaab", true},
#     {"aaaaaaaaaabb", false},
#     {"aaaaaabaaab", false},
# }},

# Grammar_Test{// Accept strings with any number of 'ab' repetitions
#                 GLUD(
#                     {'S', 'A'}, // Variables
#                     {'a', 'b'}, // Terminals
#                     {           // Productions
#                     {'S', {"aA", EPSILON_STRING}},
#                     {'A', {"bS"}}},
#                     'S' // Start symbol
#                     ),
#                 Test_Input{
#                     {"", true},
#                     {"a", false},
#                     {"b", false},
#                     {"ab", true},
#                     {"ba", false},
#                     {"aab", false},
#                     {"aabb", false},
#                     {"aaaaaaaab", false},
#                     {"aaaaaaaaaabb", false},
#                     {"aaaaaabaaab", false},
#                     {"abab", true},
#                     {"ababababab", true},
#                     {"abababaabab", false},
#                     {"abababbabab", false},
#                     {"ababababa", false},
#                     {"bababab", false},
#                 }},

# Grammar_Test{// Accept strings with any number of 'a' followed by only one 'b'
#                 GLUD(
#                     {'S', 'A'},
#                     {'a', 'b'},
#                     {{'S', {"aS", "b"}}},
#                     'S'),
#                 Test_Input{
#                     {"", false},
#                     {"b", true},
#                     {"a", false},
#                     {"ab", true},
#                     {"aab", true},
#                     {"aaab", true},
#                     {"ba", false},
#                     {"bbb", false},
#                     {"aaabb", false},
#                 }},