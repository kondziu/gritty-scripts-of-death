#!/usr/bin/env python
#
# Duplicates
#
# A quick and simple script to find files in a directory which have the same
# contents as one another. A hash of each files' contents is created and 
# compared against one another to find identical files. When hashes match the
# files' contents are compared bit-by-bit. The script then prints out groups of
# files which have the same contents.
#
# Options:
#   -h, --help            show this help message and exit
#   --paragraphs          Print out final results as paragraphs, where each line
#                         is filename, and each group of identical files is
#                         separated from another by an empty line.
#   -f FIELD, --field-separator=FIELD
#                         Print out identical files separated from one another
#                         by the specified string. Uses system path separator by
#                         default.
#   -g GROUP, --group-separator=GROUP
#                         Print out groups of identical files separated from one
#                         another by the specified string. Uses new lines by
#                         default.
#   -v, --verbose         Show more diagnostic messages (none - only errors and
#                         final results, once [-v] - duplicate messages, twice
#                         [-vv] - matching hash messages, four times [-vvvv] -
#                         all possible diagnostic messages.
#   --hash-only           Do not compare duplicate files bit-by-bit if hashes
#                         match
#   --non-recursive       Only look through the files in the directory but do
#                         not descend into subdirectories.
#
# Example:
#   This is how you go about checking if Steve has any duplicated files in his
#   home directory:
#       ./duplicates.py /home/steve
#
# License:
#   Copyright (C) 2010 Konrad Siek <konrad.siek@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it 
#   under the terms of the GNU General Public License version 3, as published 
#   by the Free Software Foundation.
# 
#   This program is distributed in the hope that it will be useful, but 
#   WITHOUT ANY WARRANTY; without even the implied warranties of 
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#   PURPOSE.  See the GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License along 
#   with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, sys

# Levels of verbocity:
#   * results - print out the final results formatted as specified by the user,
#   * errors - show final results and messages from any errors that occur,
#   * duplicate - print out a message every time a duplicate is found,
#   * hash - print out an information every time two hashes match
#   * all - show all diagnostic messages possible (a lot of text, this)
SHOW_RESULTS, SHOW_ERRORS, SHOW_DUPLICATE, SHOW_HASH, SHOW_ALL = range(-1,4)

# The selected level of verbosity will be stored here.
global verbosity

def printerr(level, *args):
    """ Print an error message if the specified level of verbosity allow it."""
    if level > verbosity:
        return
    from sys import argv, stderr
    from os.path import basename
    stderr.write("%s:" % basename(argv[0]))
    for arg in args:
        stderr.write(" %s" % arg)
    stderr.write("\n")
    
def listall(root, recursive=True):
    """ Traverse a file tree and list all files therein."""
    from os import listdir
    from os.path import isdir, abspath, exists, join
    files = []
    todo = [abspath(root)]
    while todo:
        path = todo.pop()
        printerr(SHOW_ALL, 'Found file:', "'%s'" % path)
        if not isdir(path):
            files.append(path)
            continue
        contents = [join(path, file) for file in listdir(path)]
        todo += contents if recursive else filter(lambda f: not isdir(f), contents)
    return files

def same_file(data_a, data_b):
    """ Compare the contents of two files bit by bit."""
    len_a = len(data_a)
    len_b = len(data_b)
    if len_a !=  len_b:
        return False
    for i in range(0, len_a):
        if data_a[i] != data_b[i]:
            return False
    return True

