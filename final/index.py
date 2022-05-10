#!/usr/bin/env python3

from regex_check import *
from regex_tree import *
import settings

#Preprocessing Functions
def preprocess(regex):
    regex = clean_kleene(regex)
    regex = regex.replace(' ','')
    regex = '(' + regex + ')' + '#'
    while '()' in regex:
        regex = regex.replace('()','')
    return regex

def clean_kleene(regex):
    for i in range(0, len(regex) - 1):
        while i < len(regex) - 1 and regex[i + 1] == regex[i] and regex[i] == '*':
            regex = regex[:i] + regex[i + 1:]
    return regex

def gen_alphabet(regex):
    return set(regex) - set('()|*')

#setup
DEBUG = False
use_lambda = False
lambda_symbol = '_'
extra = ''
alphabet = None
settings.myList['DEBUG'] = DEBUG
settings.myList['use_lambda'] = use_lambda
settings.myList['lambda_symbol'] = lambda_symbol
settings.myList['extra'] = extra
settings.myList['alphabet'] = alphabet

#Main
regex = '(aa|b)*ab(bb|a)*'

#Check
if not is_valid_regex(regex):
    exit(0)

#Preprocess regex and generate the alphabet    
p_regex = preprocess(regex)
alphabet = gen_alphabet(p_regex)
settings.myList['alphabet'] = alphabet
#add optional letters that don't appear in the expression
alphabet = alphabet.union(set(extra))
settings.myList['alphabet'] = alphabet

#Construct
tree = RegexTree(p_regex)
if DEBUG:
    tree.write()
dfa = tree.toDfa()

#Test
message = 'baaab'
message2 = 'baaabb'
message3 = 'baaabbb'
print('This is the regex : ' + regex)
print('This is the alphabet : ' + ''.join(sorted(alphabet)))
print('This is the automata : \n')
dfa.write()
print('\nTesting for : "'+message+'" : ')
dfa.run(message)
print('\nTesting for : "'+message2+'" : ')
dfa.run(message2)
print('\nTesting for : "'+message3+'" : ')
dfa.run(message3)