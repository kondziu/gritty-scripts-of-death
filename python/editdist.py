#!/usr/bin/python3
#
# Edit distance
#
# Various methods to derive the edit difference between strings (how many
# operations are necessary to make the two strings identical). 
#
# The algorithms themselves were ripped off of Wikipedia and other places:
#     * http://en.wikipedia.org/wiki/Levenshtein_distance
#     * http://en.wikipedia.org/wiki/Damerau-Levenshtein_distance
#     * http://en.wikipedia.org/wiki/Hamming_distance
#     * http://en.wikipedia.org/wiki/Jaro-Winkler_distance and
#     * http://lingpipe-blog.com/2006/12/13/code-spelunking-jaro-winkler-string-comparison/
#     * http://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
# 
# Requires:
#     Python 3
#
# Author:
#     Konrad Siek <konrad.siek@gmail.com>
#
# License information:
#     Copyright 2011 Konrad Siek 
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

def __pp_arr_2d(array):
    """    Print a 2D array."""
    from sys import stdout
    for row in array:
        stdout.write("%s\n" % row)
    stdout.write("\n")

def __make_arr_2d(value, height, width):
    """    Create a 2d array of given size filled with given value."""
    arr = []
    for i in range(0, height):
        arr.append([None] * width)
    return arr

def hamming_distance(string_a, string_b, parameters={}):
    """    Establish the Hamming edit distance between strings.
    
    The Hamming distance between two strings is the number of substitutions
    required to make the first string identical to the other one.

    The Hamming distance requires the strings to be of same length. If they
    are not it returns -1.

    The Hamming distance function requires no additional parameters.
    """

    len_a, len_b = len(string_a), len(string_b)

    # Length needs to be the same for both strings.
    if len_a != len_b:
        return -1

    # Check for differences.
    changes = 0
    for i in range(0, len_a):
        if string_a[i] != string_b[i]:
            changes += 1

    return changes


def levenshtein_distance(string_a, string_b, parameters={}):
    """    Establish the Levenshtein edit distance between strings.
    
    The distance between identical strings is 0, and for each basic 
    difference between them (any change that needs to be applied to make
    them identical) the distance grows by 1.

    Basic operations include: insertion, deletion, and substitution. 

    The optional parameter 'cost' is the cost of the substitution operation
    (1 by default). (Parameter name: 'cost'.)
    """

    len_a, len_b = len(string_a), len(string_b)

    cost = parameters['cost'] if 'cost' in parameters else 1

    # Initialize array and fill it with zeros.
    d = []
    for i in range(0, len_a + 1):
        section = []
        d.append(section)
        for j in range(0, len_b + 1):
            section.append(0)

    # Maximum distances.
    for i in range(1, len_a + 1):
        d[i][0] = i
    for j in range(1, len_b + 1):
        d[0][j] = j

    # Dynamic programming FTW.
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            d[i][j] = d[i-1][j-1] \
                if string_a[i-1] == string_b[j-1] \
                else min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + cost)

    return d[len_a][len_b]


def damerau_levenshtein_distance(string_a, string_b, parameters={}):
    """    Establish the Damerau-Levenshtein edit distance between strings.
    
    The distance between identical strings is 0, and for each basic 
    difference between them (any change that needs to be applied to make
    them identical) the distance grows by 1.

    Basic operations include: insertion, deletion, substitution, and 
    transportation of two characters.

    The Damerau-Levenshtein distance differs from the basic Levenshtein
    distance in that it allows for the transportation operation.

    The optional parameter 'cost' is the cost of the substitution operation
    (1 by default). (Parameter name: 'cost'.)
    """

    len_a, len_b = len(string_a), len(string_b)

    cost = parameters['cost'] if 'cost' in parameters else 1
    
    # Initialize array and fill it with zeros.
    d = []
    for i in range(0, len_a + 1):
        section = []
        d.append(section)
        for j in range(0, len_b + 1):
            section.append(0)

    # Maximum distances.
    for i in range(1, len_a + 1):
        d[i][0] = i
    for j in range(1, len_b + 1):
        d[0][j] = j

    # Dynamic programming FTW.
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            d[i][j] = d[i-1][j-1] \
                if string_a[i-1] == string_b[j-1] \
                else min(d[i-1][j] + 1, d[i][j-1], d[i-1][j-1] + cost)
            # Check for transposition.
            if i > 1 and j > 1 \
                and string_a[i-1] == string_b[j-2] \
                and string_a[i-2] == string_b[j-1]:
                d[i][j] = min(d[i][j], d[i-2][j-2] + cost)

    return d[len_a][len_b]


