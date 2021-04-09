import random
import pandas as pd
import itertools
import collections

from state import State

random.seed(110235171)


class DFA:
    def __init__(self):
        self.alphabet = []
        self.states = {}
        self.start_state_names = []
        self.final_state_names = []
        self.reachable_state_names = []
        self.unreachable_state_names = []
        self.table_df = None

    @property
    def state_names(self):
        return list(self.states.keys())

    def create_transition_table(self):
        start_state_names = self.start_state_names
        final_state_names = self.final_state_names

        table_df = pd.DataFrame(columns=self.alphabet)
        for state in self.states.values():
            for symbol in self.alphabet:
                row_label = state.name
                if state.name in final_state_names:
                    row_label = '*' + row_label
                if state.name in start_state_names:
                    row_label = '\N{RIGHTWARDS ARROW}' + row_label
                table_df.at[row_label, symbol] = state.transitions.get(symbol)
        return table_df

    def check_membership(self, w=None):
        # w is a list of symbols, where each symbol is represented by a python string
        if w is None:
            w = []
        accepted = False
        for start_state in self.start_state_names:
            # get the next symbol from the input
            next_state = start_state
            for i in range(len(w)):
                next_symbol = w[i]
                # get the next state
                temp1 = self.states[next_state]
                temp2 = temp1.transitions.get(next_symbol)
                next_state = self.states[temp2].name
            if next_state in self.final_state_names:
                accepted = True
        if accepted:
            return True
        else:
            return False

    # Inspiration from: https://www.codespeedy.com/breadth-first-search-algorithm-in-python/
    def bfs(self):
        if not len(self.states) == 0:
            visited = {}
            frontier = [self.states[name] for name in self.start_state_names]
            for state in self.state_names:
                visited[state] = False
            # While frontier is not empty
            while frontier:
                node = frontier.pop(0)
                if not visited[node.name]:
                    visited[node.name] = True
                    neighbours = node.transitions
                    for neighbour in neighbours.values():
                        frontier.append(self.states[neighbour])
            return visited

    # Inspiration from: https://stackoverflow.com/a/942551
    #                   https://www.youtube.com/watch?v=o34C4l5OhN4
    #                   https://www.youtube.com/watch?v=UiXkJUTkp44
    def state_minimisation(self):
        final_states = self.final_state_names
        marked = []

        # Step 0, Prune Unreachable States
        unmarked = list(itertools.combinations(
            self.reachable_state_names, r=2))

        # Step 1, Mark each known distinguishable pair (defined as any pair that has one and only one accept state)
        for pair in unmarked:
            if len(set(final_states).intersection(pair)) == 1:
                marked.append(pair)

        unmarked = [pair for pair in unmarked if pair not in marked]

        # Step 2, For each unmarked pair (P,Q) such that [𝛿(P,x),𝛿(Q,x)] is marked, mark [P,Q] where 'x' is a given
        # input symbol from the alphabet. Repeat this process until no more changes can be made.
        changed = True
        while changed:
            changed = False
            newly_marked = []
            for pair in unmarked:
                state_obj_a = self.states[pair[0]]
                state_obj_b = self.states[pair[1]]
                for a in self.alphabet:
                    # Ignore potential pairs (1,1), (2,2), (3,3) etc...
                    if state_obj_a.transitions[a] != state_obj_b.transitions[a]:
                        # Ensure lexicographical tuple is constructed
                        if self.__make_lexical_tuple(state_obj_a.transitions[a], state_obj_b.transitions[a]) in marked:
                            if pair not in marked:
                                marked.append(pair)
                                newly_marked.append(pair)
                                changed = True
                                if pair in unmarked:
                                    unmarked.remove(pair)

        # Step 3, Squash pairs of states that overlap one another into one singular state
        # Inspiration from: https://stackoverflow.com/a/48762361
        #                   https://www.youtube.com/watch?v=UiXkJUTkp44 [16:00]
        flat_list = [item for sublist in unmarked for item in sublist]
        duplicates = [item for item, count in collections.Counter(
            flat_list).items() if count > 1]
        unmarked = [item for item in unmarked if item[1]
                    not in duplicates and item[0] not in duplicates]

        if not len(duplicates) == 0:
            unmarked.append(tuple(duplicates))

        # Step 4, Combine all the unmarked pairs and make them new states in the DFA
        tuple_names = {}
        tuple_objects = {}

        for tpl in unmarked:
            state_objects = [self.states[state_name] for state_name in tpl]
            start_state_flags = [
                state_obj.is_start for state_obj in state_objects]
            final_state_flags = [
                state_obj.is_final for state_obj in state_objects]

            new_state_name = "{"

            for idx, state in enumerate(state_objects):
                if idx != 0:
                    new_state_name += ","
                new_state_name += state.name

            new_state_name += "}"

            # Store for Step 6
            tuple_names[tpl] = new_state_name
            tuple_objects[tpl] = state_objects[0]

            # Transitions cannot be calculated here yet
            self.states[new_state_name] = State(
                new_state_name, None, True in start_state_flags, True in final_state_flags)

        # Step 5, Remove all the single states that are now part of a combined state in the DFA
        redundant_states = set()

        for tpl in unmarked:
            for state in tpl:
                redundant_states.add(state)

        minimal_state_names = [state.name for state in self.states.values(
        ) if state.name not in redundant_states]
        states = [state for state in self.states.values(
        ) if state.name in minimal_state_names]
        self.states = {k: v for k, v in [
            (state.name, state) for state in states]}

        # Step 6, Calculate new transitions
        state_names = self.states.keys()

        for tpl in unmarked:
            state = self.states[tuple_names[tpl]]
            new_transitions = {}
            for k, v in tuple_objects[tpl].transitions.items():
                for n_tpl in state_names:
                    if v in n_tpl:
                        new_transitions[k] = n_tpl
                        break

            state.transitions = new_transitions

        for state in self.states.values():
            new_transitions = {}

            for k, v in state.transitions.items():
                for n_tpl in state_names:
                    if v in n_tpl:
                        new_transitions[k] = n_tpl
                        break

            state.transitions = new_transitions

        # Iterate over the states assigned to the dfa, find all states which are start states
        # and add them to the start_state_names set member variable
        self.start_state_names = self.find_start_state_names()

        # Run bfs to determine which states are reachable and which are unreachable,
        # return the result
        bfs_output = self.bfs()

        # Assign which states are reachable and unreachable based on the output of bfs,
        # record their names in set member variables
        self.assign_reachable_unreachable_state_names(bfs_output)

        # After BFS, remove states that are unreachable from the states dictionary data structure
        self.remove_unreachable_states()

        # Iterate over the remaining states assigned to the dfa, find all states which are final
        # states and add them to the final_state_names set member variable
        self.final_state_names = self.find_final_state_names()

        # Create transition table with only reachable states
        self.table_df = self.create_transition_table()

    def equivalence_test(self, other_dfa):

        if(self.alphabet != other_dfa.alphabet):
            return False

        early_exit_condition = False

        initial_and_final_state_check_a = self.start_state_names[0] in self.final_state_names
        initial_and_final_state_check_b = other_dfa.start_state_names[
            0] in other_dfa.final_state_names

        if initial_and_final_state_check_a and initial_and_final_state_check_b:
            early_exit_condition = True
        elif initial_and_final_state_check_a and not initial_and_final_state_check_b:
            early_exit_condition = False
        elif not initial_and_final_state_check_a and initial_and_final_state_check_b:
            early_exit_condition = False
        else:
            early_exit_condition = True

        if not early_exit_condition:
            return False

        pairs = {}

        new_pairs_queue = [
            (self.start_state_names[0], other_dfa.start_state_names[0])]

        iteration = 0

        while new_pairs_queue:

            iteration += 1
            new_pair = new_pairs_queue.pop()
            self_start_name = new_pair[0]
            other_start_name = new_pair[1]

            zero_symb_trans_pair = (self.states[self_start_name].transitions[self.alphabet[0]],
                                 other_dfa.states[other_start_name].transitions[self.alphabet[0]])
            one_symb_trans_pair = (self.states[self_start_name].transitions[self.alphabet[1]],
                                 other_dfa.states[other_start_name].transitions[self.alphabet[1]])

            
            if zero_symb_trans_pair not in pairs:

                zero_trans_name_a = self.states[self_start_name].transitions[self.alphabet[0]]
                zero_trans_name_b = other_dfa.states[other_start_name].transitions[self.alphabet[0]]
            
                pairs[zero_symb_trans_pair] = [
                    self.states[zero_trans_name_a].is_final, other_dfa.states[zero_trans_name_b].is_final]

                if pairs[zero_symb_trans_pair][0] != pairs[zero_symb_trans_pair][1]:
                    return False

                new_pairs_queue.append(zero_symb_trans_pair)

            if one_symb_trans_pair not in pairs:

                one_trans_name_a = self.states[self_start_name].transitions[self.alphabet[1]]
                one_trans_name_b = other_dfa.states[other_start_name].transitions[self.alphabet[1]]

                pairs[one_symb_trans_pair] = [
                    self.states[one_trans_name_a].is_final, other_dfa.states[one_trans_name_b].is_final]

                if pairs[one_symb_trans_pair][0] != pairs[one_symb_trans_pair][1]:
                    return False 

                new_pairs_queue.append(one_symb_trans_pair)

        return True

    @staticmethod
    def __make_lexical_tuple(trans_a, trans_b):
        temp_list = [trans_a, trans_b]
        temp_list.sort()
        return temp_list[0], temp_list[1]

    # Assign n start states randomly
    def assign_n_random_start_state_names(self, n):
        self.start_state_names = []
        available_state_pool = self.state_names.copy()

        for _ in range(0, n):
            random_state = random.choice(available_state_pool)
            self.states[random_state].is_start = True
            self.start_state_names.append(random_state)
            available_state_pool.remove(random_state)

    # Assign n final states randomly
    def assign_n_random_final_state_names(self, n):
        self.final_state_names = []
        available_state_pool = self.state_names.copy()

        random_reachable_state = random.choice(self.reachable_state_names)
        self.states[random_reachable_state].is_final = True
        self.final_state_names.append(random_reachable_state)
        available_state_pool.remove(random_reachable_state)

        for _ in range(1, n):
            random_state = random.choice(available_state_pool)
            self.states[random_state].is_final = True
            self.final_state_names.append(random_state)
            available_state_pool.remove(random_state)

    def assign_reachable_unreachable_state_names(self, bfs_output):
        self.reachable_state_names = []
        self.unreachable_state_names = []
        for k, v in bfs_output.items():
            if v:
                self.reachable_state_names.append(k)
            else:
                self.unreachable_state_names.append(k)

        # Sort for itertools to ensure lexical ordering
        self.reachable_state_names.sort()
        self.unreachable_state_names.sort()

    def remove_unreachable_states(self):
        for state in self.unreachable_state_names:
            del self.states[state]

    # Checks if no accept states are reachable
    def check_invalid(self):
        # Check if all final states are unreachable
        # i.e. DFA is invalid
        return all(name in self.unreachable_state_names for name in self.final_state_names)

    def find_start_state_names(self):
        start_states = []
        for state in self.states.values():
            if state.is_start:
                start_states.append(state.name)
        return start_states

    def find_final_state_names(self):
        final_states = []
        for state in self.states.values():
            if state.is_final:
                final_states.append(state.name)
        return final_states

    def __str__(self):

        states_string = ""

        for state in self.states.values():
            states_string += str(state)

        return "{Alphabet: " + str(self.alphabet) + ", Reachable States: " + str(
            self.reachable_state_names) + ", Unreachable States: " + str(self.unreachable_state_names) + ", States: {" + str(
            states_string) + "}"
