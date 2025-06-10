from GLUD import GLUD
from global_variable import EPSILON_SYMBOL
from convert import Convert
from cli_operation import CLI_Printer
from file_operations import AutomatonLoader, GrammarLoader
from AF import AF
from global_variable import GRAMMAR_FINAL_STATE


def check_word(word: str, grammar: GLUD, valid: bool):
    print()
    afnd = Convert.convert_GLUD_AFND(grammar)
    afd = Convert.convert_AFND_AFD(afnd)

    CLI_Printer.print_word_steps(word, afd, valid)


def print_conversions(grammar: GLUD):
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
