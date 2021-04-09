import unittest
import copy

from example_dfa import ExampleDFA
from bruteforce import BruteForcer


class TestDFAMethods(unittest.TestCase):

    maxDiff = None

    def test_bfs_one(self):
        my_dfa = ExampleDFA.one()
        self.assertEqual(
            my_dfa.bfs(), {'S1': True, 'S2': True, 'S3': True, 'S4': True})

    def test_bfs_two(self):
        my_dfa = ExampleDFA.two()
        self.assertEqual(my_dfa.bfs(), {'A': True, 'B': True})

    def test_random_states_and_transitions_initialisation(self):
        my_dfa = ExampleDFA.three()
        self.assertEqual(''.join(str(my_dfa.table_df).split(
        )), "01S0S7S13S1S1S22S2S6S6S4S9S23S5S2S0S6S24S0S7S19S11→S8S8S15S9S7S25*S10S2S5S11S16S9S12S24S0S13S1S15S14S13S10S15S6S5S16S18S12S17S15S20S18S10S8S19S14S26S20S8S25S21S8S26S22S17S2S23S8S25*S24S17S20*S25S4S21S26S19S26")

    # Inspiration from: https://stackoverflow.com/a/3166985
    def test_validity_checking(self):
        with self.assertRaises(ValueError) as context:
            ExampleDFA.four()
        self.assertTrue('Proposed DFA is not valid' in str(context.exception))

    # Tutorial 2
    def test_minimisation_one(self):
        my_dfa = ExampleDFA.five()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split()),
                         "ab→12{3,5}2{4,6}{3,5}*7{4,6}7{3,5}{4,6}7*{4,6}{4,6}{3,5}")

    # https://www.youtube.com/watch?v=o34C4l5OhN4
    def test_minimisation_two(self):
        my_dfa = ExampleDFA.six()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split()),
                         "abq1q1q3q3q1q4*q4q1{q0,q2}→{q0,q2}q1{q0,q2}")

    # Workshop 2
    def test_minimisation_three(self):
        my_dfa = ExampleDFA.seven()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split()),
                         "rb→ABCB{D,E}{D,E}C{D,E}F*F{D,E}C*G{D,E}G{D,E}{D,E}G")

    # https://www.youtube.com/watch?v=UiXkJUTkp44
    def test_minimisation_four(self):
        my_dfa = ExampleDFA.eight()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split()),
                         "10FFF→{A,B}{C,D,E}{A,B}*{C,D,E}F{C,D,E}")

    # Example 27 Case using another students seed
    def test_minimisation_five(self):
        my_dfa = ExampleDFA.nine()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split(
        )), "01S_1S_6S_23S_2S_22S_20S_6S_16S_7S_7S_23S_18→S_12S_12S_21S_13S_7S_19S_16S_20S_13S_18S_22S_18S_19S_1S_23*S_20S_12S_1S_21S_2S_20S_22S_1S_2S_23S_21S_1")

    # Hand made example (shared with other students)
    def test_minimisation_six(self):
        my_dfa = ExampleDFA.ten()
        my_dfa.state_minimisation()
        self.assertEqual(''.join(str(my_dfa.table_df).split(
        )), "01→test_s0test_s0{test_s1,test_s3}*test_s2test_s5test_s4*test_s4test_s4test_s5test_s5test_s5test_s2{test_s1,test_s3}test_s2{test_s1,test_s3}")

    def test_check_membership(self):
        my_dfa = ExampleDFA.three()
        self.assertEqual(my_dfa.check_membership(""), False)
        self.assertEqual(my_dfa.check_membership("1111"), False)
        self.assertEqual(my_dfa.check_membership("0000"), False)
        self.assertEqual(my_dfa.check_membership("010101010"), True)
        self.assertEqual(my_dfa.check_membership("110011"), False)

    def test_check_membership_minimised(self):
        my_dfa = ExampleDFA.three()
        my_dfa.state_minimisation()
        self.assertEqual(my_dfa.check_membership(""), False)
        self.assertEqual(my_dfa.check_membership("1111"), False)
        self.assertEqual(my_dfa.check_membership("0000"), False)
        self.assertEqual(my_dfa.check_membership("010101010"), True)
        self.assertEqual(my_dfa.check_membership("110011"), False)

    def test_check_membership_brute_force(self):
        my_dfa = ExampleDFA.three()
        minimum_acceptable_string = BruteForcer.bruteforce_dfa_check_string_membership(
            my_dfa, ['0', '1'])
        self.assertEqual(minimum_acceptable_string, "100")

    def test_check_membership_minimised_brute_force(self):
        my_dfa = ExampleDFA.three()
        my_dfa.state_minimisation()
        minimum_acceptable_string = BruteForcer.bruteforce_dfa_check_string_membership(
            my_dfa, ['0', '1'])
        self.assertEqual(minimum_acceptable_string, "100")

    def test_equivalence_simple_one(self):
        my_dfa_a = ExampleDFA.one()
        my_dfa_b = ExampleDFA.one()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_simple_two(self):
        my_dfa_a = ExampleDFA.three()
        my_dfa_b = copy.deepcopy(my_dfa_a)
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_simple_three(self):
        my_dfa_a = ExampleDFA.five()
        my_dfa_b = ExampleDFA.five()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_simple_four(self):
        my_dfa_a = ExampleDFA.six()
        my_dfa_b = ExampleDFA.six()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_simple_five(self):
        my_dfa_a = ExampleDFA.eight()
        my_dfa_b = ExampleDFA.eight()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_minimised_one(self):
        my_dfa_a = ExampleDFA.one()
        my_dfa_b = ExampleDFA.one()
        my_dfa_b.state_minimisation()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_minimised_two(self):
        my_dfa_a = ExampleDFA.three()
        my_dfa_b = copy.deepcopy(my_dfa_a)
        my_dfa_b.state_minimisation()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_minimised_three(self):
        my_dfa_a = ExampleDFA.five()
        my_dfa_b = ExampleDFA.five()
        my_dfa_b.state_minimisation()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_minimised_four(self):
        my_dfa_a = ExampleDFA.six()
        my_dfa_b = ExampleDFA.six()
        my_dfa_b.state_minimisation()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_equivalence_minimised_five(self):
        my_dfa_a = ExampleDFA.eight()
        my_dfa_b = ExampleDFA.eight()
        my_dfa_b.state_minimisation()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), True)

    def test_unequivalence_simple_one(self):
        my_dfa_a = ExampleDFA.one()
        my_dfa_b = ExampleDFA.two()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), False)

    def test_unequivalence_simple_two(self):
        my_dfa_a = ExampleDFA.three()
        my_dfa_b = ExampleDFA.nine()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), False)

    def test_unequivalence_simple_three(self):
        my_dfa_a = ExampleDFA.five()
        my_dfa_b = ExampleDFA.six()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), False)

    def test_unequivalence_simple_four(self):
        my_dfa_a = ExampleDFA.six()
        my_dfa_b = ExampleDFA.seven()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), False)

    def test_unequivalence_simple_five(self):
        my_dfa_a = ExampleDFA.eight()
        my_dfa_b = ExampleDFA.ten()
        self.assertEqual(my_dfa_a.equivalence_test(my_dfa_b), False)
