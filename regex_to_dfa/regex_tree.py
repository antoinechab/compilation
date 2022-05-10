"""
Make the deterministe automata from regex
"""

from regex_node import RegexNode
from dfa import Dfa
import settings

class RegexTree:
    """
    Make the deterministe automata from regex
    """

    def __init__(self, regex):
        self.root = RegexNode(regex)
        self.positions = []
        self.functions()

    def write(self):
        """
        Display the tree in the console if debug is true
        """
        self.root.write_level(0)

    def functions(self):
        """
        Parse positions and build the tree
        """
        self.root.calc_functions(0, self.positions)
        if settings.myList['DEBUG'] is True:
            print(self.positions)

    def to_dfa(self):
        """
        return the deterministic final automata from the regex
        """
        def contains_hashtag(regex):
            for i in regex:
                if self.positions[i][0] == '#':
                    return True
            return False

        marked_states = []
        state_list = []
        alphabet = settings.myList['alphabet'] - {
            '#', settings.myList['lambda_symbol'] if settings.myList['use_lambda'] else ''
        }
        delta = []
        finale_states = []
        current_state = self.root.firstpos

        state_list.append(current_state)
        if contains_hashtag(current_state):
            finale_states.append(state_list.index(current_state))

        while len(state_list) - len(marked_states) > 0:
            unmarked_state = [i for i in state_list if i not in marked_states][0]
            delta.append({})
            marked_states.append(unmarked_state)

            for char in alphabet:
                destination_state = []

                for i in unmarked_state:
                    if self.positions[i][0] == char:
                        destination_state = destination_state + self.positions[i][1]
                destination_state = sorted(list(set(destination_state)))
                #Checking if this is char valid state
                if len(destination_state) == 0:
                    #No positions, skipping, it won't produce any new states ( also won't be final )
                    continue
                if destination_state not in state_list:
                    state_list.append(destination_state)
                    if contains_hashtag(destination_state):
                        finale_states.append(state_list.index(destination_state))

                delta[state_list.index(unmarked_state)][char] = state_list.index(destination_state)

        return Dfa(state_list,alphabet,delta,state_list.index(current_state),finale_states)
