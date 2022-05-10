"""
Regex validation:
brackets: ()
operators: *, |, .
"""
def is_valid_regex(regex):
    """
    Checking if the regex is valid
    """
    return valid_brackets(regex) and valid_operations(regex)


def valid_brackets(regex):
    """
    Checking if the brackets are balanced
    """
    opened_brackets = 0
    for char in regex:
        if char == '(':
            opened_brackets += 1
        if char == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            print('ERROR missing bracket')
            return False
    if opened_brackets == 0:
        return True
    print('ERROR unclosed brackets')
    return False


def valid_operations(regex):
    """
    Checking if the operators are valid
    """
    for i, char in enumerate(regex):
        if char == '*':
            if i == 0 or regex[i - 1] in '(|':
                print('ERROR * with no argument at', i)
                return False
        if char == '|':
            if i in (0, len(regex) - 1):
                print('ERROR | with missing argument at', i)
                return False
            if regex[i - 1] in '(|' or regex[i + 1] in ')|':
                print('ERROR | with missing argument at', i)
                return False
    return True
