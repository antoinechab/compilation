from regex_node import *
from dfa import *
import settings

class RegexTree:

    def __init__(self, regex):
        self.root = RegexNode(regex)
        self.followpos = []
        self.functions()
    
    def write(self):
        self.root.write_level(0)

    def functions(self):
        positions = self.root.calc_functions(0, self.followpos)   
        if settings.myList['DEBUG'] == True:
            print(self.followpos)
    
    def toDfa(self):

        def contains_hashtag(q):
            for i in q:
                if self.followpos[i][0] == '#':
                    return True
            return False

        M = [] #Marked states
        Q = [] #States list in the followpos form ( array of positions ) 
        V = settings.myList['alphabet'] - {'#', settings.myList['lambda_symbol'] if settings.myList['use_lambda'] else ''} #Automata alphabet
        d = [] #Delta function, an array of dictionaries d[q] = {x1:q1, x2:q2 ..} where d(q,x1) = q1, d(q,x2) = q2..
        F = [] #FInal states list in the form of indexes (int)
        q0 = self.root.firstpos

        Q.append(q0)
        if contains_hashtag(q0):
            F.append(Q.index(q0))
        
        while len(Q) - len(M) > 0:
            #There exists one unmarked
            #We take one of those
            q = [i for i in Q if i not in M][0]
            #Generating the delta dictionary for the new state
            d.append({})
            #We mark it
            M.append(q)
            #For each letter in the automata's alphabet
            for a in V:
                # Compute destination state ( d(q,a) = U )
                U = []
                #Compute U
                #foreach position in state
                for i in q:
                    #if i has label a
                    if self.followpos[i][0] == a:
                        #We add the position to U's composition
                        U = U + self.followpos[i][1]
                U = sorted(list(set(U)))
                #Checking if this is a valid state
                if len(U) == 0:
                    #No positions, skipping, it won't produce any new states ( also won't be final )
                    continue
                if U not in Q:
                    Q.append(U)
                    if contains_hashtag(U):
                        F.append(Q.index(U))
                #d(q,a) = U
                d[Q.index(q)][a] = Q.index(U)
        
        return Dfa(Q,V,d,Q.index(q0),F)