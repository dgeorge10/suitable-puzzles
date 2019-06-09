#!/usr/bin/env python3
import sys
#divide_list()
#parameters: L
#intention: input a list, and return the valued divided from left to right
#returns: a float
def divide_list(L):
    if len(L) == 0:
        return
    div = L[0]
    for item in L[1:]:
        if item == 0:
            return None
        div /= item
    return div

#recurse(L)
#parameters: L
#intention: This function will loop thru all of the values in the inputted list
#           If any element of the main list, is of type list, then we want to call divide_list() on that sublist and set
#           its value in the main list to whatever divide_list() returns 
#returns: A single list, with all divided values
def recurse(L):
    for x in range(0, len(L) ) :
        if type(L[x]) == list:
            L[x] = divide_list(recurse(L[x]))
    return L

#solve(L)
#parameters: L
#intention: this is the main function that will be used in order to process the entire inputted list
#returns: the answer!
def solve(L):
    singles = recurse(L)
    divided = divide_list(singles)
    return divided

if __name__ == "__main__":
    print(solve([[16, [8, 2], 4], 2, 80]))