def duplicates(paths, onlyhashes=False):
    """ For each file in a list of files find its duplicates in that list. A 
    duplicate of file is such that has the same contents. The files are compared
    first by hashes of its contents and if those match, bit by bit (although the
    latter can be turned off for a performance increase."""
    from hashlib import md5
    hashes = {}
    duplicates = []
    for path in paths:
        printerr(SHOW_ALL, 'Looking for duplicates for', "'%s'" % path)
        data = open(path, 'rb').read()
        hash = md5(data).digest()
        if hash in hashes:
            other_paths = hashes[hash]
            printerr(SHOW_HASH, 'Hash of ', "'%s'" % path, \
                'matches has of ', "'%s'" % other_paths)
            duplicated = False
            for other_path in other_paths:
                # If only hashes are supposed to be taken into account, then
                # assume this file is a duplicate and do not process further.
                if onlyhashes:
                    duplicates.append((other_path, path))
                    duplicated = True
                    break
                other_data = open(other_path, 'rb').read()
                # Check if files are different despite having the same hash.
                if same_file(data, other_data):
                    printerr(SHOW_DUPLICATE, 'Found duplicates: \
                        '"'%s'" % path, 'and', "'%s'" % other_path)
                    duplicates.append((other_path, path))
                    duplicated = True
            if not duplicated:
                # Same hash but different content.
                printerr(SHOW_HASH, 'No duplicate found for', "'%s'" % path)
                hashes[hash].append(path)
        else:
            # No matching hash.
            printerr(SHOW_ALL, 'No duplicate found for', "'%s'" % path)
            hashes[hash] = [path]
    return duplicates

def sort(duplicates):
    """ Organize pairs of duplicates into groups (sets)."""
    sorts = []
    for duplicate_a, duplicate_b in duplicates:
        for sort in sorts:
            if duplicate_a in sort or duplicate_b in sort:
                sort.add(duplicate_a)
                sort.add(duplicate_b)
                break
        else:
            sorts.append(set([duplicate_a, duplicate_b]))
    return sorts

def print_results(sorts, separator=os.pathsep, group_separator="\n"):
    """ Print out sets of results, where each element of a set is one field,
    separated from others by a field separator, and each set is a record or 
    group, separated from other groups by a group separator."""
    
    from sys import stdout
    for sort in sorts:
        first = True
        for s in sort:
            if not first:
                stdout.write(separator)
            stdout.write(s)
            first = False
        stdout.write(group_separator)

if __name__ == '__main__':
    """ The main function: argument handling and all processing start here."""
    
    from optparse import OptionParser
    from os.path import basename
    from sys import argv

    # Prepare user options.
    usage = '\n%s [OPTIONS] PATH_LIST ' % basename(argv[0])

    description = 'Looks through the specified directory or directories ' + \
        'for duplicated files. Files are compared primarily by a hash ' + \
        'created from their contents, and if there\'s a hit, they are ' + \
        'compared bit-by-bit to ensure correctness.'

    parser = OptionParser(usage=usage, description=description)
    
    parser.add_option('--paragraphs', action='store_true', dest='paragraphs', \
        help='Print out final results as paragraphs, where each line is ' + \
        'filename, and each group of identical files is separated from ' + \
        'another by an empty line.', default=False)
    parser.add_option('-f', '--field-separator', action='store', dest='field', \
        help='Print out identical files separated from one another by the ' + \
        'specified string. Uses system path separator by default.', \
        default=os.pathsep)
    parser.add_option('-g', '--group-separator', action='store', dest='group', \
        help='Print out groups of identical files separated from one ' + \
        'another by the specified string. Uses new lines by default.', \
        default='\n')
    parser.add_option('-v', '--verbose', action='count', dest='verbosity', \
        help='Show more diagnostic messages (none - only errors and final ' + \
        'results, once [-v] - duplicate messages, twice [-vv] - matching ' + \
        'hash messages, four times [-vvvv] - all possible diagnostic messages.')
    parser.add_option('--hash-only', action='store_true', dest='hashonly', \
        help='Do not compare duplicate files bit-by-bit if hashes match', \
        default=False)
    parser.add_option('--non-recursive', action='store_false', dest='recursive', \
        help='Only look through the files in the directory but do not ' + \
        'descend into subdirectories.', default=True)

    # Gathering option information
    opts, args = parser.parse_args()
    if opts.paragraphs:
        opts.field = '\n'
        opts.group = '\n\n'
    verbosity = opts.verbosity

    if len(argv) == 1: 
        parser.print_help()
        sys.exit(1)

    # Processing.
    files = []
    for arg in args:
        printerr(SHOW_ALL, 'Reading file tree under %s%s' \
            % (arg, 'recursively' if opts.recursive else ''))
        files += listall(arg, opts.recursive)
    sorts = sort(duplicates(files, opts.hashonly))
    print_results(sorts, separator=opts.field, group_separator=opts.group)


