#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tabrot
#
# The script reads the array from standard input, applies the specified 
# transformations and prints the new array to standard output. The 
# transformations include rotating the array (90°, 180°, 270°, and 0°) or 
# flipping it (horizontally, vertically, or both).
#
# The input array is expected to be in a text format. The particular row and 
# field delimiters can be set up with the appropriate options (see below).
#
# The functions used in the script can also be used via Python instead of a 
# commandline tool, if your fancy takes you that way.
#
# Usage:
#   tabrot.py [OPTIONS]
#
# Options:
#   Rotating:
#       -c, --clockwise     rotate the array clockwise (right).
#       -C, --counter-clockwise
#                           rotate the array counter-clockwise (left).
#       -r, --rotate-180    rotate the array 180? - make it upside-down.
#       -m, --meh, --do-nothing
#                           rotate the array 0? - not at all.
#   Flipping (mirroring):
#       -f, --horizontal-flip
#                           flip the array horizontally.
#       -v, --vertical-flip
#                           flip the array vertically.
#       -b, --horizontal-and-vertical-flip
#                           flip the array both vertically and horizontally.
#   Delimiters:
#       -d DELIM, --field-delimiter=DELIM
#                           specify a field (column) delimiter instead of ",".
#       -D DELIM, --row-delimiter=DELIM
#                           specify a row delimiter instead of " ".
#   Printing:
#       -s TEMPLATE, --print-template=TEMPLATE
#                           set a sprintf-like template for cells, default: "%s"
#       -e STRING, --empty-field-symbol=STRING
#                           set a string to use for empty cells instead of " ".
#       -n, --no-newline    do not append new line at the end of output.
#   -h, --help            show this help message and exit
#
# Examples:
#   echo -en "a,b,c\n1,2,3" | ./tabrot.py -c            # result: 1,a\n2,b\n3,c
#   echo 'a&b&c|1&2&3' | ./tabrot.py -d'&' -D'|' -f     # result: c&b&a|3&2&1
#
# Author:
#   Konrad Siek <konrad.siek@gmail.com>
#
# License:
#   Copyright 2010 Konrad Siek
#
#   This program is free software: you can redistribute it and/or modify it 
#   under the terms of the GNU General Public License as published by the Free 
#   Software Foundation, either version 3 of the License, or (at your option) 
#   any later version. See  <http://www.gnu.org/licenses/> for details.

# Default constants that get used by all the functions unless other values are
# specified via arguments.
COL_DELIM = ','
ROW_DELIM = '\n'
EMPTY_SYM = ' '
PRINT_TPL = '%s'

def rotate_clockwise(array, empty=EMPTY_SYM):
    """ Rotate a 2D array clockwise (rightward) returning a copy of the array.
    By a 2D array I mean a list containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.
    
    If the array is ragged (contains rows of different lengths), then it will
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _cw_coord_trans, empty=empty)

def rotate_counterclockwise(array, empty=EMPTY_SYM):
    """ Rotate a 2D array counter-clockwise (leftward) returning a copy of the
     array. By a 2D array I mean a list containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _ccw_coord_trans, empty=empty)

def rotate_180_degrees(array, empty=EMPTY_SYM):
    """ Rotate a 2D array upside-down (180° as the name implies) returning a
    copy of the array. By a 2D array I mean a list containing lists containing
    strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will 
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _180_coord_trans, swap=False, empty=empty)

def flip_horizontal(array, empty=EMPTY_SYM):
    """ Flip a 2D array horizontally (left-to-right) returning a copy of the 
    array. By a 2D array I mean a list containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will 
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _flip_horz_trans, swap=False, empty=empty)

def flip_vertical(array, empty=EMPTY_SYM):
    """ Flip a 2D array vertically (upside-down) returning a copy of the
    array. By a 2D array I mean a list containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _flip_vert_trans, swap=False, empty=empty)

def flip_horizontal_and_vertical(array, empty=EMPTY_SYM):
    """ Flip a 2D array vertically and horizontally (both upside-down and
    left-to-right) returning a copy of the array. By a 2D array I mean a list
    containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will 
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _flip_both_trans, swap=False, empty=empty)

