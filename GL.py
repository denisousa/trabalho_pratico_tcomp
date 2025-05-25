from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List

class GL(ABC):
    def __init__(self, non_terminals: Set[str], terminals: Set[str], start_symbol: str,
                 productions: List[Dict[str, List[str]]]):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions

    @abstractmethod
    def is_valid_production(self, lhs: str, rhs: str) -> bool:
        pass

    def display(self):
        print(f"Start Symbol: {self.start_symbol}")
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                print(f"{lhs} -> {rhs}")

