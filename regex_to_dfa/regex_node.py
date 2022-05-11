"""
Find all nodes of the regex and create a list of them
"""
from copy import deepcopy
from regex_check import is_valid_regex
from settings import SESSION

class RegexNode:
    """
    Find all nodes of the regex and create a list of them
    """
    # pylint: disable=too-many-instance-attributes

    @staticmethod
    def trim_brackets(regex):
        """
        Retrun the original regex
        """
        while regex[0] == '(' and regex[-1] == ')' and is_valid_regex(regex[1:-1]):
            regex = regex[1:-1]
        return regex

    @staticmethod
    def is_concat(char):
        """
        Check if the char is a concatenation
        """
        return char == '(' or RegexNode.is_letter(char)

    @staticmethod
    def is_letter(char):
        """
        Check if the char is a letter in the alphabet
        """
        return char in SESSION['alphabet']

    def test_leaf(self, regex):
        """
        Test if it is a leaf
        """
        if len(regex) == 1 and self.is_letter(regex):
            #Leaf
            self.item = regex
            #Lambda checking
            if SESSION['use_lambda']:
                if self.item == SESSION['lambda_symbol']:
                    self.nullable = True
                else:
                    self.nullable = False
            else:
                self.nullable = False
            return

    def priority(self, regex):
        """
        Return the priority of the node
        """
        if self.or_operator != -1:
            #Found an or operation
            self.item = '|'
            self.children.append(RegexNode(self.trim_brackets(regex[:self.or_operator])))
            self.children.append(RegexNode(self.trim_brackets(regex[(self.or_operator+1):])))
        elif self.concatenation != -1:
            #Found a concatenation
            self.item = '.'
            self.children.append(RegexNode(self.trim_brackets(regex[:self.concatenation])))
            self.children.append(RegexNode(self.trim_brackets(regex[self.concatenation:])))
        elif self.kleene != -1:
            #Found a kleene
            self.item = '*'
            self.children.append(RegexNode(self.trim_brackets(regex[:self.kleene])))

    def test_operator(self, regex, i):
        """
        Test operator type
        """
        if i == len(regex):
            return False
        if self.is_concat(regex[i]): #Testing if concatenation
            if self.concatenation == -1:
                self.concatenation = i
            return True
        if regex[i] == '*':  #Testing for kleene
            if self.kleene == -1:
                self.kleene = i
            return True
        if regex[i] == '|': #Testing for or operator
            if self.or_operator == -1:
                self.or_operator = i
            return True
        return False

    def build_init(self, regex):
        """
        Build the tree
        """
        if SESSION['DEBUG']:
            print('Current : '+regex)
        #Check if it is leaf
        self.test_leaf(regex)

        #It is an internal node
        #Finding the leftmost operators in all three
        i = 0

        #Getting the rest of terms
        while i < len(regex):
            if regex[i] == '(':
                #Composed block
                bracketing_level = 1
                #Skipping the entire term
                i+=1
                while bracketing_level != 0 and i < len(regex):
                    if regex[i] == '(':
                        bracketing_level += 1
                    if regex[i] == ')':
                        bracketing_level -= 1
                    i+=1
            else:
                #Going to the next char
                i+=1

            #Found a concatenation in previous iteration
            #And also it was the last element check if breaking
            if self.test_operator(regex, i):
                continue

        #Setting the current operation by priority
        self.priority(regex)

    def __init__(self, regex):
        self.nullable = None
        self.firstpos = []
        self.lastpos = []
        self.item = None
        self.position = None
        self.children = []

        self.kleene = -1
        self.or_operator = -1
        self.concatenation = -1

        self.build_init(regex)

    def kleene_process(self, positions):
        """
        Process kleene
        """
        #Is kleene
        #Firstpos
        self.firstpos = deepcopy(self.children[0].firstpos)
        #Lastpos
        self.lastpos = deepcopy(self.children[0].lastpos)
        #Nullable
        self.nullable = True
        #positions
        for i in self.children[0].lastpos:
            for j in self.children[0].firstpos:
                if j not in positions[i][1]:
                    positions[i][1] = sorted(positions[i][1] + [j])
        return positions

    def concat_process(self, positions):
        """
        Process concatenation
        """
        #Is concatenation
        #Firstpos
        if self.children[0].nullable:
            self.firstpos = sorted(
                list(set(self.children[0].firstpos + self.children[1].firstpos))
            )
        else:
            self.firstpos = deepcopy(self.children[0].firstpos)
        #Lastpos
        if self.children[1].nullable:
            self.lastpos = sorted(
                list(set(self.children[0].lastpos + self.children[1].lastpos))
            )
        else:
            self.lastpos = deepcopy(self.children[1].lastpos)
        #Nullable
        self.nullable = self.children[0].nullable and self.children[1].nullable
        #positions
        for i in self.children[0].lastpos:
            for j in self.children[1].firstpos:
                if j not in positions[i][1]:
                    positions[i][1] = sorted(positions[i][1] + [j])
        return positions

    def or_process(self):
        """
        Process or
        """
        #Is or operator
        #Firstpos
        self.firstpos = sorted(list(set(self.children[0].firstpos + self.children[1].firstpos)))
        #Lastpos
        self.lastpos = sorted(list(set(self.children[0].lastpos + self.children[1].lastpos)))
        #Nullable
        self.nullable = self.children[0].nullable or self.children[1].nullable

    def process_function(self, positions):
        """
        Process the function
        """
        if self.item == '.':
            positions = self.concat_process(positions)
        elif self.item == '|':
            self.or_process()
        elif self.item == '*':
            positions = self.kleene_process(positions)

        return positions

    def calc_functions(self, pos, positions):
        """
        Calculate the firstpos, lastpos and nullable functions
        """
        if self.is_letter(self.item):
            #Is a leaf
            self.firstpos = [pos]
            self.lastpos = [pos]
            self.position = pos
            #Add the position in the followpos list
            positions.append([self.item,[]])
            return pos+1
        #Is an internal node
        for child in self.children:
            pos = child.calc_functions(pos, positions)
        #Calculate current functions
        positions = self.process_function(positions)

        return pos

    def write_level(self, level):
        """
        Display the tree level by level
        """
        print(
            str(level) + ' ' +
            self.item,
            self.firstpos,
            self.lastpos,
            self.nullable,
            '' if self.position is None else self.position
        )
        for child in self.children:
            child.write_level(level+1)