def jaro_distance(string_a, string_b, parameters={}):
    """    Establish the Jaro-Winkler edit distance between strings.
    
    The Jaro distance is useful for duplicate detection and it is aimed at short
    strings. It returns a score between 0 and 1 where a higher score signifies 
    more similar strings.

    The Jaro distance function requires no additional parameters.
    """

    # The algotihm consists of two basic parts: matching and transpositions: 
    # each of these is extracted into a sub-function.
    def __matching_chars(string_a, string_b):
        """    Align characters of one string against those of the other 
        string. """

        length_a, length_b = len(string_a), len(string_b)

        max_dist = max(length_a, length_b) / 2 - 1

        matching_a = [ False for i in range(0, length_a) ]
        matching_b = [ False for i in range(0, length_b) ]

        for i in range(0, length_a):
            for j in range(0, length_b):
                if string_a[i] == string_b[j]:
                    if i - j  == 0 or abs(i - j) < max_dist:
                        matching_a[i] = True
                        matching_b[j] = True

        return matching_a, matching_b

    def __transpositions(string_a, string_b, matching_a, matching_b):
        """    Extract subsequences of alike characters and count those that 
        cannot be alined as requiring transpositions. """

        def __make_sequence(string, matching):
            """    Extract a subsequence where both strings match. """

            sequence = []
            for i in range(0, len(string)):
                if matching[i]:
                    sequence.append(string[i])
            return sequence

        # Find subsequences.
        sequence_a = __make_sequence(string_a, matching_a)            
        sequence_b = __make_sequence(string_b, matching_b)
        
        half_transpositions = 0

        # Count half-transpositions.
        for i in range(0, min(len(sequence_a), len(sequence_b))):
            #print(len(sequence_a), len(sequence_b), i)
            if sequence_a[i] != sequence_b[i]:
                half_transpositions += 1
        half_transpositions += abs(len(sequence_a) - len(sequence_b))

        return half_transpositions / 2
    
    matching_a, matching_b = __matching_chars(string_a, string_b)

    m = float(matching_a.count(True))
    t = float(__transpositions(string_a, string_b, matching_a, matching_b))

    len_a = float(len(string_a))
    len_b = float(len(string_b))

    module_a = m / len_a if len_a > 0 else 0
    module_b = m / len_b if len_b > 0 else 0
    module_t = (m - t) / m if m > 0 else 0

    return (module_a + module_b + module_t) / 3.0


def jaro_winkler_distance(string_a, string_b, parameters={}):
    """    Establish the Jaro-Winkler edit distance between strings.
    
    The Jaro-Winkler distance is useful for duplicate detection and it is aimed
    at short strings. It returns a score between 0 and 1 where a higher score 
    signifies more similar strings. 

    The Jaro-Winkler distance is more favorable to strings which have a common
    prefix. The length of the prefix is 4. (Parameter name: 'max_prefix'.)

    The weight given to the similarity of prefixes is set by the scaling factor
    p which typically is set to 0.1 and should not exceed 0.25 because the 
    distance could then be larger than 1. (Parameter name: 'p'.)
    """

    # Parameters and defaults.    length_b
    p = parameters['p'] if 'p' in parameters else 0.1
    max_prefix = parameters['max_prefix'] if 'max_prefix' in parameters else 4

    # Establish the ordinary Jaro distance.
    dj = jaro_distance(string_a, string_b, parameters)
    l = 0

    # Account for the prefix - words starting similarly are considered more 
    # similar.    
    for i in range(0, min(len(string_a), len(string_b), max_prefix)):
        if string_a[i] == string_b[i]:
            l += 1
        else:
            break

    # Adjust the distance with the prefix-related score.
    return dj + (p * l * (1 - dj))


