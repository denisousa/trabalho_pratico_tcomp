class State:
    def __init__(self, name_or_components):
        if isinstance(name_or_components, str):
            self.components = set([name_or_components])
        elif isinstance(name_or_components, (set, list)):
            self.components = set(name_or_components)
        elif isinstance(name_or_components, State):
            self.components = set(name_or_components.components)
        else:
            raise ValueError("Invalid argument type for State")

    def __iadd__(self, other):
        if isinstance(other, State):
            self.components.update(other.components)
        return self

    def __add__(self, other):
        if isinstance(other, State):
            new_state = State(self)
            new_state += other
            return new_state
        return NotImplemented

    def __eq__(self, other):
        return isinstance(other, State) and self.components == other.components

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return sorted(self.components) < sorted(other.components)

    def __hash__(self):
        return hash(frozenset(self.components))

    def copy(self):
        return State(self.components)

    def __str__(self):
        return "{" + ",".join(sorted(self.components)) + "}"

    def __repr__(self):
        return str(self)
