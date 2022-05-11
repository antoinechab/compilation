"""
Run automata on a message
"""
import sys

class Dfa:
    """
    Run automata on a message
    """
    # pylint: disable=too-many-arguments

    def __init__(self,state_list,alphabet,delta,current_state,finale_states):
        self.state_list = state_list
        self.alphabet = alphabet
        self.delta = delta
        self.current_state = current_state
        self.finale_states = finale_states

    def run(self, text):
        """
        Run automata on a message
        """
        #Checking if the input is in the current alphabet
        if len(set(text) - self.alphabet) != 0:
            #Not all the characters are in the language
            print(
                'ERROR characters',(set(text)-self.alphabet),
                'are not in the automata\'s alphabet'
            )
            sys.exit(0)

        #Running the automata
        current = self.current_state
        for i in text:
            #Check if transition exists
            if current >= len(self.delta):
                print('Message NOT accepted, state has no transitions')
                sys.exit(0)
            if i not in self.delta[current].keys():
                print('Message NOT accepted, state has no transitions with the character')
                sys.exit(0)
            #Execute transition
            current = self.delta[current][i]

        if current in self.finale_states:
            print('Message accepted!')
        else:
            print('Message NOT accepted, stopped in an unfinal state')

    def write(self):
        """
        Display the tree in the console if debug is true
        """
        for i in range(len(self.state_list)):
            #Printing index, the delta fuunction for that transition and if it's final state
            print(i,self.delta[i],'F' if i in self.finale_states else '')
