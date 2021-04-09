from state import State
from dfa import DFA


class DFAFactory:
    @classmethod
    def from_range(cls, alphabet: list, n_states: int, n_start_states: int, n_final_states: int):
        # Create a new empty list to hold generated states
        states = []

        # Generate n states and label them sequantially, addimg them to the states list
        for i in range(0, n_states):
            states.append(State.from_range("S" + str(i), alphabet, n_states))

        # Create a new empty DFA
        new_dfa = DFA()

        # Assign the alphabet to the DFA
        new_dfa.alphabet = alphabet

        # Create a new dictionary where the state name is the key and the state object is the
        # value, assign it to the DFA
        new_dfa.states = {k: v for k, v in [
            (state.name, state) for state in states]}

        # Assign n random start states, record their names in a set member variable
        new_dfa.assign_n_random_start_state_names(n_start_states)

        # Run bfs to determine which states are reachable and which are unreachable,
        # return the result
        bfs_output = new_dfa.bfs()

        # Assign which states are reachable and unreachable based on the output of bfs,
        # record their names in set member variables
        new_dfa.assign_reachable_unreachable_state_names(bfs_output)

        # After BFS, remove states that are unreachable from the states dictionary data structure
        new_dfa.remove_unreachable_states()

        # Assign n random final states, record their names in a set member variable
        new_dfa.assign_n_random_final_state_names(n_final_states)

        # Create transition table with only reachable states
        new_dfa.table_df = new_dfa.create_transition_table()

        # Check if the resultant dfa is valid (i.e. at least one final state is reachable from
        # any of the start states)
        invalid = new_dfa.check_invalid()

        # If for whatever reason it is invalid (shouldn't be possible), regenerate a new random
        # DFA
        if invalid:
            return DFAFactory.from_range(alphabet, n_states, n_start_states, n_final_states)
        else:
            return new_dfa

    @classmethod
    def from_parameters(cls, alphabet: list, states: list):
        # Create a new empty DFA
        new_dfa = DFA()

        # Assign the alphabet to the DFA
        new_dfa.alphabet = alphabet

        # Create a new dictionary where the state name is the key and the state object is the
        # value, assign it to the DFA
        new_dfa.states = {k: v for k, v in [
            (state.name, state) for state in states]}

        # Iterate over the states assigned to the dfa, find all states which are start states
        # and add them to the start_state_names set member variable
        new_dfa.start_state_names = new_dfa.find_start_state_names()

        # Run bfs to determine which states are reachable and which are unreachable,
        # return the result
        bfs_output = new_dfa.bfs()

        # Assign which states are reachable and unreachable based on the output of bfs,
        # record their names in set member variables
        new_dfa.assign_reachable_unreachable_state_names(bfs_output)

        # After BFS, remove states that are unreachable from the states dictionary data structure
        new_dfa.remove_unreachable_states()

        # Iterate over the remaining states assigned to the dfa, find all states which are final
        # states and add them to the final_state_names set member variable
        new_dfa.final_state_names = new_dfa.find_final_state_names()

        # Create transition table with only reachable states
        new_dfa.table_df = new_dfa.create_transition_table()

        # Check if the resultant dfa is valid (i.e. at least one final state is reachable from
        # any of the start states)
        invalid = new_dfa.check_invalid()

        # If the DFA is invalid, throw an error
        if invalid:
            raise ValueError("Proposed DFA is not valid")
        else:
            return new_dfa
