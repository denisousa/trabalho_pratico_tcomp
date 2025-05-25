from file_operations import GrammarLoader
from convert import Convert

if __name__ == '__main__':
    grammar = GrammarLoader.load_from_file('./gramatica.txt')
    AFND_1 = Convert.convert_GLUD_AFND(grammar)
    
    GrammarLoader.write_AFND(AFND_1)