def rotate_not_at_all(array, empty=EMPTY_SYM):
    """ Rotate a 2D array 0° returning a copy of the array. That is to say, 
    do not rotate the array at all, but apply all the delimiter splitting and 
    conversions that would've been applied had the array been rotated. 

    By a 2D array I mean a list containing lists containing strings.

    If an empty element occurs (a string of length 0), then it gets replaced
    with blanks - whatever is provided through the parameter 'empty'.

    If the array is ragged (contains rows of different lengths), then it will 
    be filled out with blanks during the transformation.

    Note that the original array is left intact."""

    return transpose(array, _meh_coord_trans, swap=False, empty=empty)

def transpose(arr, coord_trans, swap=True, empty=EMPTY_SYM):
    """ Perform a specific transformation on the given array returning a new
    version of the array.

    The general functioning can be roughly (and cryptically) described as:
        (i', j') ← coord_trans(i, j, n, m)       i = 1...n, j = 1...m
        ∀i,∀j new_array[i'][j'] ← old_array[i][j]

    That is, the coordinates of each elements in the old array are translated
    in the coordinates the elemnt should be in in the new array, and when those
    are ready, the element is pasted there.

    The parameter coord_trans specifies a function that translates indexes of 
    the old array to the indexes of the new array, and it is of type:
         int->int->int->int->(int, int)         

    This means it takes 4 integers as arguments and returns a two-integer 
    tupple.The parameters are: 
        * i - a row index of the old array (1st dimension)
        * j - a column index of the old array (2nd dimension)
        * n - the number of rows 
        * m - the number of columns (the maximum number of columns, if ragged)

    An example of a coord_trans function (that rotates the array clockwise) is:
        coord_trans = lambda i, j, n, m: (j, n - 1 - i)

    The parameter swap indicates whether the array will be put on one of its 
    sides or if it will be put on its top or bottom. True indicates that the
    array will be on the side after the transformation (rows become columns and
    vice-versa; in other words, i' will be a function of j and j' a function 
    of i). False indicates that the array will be either as it was or 
    upside-down or similar (columns remain columns, etc; in other words, i' 
    will be a function of i, and j' a function of j).

    The parameter empty is a string which will be used if the cell with a given
    index does not exist in the original array (e.g. because it was ragged) or
    instead of any cell that holds an empty string (string of length 0)."""

    isize = len(arr)
    jsize = reduce(max, map(len, arr))
    trans_f = lambda n, m: [[empty for c in range(m) ] for r in range(n)]
    trans = trans_f(jsize, isize) if swap else trans_f(isize, jsize)

    for i in range(isize):
        for j in range(len(arr[i])):
            ni, nj = coord_trans(i, j, isize, jsize)
            #print "%s, %s\t%s, %s\t'%s'" % (i,j, ni, nj, arr[i][j])
            trans[ni][nj] = arr[i][j] if len(arr[i][j]) else empty

    return trans

_cw_coord_trans  = lambda i, j, n, m: (j, n-1-i)
_ccw_coord_trans = lambda i, j, n, m: (m-1-j, i)
_180_coord_trans = lambda i, j, n, m: (n-1-i, m-1-j)
_meh_coord_trans = lambda i, j, n, m: (i, j)
_flip_horz_trans = lambda i, j, n, m: (i, m-1-j)
_flip_vert_trans = lambda i, j, n, m: (n-1-i, j)
_flip_both_trans = lambda i, j, n, m: (n-1-i, m-1-j)

def parse(text, col_delim=COL_DELIM, row_delim=ROW_DELIM):
    """ Read a block of text and divide it according to the specified row and
    column delimiters to form a 2D array (a list of lists of strings)."""

    return [[c for c in r.split(col_delim)] for r in text.split(row_delim)]

def tostr(arr, col_delim=COL_DELIM, row_delim=ROW_DELIM, tp = PRINT_TPL):
    """ Create a string representation of a given 2D array using the specified
    delimiters to separate rows and columns.

    A template may be specified accoring to python string formating utilities 
    for all the cells to use. For instance, using tp='"%20s"' will create an 
    output string where each cell uses a minimum of 20 characters and is 
    surrounded by double quotes."""

    return row_delim.join(map(lambda c: col_delim.join([tp%f for f in c]), arr))

