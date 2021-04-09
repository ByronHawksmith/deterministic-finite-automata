from dfa import DFA
from state import State
from dfa_factory import DFAFactory


class ExampleDFA:
    @classmethod
    def one(cls):
        state_1 = State('S1', {'0': 'S1', '1': 'S2'}, True, False)
        state_2 = State('S2', {'0': 'S3', '1': 'S4'}, False, True)
        state_3 = State('S3', {'0': 'S2', '1': 'S3'})
        state_4 = State('S4', {'0': 'S4', '1': 'S1'})
        state_5 = State('S5', {'0': 'S5', '1': 'S3'})
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5], alphabet=['0', '1'])

    @classmethod
    def two(cls):
        state_1 = State('A', {'0': 'A', '1': 'B'}, True, False)
        state_2 = State('B', {'0': 'B', '1': 'A'}, False, True)
        state_3 = State('C', {'0': 'A', '1': 'B'}, False, True)
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3], alphabet=['0', '1'])

    @classmethod
    def three(cls):
        return DFAFactory.from_range(['0', '1'], 27, 1, 3)

    # S5 Unreachable
    @classmethod
    def four(cls):
        state_1 = State('S1', {'0': 'S1', '1': 'S2'}, True, False)
        state_2 = State('S2', {'0': 'S3', '1': 'S4'})
        state_3 = State('S3', {'0': 'S2', '1': 'S3'})
        state_4 = State('S4', {'0': 'S4', '1': 'S1'})
        state_5 = State('S5', {'0': 'S5', '1': 'S3'}, False, True)
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5], alphabet=['0', '1'])

    # Tutorial 2
    @classmethod
    def five(cls):
        state_1 = State('1', {'a': '2', 'b': '3'}, True, False)
        state_2 = State('2', {'a': '4', 'b': '5'})
        state_3 = State('3', {'a': '6', 'b': '7'})
        state_4 = State('4', {'a': '4', 'b': '5'}, False, True)
        state_5 = State('5', {'a': '6', 'b': '7'})
        state_6 = State('6', {'a': '4', 'b': '5'}, False, True)
        state_7 = State('7', {'a': '6', 'b': '7'}, False, True)
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5, state_6, state_7],
                                          alphabet=['a', 'b'])

    # https://www.youtube.com/watch?v=o34C4l5OhN4
    @classmethod
    def six(cls):
        state_1 = State('q0', {'a': 'q1', 'b': 'q2'}, True, False)
        state_2 = State('q1', {'a': 'q1', 'b': 'q3'})
        state_3 = State('q2', {'a': 'q1', 'b': 'q2'})
        state_4 = State('q3', {'a': 'q1', 'b': 'q4'})
        state_5 = State('q4', {'a': 'q1', 'b': 'q2'}, False, True)
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5], alphabet=['a', 'b'])

    # Workshop 2
    @classmethod
    def seven(cls):
        state_1 = State('A', {'r': 'B', 'b': 'C'}, True, False)
        state_2 = State('B', {'r': 'D', 'b': 'E'})
        state_3 = State('C', {'r': 'D', 'b': 'F'})
        state_4 = State('D', {'r': 'D', 'b': 'G'})
        state_5 = State('E', {'r': 'D', 'b': 'G'})
        state_6 = State('F', {'r': 'D', 'b': 'C'}, False, True)
        state_7 = State('G', {'r': 'D', 'b': 'G'}, False, True)
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5, state_6, state_7],
                                          alphabet=['r', 'b'])

    # https://www.youtube.com/watch?v=UiXkJUTkp44
    @classmethod
    def eight(cls):
        state_1 = State('A', {'1': 'C', '0': 'B'}, True, False)
        state_2 = State('B', {'1': 'D', '0': 'A'})
        state_3 = State('C', {'1': 'F', '0': 'E'}, False, True)
        state_4 = State('D', {'1': 'F', '0': 'E'}, False, True)
        state_5 = State('E', {'1': 'F', '0': 'E'}, False, True)
        state_6 = State('F', {'1': 'F', '0': 'F'})
        return DFAFactory.from_parameters(states=[state_1, state_2, state_3, state_4, state_5, state_6], alphabet=['1', '0'])

    # Example 27 Case
    @classmethod
    def nine(cls):
        s1 = State('S_0', {'0': 'S_5', '1': 'S_13'})
        s2 = State('S_1', {'0': 'S_6', '1': 'S_23'})
        s3 = State('S_2', {'0': 'S_22', '1': 'S_20'})
        s4 = State('S_3', {'0': 'S_14', '1': 'S_18'})
        s5 = State('S_4', {'0': 'S_6', '1': 'S_21'})
        s6 = State('S_5', {'0': 'S_19', '1': 'S_1'})
        s7 = State('S_6', {'0': 'S_16', '1': 'S_7'})
        s8 = State('S_7', {'0': 'S_23', '1': 'S_18'})
        s9 = State('S_8', {'0': 'S_14', '1': 'S_2'})
        s10 = State('S_9', {'0': 'S_1', '1': 'S_22'})
        s11 = State('S_10', {'0': 'S_10', '1': 'S_6'})
        s12 = State('S_11', {'0': 'S_26', '1': 'S_7'}, False, True)
        s13 = State('S_12', {'0': 'S_12', '1': 'S_21'}, True, False)
        s14 = State('S_13', {'0': 'S_7', '1': 'S_19'})
        s15 = State('S_14', {'0': 'S_21', '1': 'S_25'}, False, True)
        s16 = State('S_15', {'0': 'S_18', '1': 'S_11'})
        s17 = State('S_16', {'0': 'S_20', '1': 'S_13'})
        s18 = State('S_17', {'0': 'S_7', '1': 'S_0'})
        s19 = State('S_18', {'0': 'S_22', '1': 'S_18'})
        s20 = State('S_19', {'0': 'S_1', '1': 'S_23'})
        s21 = State('S_20', {'0': 'S_12', '1': 'S_1'}, False, True)
        s22 = State('S_21', {'0': 'S_2', '1': 'S_20'})
        s23 = State('S_22', {'0': 'S_1', '1': 'S_2'})
        s24 = State('S_23', {'0': 'S_21', '1': 'S_1'})
        s25 = State('S_24', {'0': 'S_14', '1': 'S_18'})
        s26 = State('S_25', {'0': 'S_15', '1': 'S_8'})
        s27 = State('S_26', {'0': 'S_5', '1': 'S_14'})
        return DFAFactory.from_parameters(
            states=[s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22,
                    s23, s24, s25, s26, s27], alphabet=['0', '1'])

    # Hand made example (shared with other students)
    @classmethod
    def ten(cls):
        test_s0 = State("test_s0", {'0': 'test_s0',
                                    '1': 'test_s1'}, True, False)
        test_s1 = State("test_s1", {'0': 'test_s2', '1': 'test_s3'})
        test_s2 = State("test_s2", {'0': 'test_s5',
                                    '1': 'test_s4'}, False, True)
        test_s3 = State("test_s3", {'0': 'test_s2', '1': 'test_s1'})
        test_s4 = State("test_s4", {'0': 'test_s4',
                                    '1': 'test_s5'}, False, True)
        test_s5 = State("test_s5", {'0': 'test_s5', '1': 'test_s2'})
        test_s6 = State("test_s6", {'0': 'test_s6',
                                    '1': 'test_s4'}, False, True)
        return DFAFactory.from_parameters(
            states=[test_s0, test_s1, test_s2, test_s3, test_s4, test_s5, test_s6], alphabet=['0', '1'])

    # Another Example 27 Case
    @classmethod
    def eleven(cls):
        s1 = State('S0', {'0': 'S7', '1': 'S22'}, False, True)
        s2 = State('S1', {'0': 'S12', '1': 'S15'}, True, False)
        s3 = State('S2', {'0': 'S23', '1': 'S18'}, False, False)
        s4 = State('S3', {'0': 'S22', '1': 'S7'}, False, False)
        s5 = State('S4', {'0': 'S10', '1': 'S14'}, False, True)
        s6 = State('S5', {'0': 'S3', '1': 'S13'}, False, False)
        s7 = State('S6', {'0': 'S20', '1': 'S22'}, False, False)
        s8 = State('S7', {'0': 'S16', '1': 'S6'}, False, False)
        s9 = State('S8', {'0': 'S13', '1': 'S21'}, False, True)
        s10 = State('S9', {'0': 'S18', '1': 'S24'}, False, False)
        s11 = State('S10', {'0': 'S10', '1': 'S25'}, False, False)
        s12 = State('S11', {'0': 'S17', '1': 'S22'}, False, False)
        s13 = State('S12', {'0': 'S16', '1': 'S19'}, False, False)
        s14 = State('S13', {'0': 'S0', '1': 'S17'}, False, False)
        s15 = State('S14', {'0': 'S12', '1': 'S19'}, False, False)
        s16 = State('S15', {'0': 'S10', '1': 'S13'}, False, False)
        s17 = State('S16', {'0': 'S26', '1': 'S25'}, False, False)
        s18 = State('S17', {'0': 'S8', '1': 'S1'}, False, False)
        s19 = State('S18', {'0': 'S5', '1': 'S26'}, False, False)
        s20 = State('S19', {'0': 'S14', '1': 'S0'}, False, False)
        s21 = State('S20', {'0': 'S10', '1': 'S9'}, False, False)
        s22 = State('S21', {'0': 'S1', '1': 'S15'}, False, False)
        s23 = State('S22', {'0': 'S9', '1': 'S24'}, False, False)
        s24 = State('S23', {'0': 'S24', '1': 'S13'}, False, False)
        s25 = State('S24', {'0': 'S0', '1': 'S18'}, False, False)
        s26 = State('S25', {'0': 'S11', '1': 'S0'}, False, False)
        s27 = State('S26', {'0': 'S19', '1': 'S12'}, False, False)
        return DFAFactory.from_parameters(
            states=[s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22,
                    s23, s24, s25, s26, s27], alphabet=['0', '1'])

    # https://www.youtube.com/watch?v=nX4JrcHgpZY
    @classmethod
    def twelve(cls):
        s1 = State('q1', {'d': 'q2', 'c': 'q1'}, True, True)
        s2 = State('q2', {'d': 'q1', 'c': 'q3'})
        s3 = State('q3', {'d': 'q3', 'c': 'q2'})
        return DFAFactory.from_parameters(states=[s1, s2, s3], alphabet=['d', 'c'])

    # https://www.youtube.com/watch?v=nX4JrcHgpZY
    @classmethod
    def thirteen(cls):
        s4 = State('q4', {'d': 'q5', 'c': 'q4'}, True, True)
        s5 = State('q5', {'d': 'q4', 'c': 'q6'})
        s6 = State('q6', {'d': 'q6', 'c': 'q7'})
        s7 = State('q7', {'d': 'q4', 'c': 'q6'})
        return DFAFactory.from_parameters(states=[s4, s5, s6, s7], alphabet=['d', 'c'])
