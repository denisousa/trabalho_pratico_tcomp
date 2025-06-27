from AF import AF

def check_valid_word(word: str, automaton: AF):
    for i, w in enumerate(word):
        if i == 0:
            current_state = automaton.start_state

        for t in automaton.transition_function:
            if t[0][0] == current_state and t[0][1] == w:
                current_state = t[1]
                break

        if i == len(word) - 1 and current_state in automaton.accept_states:
            return True
        
    return False
