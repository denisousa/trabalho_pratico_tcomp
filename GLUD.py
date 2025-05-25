from abc import ABC, abstractmethod
from typing import Set, Dict, Tuple, Union, List
from GL import GL

class GLUD(GL):
    def is_valid_production(self, lhs: str, rhs: str) -> bool:
        if lhs not in self.non_terminals:
            return False
        if rhs == "":  # ε-production
            return True
        if len(rhs) == 1:
            return rhs in self.terminals
        if len(rhs) == 2:
            return rhs[0] in self.terminals and rhs[1] in self.non_terminals
        return False

    def validate_grammar(self) -> bool:
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                if not self.is_valid_production(lhs, rhs):
                    return False
        return True
