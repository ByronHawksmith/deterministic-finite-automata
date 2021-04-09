import itertools


class BruteForcer():
    @classmethod
    def bruteforce_dfa_check_string_membership(cls, dfa, alphabet):
        found = False
        r = 1
        current = []

        while not found:
            perms = list(itertools.product(alphabet, repeat=r))

            for perm in perms:
                current = ''.join(perm)
                outcome = dfa.check_membership(current)
                if outcome:
                    found = True
                    break

            r += 1

        return current
