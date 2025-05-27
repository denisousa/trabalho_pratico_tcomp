from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List

class GL(ABC):
    def __init__(self, non_terminals: Set[str], terminals: Set[str], start_symbol: str,
                 productions: List[Tuple[str, List[str]]]):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions
