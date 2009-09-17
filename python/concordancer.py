#!/usr/bin/python
#
# Concordancer
# 
# A script for finding concordances for given keywords in the 
# specified text.
# 
# A concordance is a keyword with its context (here, the closest 
# n words), a combination used, for instance, in lexicography to
# deduce the meaning of the keyword based on the way it is used
# in text.
#
# Parameters:
# 	c - the number of words that surround a keyword in context
# 	p - the string that is stuck in front of keywords
# 	s - the string that is stuck at the ends of keywords
# 	d - formatting of the display,
# 		'simple' - one concordance per line (default)
# 		'group' - group concordances by keywords	 
#	
# Example:
# 	to find concordances for the word 'list' in the bash manual:
# 		man bash | concordancer.py arguments options
#
# Author:
# 	Konrad Siek <konrad.siek@gmail.com>
#
# License:
#
# Copyright 2008 Konrad Siek 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Imports.
import getopt
import sys

# Option sigils - the characters associated with various options. 
CONTEXT_SIZE = 'c'
PREFIX = 'p'
SUFFIX = 's'
DISPLAY = 'd'

# Option default values, represented as a map for convenience.
OPTIONS = {\
	CONTEXT_SIZE: str(5), \
	PREFIX: '*', \
	SUFFIX: '*', \
	DISPLAY: 'simple'\
}

# Character constants, also for convenience.
EMPTY=""
SPACE = " "
NEWLINE = "\n"
TAB = "\t"
COLON = ":"
SWITCH = "-"

def display_help(program_name):
	"""	Display usage information.

	@param program_name - the name of the script"""

	help_string = \
	"""Usage:
    %s [OPTION] ... [WORD] ...
Options:
    %s    the number of words that surround a keyword in context
    %s    the string that is stuck in front of keywords
    %s    the string that is stuck at the ends of keywords
    %s    formatting of the display,
        'simple' - one concordance per line (default)
        'group' - group concordances by keywords
Words:
	The list of words that concordances will be searched for. If
	no list is provided, a complete concordance is made - that is,
	one using all input words.""" \
	% (program_name, CONTEXT_SIZE, PREFIX, SUFFIX, DISPLAY)
	print(help_string)

def find_concordances(keywords, words, context_size):
	"""	Finds concordances for keywords in a list of input words.

	@param keywords - list of keywords,
	@param words - input text as a list of words
	@param context_size - number of words that should surround a keyword
	@return list of concordances"""

	# Initialize the concordance map with empty lists, for each keyword.
	concordances = prep_concordance_map(keywords)

	# If any word in the text matches a keyword, create a concordance.	
	for i in range(0, len(words)):
		for keyword in keywords:
			if matches(keyword, words[i]):
				concordance = form_concordance(words, i, context_size)
				concordances[keyword].append(concordance)
	
	return concordances

def find_all_concordances(words, context_size):
	""" Make a complete concordance - assume all words match.

	@param words - input text as a list of words
	@param context_size - number of words that should surround a keyword
	@return list of concordances"""

	concordances = {}

	for i in range(0, len(words)):
		word = words[i]
		if word not in concordances:
			concordances[word] = []
		concordance = form_concordance(words, i, context_size)
		concordances[word].append(concordance)

	return concordances 

def print_concordances(concordances, simple, prefix, suffix):
	"""	Print the concordances to screen.

	@param concordances - list of concordances to display
	@param simple - True: display only concordances, False: group by keywords
	@param prefix - prefix to keywords
	@param suffix - suffix to keywords"""

	# For each concordance, mark the keywords in the sentence and print it out.
	for keyword in concordances:
		if not simple:
			sys.stdout.write(prefix + keyword + suffix + COLON + NEWLINE)
		for words in concordances[keyword]:		
			if not simple:
				sys.stdout.write(TAB)
			for i in range(0, len(words)):
				if matches(keyword, words[i]): 
					sys.stdout.write(prefix + words[i] + suffix)
				else:
					sys.stdout.write(words[i])
				if i < len(words) - 1:
					sys.stdout.write(SPACE)
				else:
					sys.stdout.write(NEWLINE)

def prep_concordance_map(dict_words):
	"""	Prepare a map with keywords as keys and empty lists as values.

	@param dict_words - list of keywords"""

	# Put an empty list value for each keyword as key.
	concordances = {}
	for word in dict_words:
		concordances[word] = []

	return concordances

def matches(word_a, word_b):
	""" Case insensitive string equivalence.

	@param word_a - first string
	@param word_b - second string (duh)
	@return True or False""" 

	return word_a.lower() == word_b.lower()

def form_concordance(words, occurance, context_size):
	"""	Creates a concordance.

	@param words - list of all input words
	@param occurance - index of keyword in input list
	@param context_size - number of preceding and following words
	@return a sublist of the input words"""

	start = occurance - context_size
	if start < 0:
		start = 0

	return words[start : occurance + context_size + 1]

def read_stdin():
	"""	Read everything from standard input as a list.
	
	@return list of strings"""

	words = []
	for line in sys.stdin:
		# Add all elements returned by function to words.
		words.extend(line.split())

	return words

def read_option(key, options, default):
	""" Get an option from a map, or use a default.
	
	@param key - option key
	@param options - option map
	@param default - default value, used if the map does not contain that key
	@return value from the map or default"""

	for option, value in options:
		if (option == SWITCH + key):
			return value

	return default

def get_configuration(arguments):
	"""	Retrieve the entire configuration of the script.
	
	@param arguments - script runtime parameters
	@return map of options with defaults included
	@return list of arguments (keywords)
	@return list of words from standard input"""

	# All possible option sigils are concatenated into an option string.
	option_string = EMPTY.join([("%s" + COLON) % i for i in OPTIONS.keys()])
	# Read all the options.
	options, arguments = getopt.getopt(arguments, option_string)

	# Apply default values if no values were set.
	fixed_options = {}
	for key in OPTIONS.keys():
		fixed_options[key] = read_option(key, options, OPTIONS[key])

	# Read the list of words at standard input.
	input = read_stdin()

	return (fixed_options, arguments, input)

def process(options, arguments, input):
	"""	The main function.
	 
	@param options - map of options with defaults included
	@param arguments - list of arguments (keywords)
	@param input - list of words from standard input"""

	# Extract some key option values.
	context_size = int(options[CONTEXT_SIZE])
	simple = options[DISPLAY] == OPTIONS[DISPLAY]

	# Conduct main processing - find the concordances.
	concordances = {}
	if arguments == []:
		# If no arguments are specified, construct a concordance for all 
		# possible keywords.
		concordances = find_all_concordances(input, context_size)
	else:
		# And if there are,make a concordance for only those words.
		concordances = find_concordances(arguments, input, context_size)

	# Display the results.
	print_concordances(concordances, simple, options[PREFIX], options[SUFFIX])

# The processing starts here.
if __name__ == '__main__':
	# Read all user-supplied information.
	options, arguments, input = get_configuration(sys.argv[1:])
	
	# The configuration is not full - display usage information.
	if arguments == [] and input == []:
		display_help(sys.argv[0])
		exit(1)

	# If evverything is in order, start concordancing.
	process(options, arguments, input)
	
# The processing starts here.
#if __name__ == '__main__':
#	if len(sys.argv) == 1:
#		display_help(sys.argv[0])
#	else:
#		process(sys.argv[1:])

