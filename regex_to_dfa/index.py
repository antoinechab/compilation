#!/usr/bin/env python3
"""
Init variables and run programme
"""

import sys
from regex_check import is_valid_regex
from regex_tree import RegexTree
from settings import SESSION

#Preprocessing
def preprocess(regex):
    """
    Surrount regex and remove useless characters
    """
    regex = clean_kleene(regex)
    regex = regex.replace(' ','')
    regex = '(' + regex + ')' + '#'
    while '()' in regex:
        regex = regex.replace('()','')
    return regex

def clean_kleene(regex):
    """
    Clean regex from useless characters
    """
    for i in range(0, len(regex) - 1):
        while i < len(regex) - 1 and regex[i + 1] == regex[i] and regex[i] == '*':
            regex = regex[:i] + regex[i + 1:]
    return regex

def gen_alphabet(regex):
    """
    Return the alphabet of the regex
    """
    return set(regex) - set('()|*')

if __name__ == '__main__':

    REGEX_VALID = 'baa*(bb|a)*(a|b)*c'
    REGEX_UNVALID = '*(aa|b)*ab(bb|a)*'

    print("unvalid regex: " + REGEX_UNVALID)
    is_valid_regex(REGEX_UNVALID)
    print("\n")

    if not is_valid_regex(REGEX_VALID):
        sys.exit(0)

    #Preprocess regex and generate the alphabet
    p_regex = preprocess(REGEX_VALID)
    SESSION['alphabet'] = gen_alphabet(p_regex)
    #add optional letters that don't appear in the expression
    SESSION['alphabet'] = SESSION['alphabet'].union(set(SESSION['extra']))

    #Construct
    tree = RegexTree(p_regex)
    if SESSION['DEBUG']:
        tree.write()
    dfa = tree.to_dfa()

    #Test
    MESSAGE = 'baaabc'
    MESSAGE2 = 'baaabb'
    MESSAGE3 = 'baaabbbc'
    print('Valid regex : ' + REGEX_VALID)
    print('alphabet : '+ ''.join(sorted(SESSION['alphabet'])).replace('#',''))
    print('automata : \n')
    # print the automata in the console (with states they transitions and final states (F))
    dfa.write()
    #ok
    print('\nTest for : "'+MESSAGE+'" : ')
    dfa.run(MESSAGE)
    #ko cause the last letter end on an unfinal state
    print('\nTest for : "'+MESSAGE2+'" : ')
    dfa.run(MESSAGE2)
    #ok
    print('\nTest for : "'+MESSAGE3+'" : ')
    dfa.run(MESSAGE3)
