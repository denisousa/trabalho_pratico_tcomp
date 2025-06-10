from GLUD import GLUD
from global_variable import EPSILON_SYMBOL
from convert import Convert
from cli_operation import CLI_Printer
from file_operations import AutomatonLoader, GrammarLoader
from AF import AF
from global_variable import GRAMMAR_FINAL_STATE


def check_word(word: str, grammar: GLUD, valid: bool):
    print()
    if grammar:
        afnd = Convert.convert_GLUD_AFND(grammar)
    
    afd = Convert.convert_AFND_AFD(afnd)

    CLI_Printer.print_word_steps(word, afd, valid)


def print_grammar_conversions(grammar: GLUD):
    afnd = Convert.convert_GLUD_AFND(grammar)
    afd = Convert.convert_AFND_AFD(afnd)
    rev = afd.apply_reverse()
    comp = afd.apply_complement()

    print("Grammar")
    GrammarLoader.write_Grammar(grammar)
    print("AFND")
    AutomatonLoader.write_AF(afnd)
    print("AFD")
    AutomatonLoader.write_AF(afd)
    print("REV")
    AutomatonLoader.write_AF(rev)
    print("COMP")
    AutomatonLoader.write_AF(comp)

g1 = GLUD(
    non_terminals=["S", "A"],
    terminals=["a", "b"],
    start_symbol="S",
    productions=[
        ("S", ["a", "A"]),
        ("S", EPSILON_SYMBOL),
        ("A", ["a", "A"]),
        ("A", ["b"]),
    ],
)

af1 = AF(
    states=[set("S"), set("A"), set(GRAMMAR_FINAL_STATE)],
    alphabet=set(["0", "1"]),
    transition_function=[
        [[set("S"), "0"], set("S")],
        [[set("S"), "1"], set("S")],
        [[set("S"), "1"], set("A")],
        [[set("A"), "0"], set(GRAMMAR_FINAL_STATE)],
        [[set("A"), "ε"], set(GRAMMAR_FINAL_STATE)],
    ],
    start_state=set("S"),
    accept_states=[set(GRAMMAR_FINAL_STATE)],
)

if __name__ in "__main__":
    print_grammar_conversions(g1)
    check_word("", grammar=g1, valid=True)
    check_word("a", grammar=g1, valid=False)
    check_word("b", grammar=g1, valid=False)
    check_word("ab", grammar=g1, valid=True)
    check_word("ba", grammar=g1, valid=False)
    check_word("aab", grammar=g1, valid=True)
    check_word("aabb", grammar=g1, valid=False)
    check_word("aaaaaaaab", grammar=g1, valid=True)
    check_word("aaaaaaaaaabb", grammar=g1, valid=False)
    check_word("aaaaaabaaab", grammar=g1, valid=False)
