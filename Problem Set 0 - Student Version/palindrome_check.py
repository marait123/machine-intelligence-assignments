import utils


def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    # TODO: ADD YOUR CODE HERE
    i, j = 0, len(string)-1
    while i <= j and string[i] == string[j]:
        i, j = i+1, j-1
    if i > j:
        return True
    else:
        return False
