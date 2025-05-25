from GLUD import GLUD
from AFND import AFND
import re


class GrammarLoader:
    @staticmethod
    def parse_production(rule: str) -> dict:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = rhs.strip()
        return {lhs: list(rhs)}

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
        grammar = re.findall(r'({[^}]+}|[^,()\s]+)', only_symbols)
        grammar = [GrammarLoader.extract_items(element) for element in grammar]

        productions = []
        for line in lines[1:]:
            productions.append(GrammarLoader.parse_production(line))

        grammar[2] = productions

        print('Grammar:', grammar)

        return GLUD(non_terminals=grammar[0],
                    terminals=grammar[1],
                    productions=grammar[2],
                    start_symbol=grammar[3])


    @staticmethod
    def write_AFND(automton: AFND) -> None:

        states_text = ', '.join(automton.states)
        alphabet_text = ', '.join(automton.alphabet)
        
        transition_function = [f'{tf[0][0]}, {tf[0][1]} -> {tf[1]}' for tf in automton.transition_function]
        transition_function_text = '\n '.join(transition_function)

        text = f'''
        # AFN Original
        Q: {states_text}  
        Σ: {alphabet_text}  
        δ:  
        {transition_function_text}  
        {automton.start_state}: inicial  
        F: {automton.accept_states}
        '''
        text = '\n'.join([line.strip() for line in text.splitlines()])

        open('AFND.txt', 'w').write(text)