def wagner_fischer_distance (string_a, string_b, parameters={}):
    """    Establish the Levenshtein edit distance between strings using the 
    Wagner-Fischer dynamic programming algorithm.

    Algorithm X in the original article.

    The distance between identical strings is 0, and for each basic 
    difference between them (any change that needs to be applied to make
    them identical) the distance grows by 1.

    Basic operations include: insertion, deletion, substitution.

    The optional parameter 'cost' is the cost of the substitution operation
    (1 by default). (Parameter name: 'cost'.)
    """
    removal_cost = 1
    insertion_cost = 1
    substitution_cost = 1 if 'cost' not in parameters else parameters['cost']            

    length_a = len(string_a) + 1
    length_b = len(string_b) + 1   

    d = __make_arr_2d(None, height=length_a, width=length_b)

    d[0][0] = 0
    
    # Fill in the defaults for string A.
    for i in range(1, length_a):
        d[i][0] = d[i - 1][0] + removal_cost # of removing string_a[i - 1]

    # Fill in the defaults for string B.
    for j in range(1, length_b):
        d[0][j] = d[0][j - 1] + insertion_cost # of inserting string_b[i - 1]

    # The trace cost function (gamma in the original article): it is simplified
    # to check only whether the two characters are the same or not. No empty 
    # strings are expected though.
    gamma = lambda a, b: 0 if a == b else substitution_cost
    
    # Fill in the rest of the array.
    for i in range(1, length_a):
        for j in range(1, length_b):
            m1 = d[i - 1][j - 1] + gamma(string_a[i - 1], string_b[j - 1])
            m2 = d[i - 1][j] + removal_cost # of removing string_a[i - 1]
            m3 = d[i][j - 1] + insertion_cost # of inserting string_b[j - 1]
            
            d[i][j] = min(m1, m2, m3)

    return d[length_a - 1][length_b - 1]

# All the functions and their names for convenience.
API = {
    'Levenshtein': levenshtein_distance, 
    'Damerau-Levenshtein': damerau_levenshtein_distance, 
    'Hamming': hamming_distance,
    'Jaro': jaro_distance,
    'Jaro-Winkler': jaro_winkler_distance,
    'Wagner-Fischer': wagner_fischer_distance, 
}

# A demonstration.
if __name__ == '__main__':
    from sys import argv, stdout

    if len(argv) < 3 or len(argv) % 2 < 1:
        stdout.write("Usage: %s WORD_A WORD_B [ WORD_A WORD_B [...] ]\n" \
                                                                    % argv[0])
        exit(-1)
    
    for i in range(1, int(len(argv)/2) + 1):

        word_a = argv[2*i - 1]
        word_b = argv[2*i]
        sentence_a, sentence_b = [s.split() for s in [word_a, word_b]]
        
        title = 'distance between "%s" and "%s"' % (word_a, word_b)
        maxlen = max([len(i) for i in API.keys()] + [len(title)])

        row = '| %' + str(maxlen) + 's | %5d | %5d |\n'
        strrow = row.replace('d', 's')
        edge = '%s\n' % ('-' * (29 + maxlen))
        rule = strrow.replace('|', '+').replace(' ', '-') % \
                                            (maxlen * '-', 5 * '-', 5 * '-')
        
        stdout.write(rule)
        stdout.write(row.replace('d', 's') % (title, 'words', 'lists'))
        stdout.write(rule)
        for method in API:
            word_r = API[method](word_a, word_b)
            sentence_r = API[method](sentence_a, sentence_b) 
            stdout.write(row % (method, word_r, sentence_r))
        stdout.write(rule)
        stdout.write("\n")