_C_CW, _C_CCW, _C_180, _C_VERT, _C_HORZ, _C_BOTH = range(6)

_C_MEH = None

_OPERATIONS = {
    _C_CW: rotate_clockwise,
    _C_CCW: rotate_counterclockwise,
    _C_180: rotate_180_degrees,
    _C_HORZ: flip_horizontal,
    _C_VERT: flip_vertical,
    _C_BOTH: flip_horizontal_and_vertical,
    _C_MEH: rotate_not_at_all,
}

if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    from sys import argv
    from os.path import basename

    # Prepare the parser.
    usage = '%s [OPTIONS]' % basename(argv[0])
    parser = OptionParser(usage=usage)

    # Prepare all the parse options that have to do with rotating the array.
    rotate = OptionGroup(parser, "Rotating")
    rotate.add_option('-c', '--clockwise', \
        action="store_const", dest="operation", const=_C_CW, \
        help='rotate the array clockwise (right).')
    rotate.add_option('-C', '--counter-clockwise', \
        action="store_const", dest="operation", const=_C_CCW, \
        help='rotate the array counter-clockwise (left).')
    rotate.add_option('-r', '--rotate-180', \
        action="store_const", dest="operation", const=_C_180, \
        help=u'rotate the array 180° - make it upside-down.')
    rotate.add_option('-m', '--meh', '--do-nothing', \
        action="store_const", dest="operation", const=_C_MEH, \
        help=u'rotate the array 0° - not at all.')
    parser.add_option_group(rotate)

    # Prepare all the parse options that have to do with flipping the array.
    flip = OptionGroup(parser, "Flipping (mirroring)")
    flip.add_option('-f', '--horizontal-flip', \
        action="store_const", dest="operation", const=_C_HORZ, \
        help='flip the array horizontally.')
    flip.add_option('-v', '--vertical-flip', \
        action="store_const", dest="operation", const=_C_VERT, \
        help='flip the array vertically.')
    flip.add_option('-b', '--horizontal-and-vertical-flip', \
        action="store_const", dest="operation", const=_C_BOTH, \
        help='flip the array both vertically and horizontally.')
    parser.add_option_group(flip)

    # Prepare all the parse options that have to do with delimiters used for
    # splitting the array on input and joining it back together on output.
    delims = OptionGroup(parser, "Delimiters")
    delims.add_option('-d', '--field-delimiter', \
        metavar='DELIM', dest="col_delim", default=COL_DELIM, \
        help='specify a field (column) delimiter instead of "%s".' % COL_DELIM)
    delims.add_option('-D', '--row-delimiter', \
        metavar='DELIM', dest="row_delim", default=ROW_DELIM, \
        help='specify a row delimiter instead of "%s".' % ROW_DELIM)
    parser.add_option_group(delims)

    # Assorted options, that have something vaguely to do with printing.
    printing = OptionGroup(parser, "Printing")
    printing.add_option('-s', '--print-template', \
        metavar='TEMPLATE', dest="print_tpl", default=PRINT_TPL, \
        help='set a sprintf-like template for cells, default: "%s"' % PRINT_TPL)
    printing.add_option('-e', '--empty-field-symbol', \
        metavar='STRING', dest="empty_sym", default=EMPTY_SYM, \
        help='set a string to use for empty cells instead of "%s".' % EMPTY_SYM)
    printing.add_option('-n', '--no-newline', \
        action="store_false", dest="newline", default=True, \
        help="do not append new line at the end of output.")
    parser.add_option_group(printing)

    opts, args = parser.parse_args()

    from sys import stdin, stdout
    
    # Read in an array from standard input in string form and normalize new
    # lines.
    input = '\n'.join(map(lambda s: s.strip('\n'), stdin))

    # Convert the string into an array, apply a transformation and the convert
    # the new array back into a string.
    arr = parse(input, opts.col_delim, opts.row_delim)
    arr = _OPERATIONS[opts.operation](arr, opts.empty_sym)
    str = tostr(arr, opts.col_delim, opts.row_delim, opts.print_tpl)

    # Write out the new array to standard output, possibly adding an extra line
    # at the end so it doesn't get glued to $PS1 (I hate when that happens).
    stdout.write(str + '\n' if opts.newline else str)

