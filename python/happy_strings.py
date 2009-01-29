#!/usr/bin/python
#
# Happy strings
# 
# More or less purposeless script, which takes strings, splits
# them up  into characters and then creates a Python print 
# statements which  reproduce the same strings in a 
# complicated, slightly less readable form... but a slightly 
# happier form, methinks.
#
# Parameters:
#   a list of strings to reproduce
# Author:
#   Konrad Siek

import sys

def escape_string(string):
    if string in ["\'", "\"", "\\"]:
        return "\\" + string
    elif string == "\n":
        return "\\n"
    return string

def output_string(string, counter, last):
    output = "'" + escape_string(string) + "'"
    if counter != 1:
        output += ' * ' + str(counter)
    if not last:
        output += ' + '
    return output

for string in sys.argv[1:]:
    output = 'print '
    previous = None
    counter = 0 
    length = len(string)
    for i in range(0, length):
        character = string[i]
        if character == previous:
            counter += 1
        else:
            if previous != None:                
                output += output_string(
                    previous, 
                    counter, 
                    False
                )
            counter = 1
            previous = character
    output += output_string(
        previous, 
        counter, 
        True
    )
    print output
