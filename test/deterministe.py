#!/usr/bin/env python3

def regular_expression_to_deterministic_finite_automaton(regex):
    """
    Convert a regular expression to a deterministic finite automaton.
    """
    return []

if __name__ == '__main__':
    #regex = input('Enter a regular expression: ')
    regex = "(2+32)*5+8"
    automaton = regular_expression_to_deterministic_finite_automaton(regex)
    print('\n')
    print('Deterministic finite automaton:')
    print(automaton)