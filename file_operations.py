from typing import Tuple, List
from GLUD import GLUD
from AFND import AFND
from AFD import AFD
import re


class GrammarLoader:
    @staticmethod
    def parse_production(rule: str) -> Tuple[str, List[str]]:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = rhs.strip()
        return [lhs, list(rhs)]

    @staticmethod
    def extract_items(item):
        if item.startswith('{') and item.endswith('}'):
            return re.findall(r'[^,\s{}]+', item)
        return item

    @staticmethod
    def load_from_file(file_path: str) -> GLUD:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        only_symbols = lines[0].replace('# Gramática: G =', '')
        match = re.search(r"\{\s*([^{}]+?)\s*\}", only_symbols)

        if match:
            symbols = [s.strip() for s in match.group(1).split(',')]

        grammar_file_txt = open(file_path, 'r', encoding='utf-8').read()
        for i, original_symbol in enumerate(symbols):
            grammar_file_txt = grammar_file_txt.replace(original_symbol, f'q{i}')

        lines = [line.strip() for line in grammar_file_txt.split('\n') if line.strip()]
        grammar_symbols = lines[0].replace('# Gramática: G =', '')

        grammar = re.findall(r'({[^}]+}|[^,()\s]+)', grammar_symbols)
        grammar = [GrammarLoader.extract_items(element) for element in grammar]
        productions = []
        for line in lines[1:]:
            non_terminal = line.replace(' ','').split('->')[0]
            symbol = line.replace(' ','').split('->')[1][0]
            resut_non_terminal = line.replace(' ','').split('->')[1][1:]
            
            if resut_non_terminal != '':
                productions.append([non_terminal,[symbol, resut_non_terminal]])
            else:
                productions.append([non_terminal,[symbol]])

        grammar[1].append('ε')
        grammar[2] = productions

        return GLUD(non_terminals=grammar[0],
                    terminals=grammar[1],
                    productions=grammar[2],
                    start_symbol=grammar[3])


class AutomatonLoader:
    @staticmethod
    def load_AFND_from_file(file_path: str) -> AFND:
        automaton = AFND()
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        tf_list =[]
        for line in lines[1:]:
            if 'Q:' in line:
                automaton.states = line.replace(' ', '').replace('Q:', '').split(',')
            
            elif 'Σ:' in line:
                automaton.alphabet = line.replace(' ', '').replace('Σ:', '').split(',')

            elif 'q0:' in line:
                automaton.start_state = line.split(':')[0]

            elif 'F' in line:
                automaton.accept_states = line.replace(' ', '').replace('F:', '').split(',')
            
            elif 'δ:' in line:
                continue

            else:
                line = line.replace(' ', '').replace('->', ',').split(',')
                tf_list.append([[line[0],line[1]], line[2]])
        
        automaton.transition_function = tf_list
        return automaton
    
    @staticmethod
    def normalize_AFD_states(state_groups):
        normalized = []

        for group in state_groups:
            group = group.strip('{} ')
            states = [s.strip() for s in group.split(',') if s.strip()]
            suffixes = sorted(s[1:] for s in states if s.startswith('q'))
            normalized_state = 'q' + ''.join(suffixes)
            normalized.append(normalized_state)

        return normalized
    
    @staticmethod
    def load_AFD_from_file(file_path: str) -> AFD:
        automaton = AFD()
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        tf_list =[]
        for line in lines[1:]:
            if 'Q:' in line:
                line = line.replace(' ', '').replace('Q:', '').split(',')
                automaton.states = AutomatonLoader.normalize_AFD_states(line)
            
            elif 'Σ:' in line:
                automaton.alphabet = line.replace(' ', '').replace('Σ:', '').split(',')

            elif 'q0:' in line:
                automaton.start_state = line.split(':')[0]

            elif 'F' in line:
                automaton.accept_states = line.replace(' ', '').replace('F:', '').split(',')
            
            elif 'δ:' in line:
                continue

            else:
                line = line.replace(' ', '').replace('->', ',').replace('{', '').replace('}', '').split(',')
                tf_list.append([[line[0],line[1]], line[2]])
        
        automaton.transition_function = tf_list
        return automaton

    @staticmethod
    def write_AFND(automton: AFND, filename: str) -> None:
        if 'ε' in automton.alphabet:
            automton.alphabet.remove('ε')
        states_text = ', '.join(automton.states)
        alphabet_text = ', '.join(automton.alphabet)
        accept_states_text = ', '.join(automton.accept_states)
        
        transition_function = [f'{tf[0][0]}, {tf[0][1]} -> {tf[1]}' for tf in automton.transition_function]
        transition_function_text = '\n '.join(transition_function)

        text = f'''
        # AFN Original
        Q: {states_text}  
        Σ: {alphabet_text}  
        δ:  
        {transition_function_text}  
        {automton.start_state}: inicial  
        F: {accept_states_text}
        '''
        text = '\n'.join([line.strip() for line in text.splitlines()])

        open(filename, 'w').write(text)

    @staticmethod
    def format_state(state):
        digits = sorted(set(state.replace('q', '')))
        return '{' + ', '.join(f'q{d}' for d in digits) + '}'
    
    @staticmethod
    def replace_states(text):
        return re.sub(r'q[0-9]+', lambda m: AutomatonLoader.format_state(m.group()), text)

    @staticmethod
    def normalize_states(states):
        states_list =  [
            '{' + ', '.join(f'q{char}' for char in sorted(state[1:])) + '}'
            for state in states
        ][::-1]

        return ', '.join(states_list);

    @staticmethod
    def write_AFD(automton: AFD, filename: str) -> None:
        if 'ε' in automton.alphabet:
            automton.alphabet.remove('ε')

        states_text = AutomatonLoader.normalize_states(automton.states)
        alphabet_text = ', '.join(automton.alphabet)
        accept_states_text = AutomatonLoader.normalize_states(automton.accept_states)
        start_state_text = '{' + automton.start_state + '}'
        
        transition_function = [AutomatonLoader.replace_states(f"{tf[0][0]}, {tf[0][1]} -> {tf[1]}") for tf in automton.transition_function]
        transition_function_text = '\n '.join(transition_function)

        text = f'''
        # AFN Original
        Q: {states_text}  
        Σ: {alphabet_text}  
        δ:  
        {transition_function_text}  
        {start_state_text}: inicial  
        F: {accept_states_text}
        '''
        text = '\n'.join([line.strip() for line in text.splitlines()])

        open(filename, 'w').write(text)
