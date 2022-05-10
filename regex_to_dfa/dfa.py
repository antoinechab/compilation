class Dfa:

    def __init__(self,Q,V,d,q0,F):
        self.Q = Q
        self.V = V
        self.d = d
        self.q0 = q0
        self.F = F

    def run(self, text):
        #Checking if the input is in the current alphabet
        if len(set(text) - self.V) != 0:
            #Not all the characters are in the language
            print('ERROR characters',(set(text)-self.V),'are not in the automata\'s alphabet')
            exit(0)
        
        #Running the automata
        q = self.q0
        for i in text:
            #Check if transition exists
            if q >= len(self.d):
                print('Message NOT accepted, state has no transitions')
                exit(0)
            if i not in self.d[q].keys():
                print('Message NOT accepted, state has no transitions with the character')
                exit(0)
            #Execute transition
            q = self.d[q][i]
        
        if q in self.F:
            print('Message accepted!')
        else:
            print('Message NOT accepted, stopped in an unfinal state')

    def write(self):
        for i in range(len(self.Q)):
            #Printing index, the delta fuunction for that transition and if it's final state
            print(i,self.d[i],'F' if i in self.F else '')