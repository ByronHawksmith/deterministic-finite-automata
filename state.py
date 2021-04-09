import random

random.seed(110235171)


class State:
    def __init__(self, name, transitions=None, is_start=False, is_final=False):
        self.transitions = transitions
        self.name = name
        self.is_start = is_start
        self.is_final = is_final

    @classmethod
    def from_range(cls, name, alphabet, n):
        transitions = {}

        for a in alphabet:
            transitions[a] = "S" + str(random.randrange(n))

        return State(name, transitions)

    def __str__(self):
        return "{Name: " + self.name + ", Transitions: " + str(
            self.transitions) + ", Start: " + str(self.is_start) + ", Final: " + str(self.is_final) + "}, "
