#!/usr/bin/python
#
# Craziest
#
# A script to find all legal Scrabble words that can be made using some list 
# of letters and a dictionary of all legal words, and sort the output by the
# total score of each word.
#
# Parameters:
# 	-m, --min-length=			Specify the minimum length of a word.
# 	-M, --max-length=			Specify the maximum length of a word.
# 	-d, --dictionary-command=	Provide a command that gives the list
# 															of correct words.
# 	-D, --dictionary-file=		Provide a file with the list of correct words.
# 	-a, --alphabet=				Specify available letters and their weights.
# 	-n, --no-scores				Do not display word scores.
# 	-b, --blank-symbol=			Define the symbol used to represent a blank.
# 	-h, --usage					Command usage information.
#
# Author:
# 	Konrad Siek
#
# License
# 	Copyright 2008 Konrad Siek 
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

SCORES = {
	'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
	'I': 1, 'J': 8, 'K': 5, 'L': 1,	'M': 3,	'N': 1,	'O': 1,	'P': 3,
	'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
	'Y': 4, 'Z': 10,
}

def usage(program):
	"""	Print the usage information."""
	print """Usage:	%s [OPTIONS] LETTERS [, ...]' 
OPTIONS
	-m, --min-length=			Specify the minimum length of a word.
	-M, --max-length=			Specify the maximum length of a word.
	-d, --dictionary-command=	Provide a command that gives the list 
															of correct words.
	-D, --dictionary-file=		Provide a file with the list of correct words.
	-a, --alphabet=				Specify available letters and their weights.
	-n, --no-scores				Do not display word scores.
	-b, --blank-symbol=			Define the symbol used to represent a blank.
	-h, --usage					Command usage information.
	""" % program	

class AspellDictionary:
	def __init__(self, command='aspell dump master', keep_capitals = False):
		"""	Create an instance of the dictionary using a command."""
		import commands
		self.words = set([])
		for word in commands.getoutput(command).split():
			if len(word) > 0 and word[0].islower():
				self.words.add(word.upper())

class FileDictionary:
	def __init__(self, path, keep_capitals = False):
		"""	Create a dictionary from a file."""
		self.words = set([])
		for line in file(path).readlines():
			for word in line.split():
				if len(word) > 0 and word[0].islower():
					self.words.add(word.upper())

def read_scores(path):
	"""	Read a list of available letters and their scores from a file."""
	score = {}
	for line in file(path).readlines():
		letter, value = line.split(None, 1)
		score[letter.upper()] = int(value)
	return score

def create_words(letters, dictionary, min_length=2, max_length=8):
	"""	Create a list of all possible words that can be created from the given
	list of letters. All the words will be correct according to the provided
	dictionary.
	"""
	from itertools import permutations
	possible_words = set([])
	for length in range(min_length, max_length + 1):
		for permutation in permutations(letters, length):
			possible_words.add("".join(permutation).upper())
	return dictionary.words.intersection(possible_words)

def weigh_word(word, scores):
	""" Add the score of each letter to produce the score of the word."""
	sum = 0
	for letter in word:
		sum += scores[letter]
	return sum

def expand_blanks(word, blank_symbol = '?', letters = SCORES.keys()):
	""" Expand the symbol representing a blank into all possible letters."""
	if word.find(blank_symbol) < 0:
		return [word]
	from itertools import permutations
	words = []
	template = word.replace(blank_symbol, "%s")
	for tuple in permutations(letters, word.count(blank_symbol)):
		 words.append(template % tuple)		
	return words

def generate(argument, dictionary, min_length, max_length, blank, scores):
	"""	Generate a list of possible words."""
	words = set([])
	for expanded_set in expand_blanks(argument, blank, scores.keys()):
		word_list = create_words(expanded_set, dictionary, min_length, max_length)
		word_set = set(word_list)
		words = words.union(word_set)
	return words

def weigh(words, scores = SCORES):
	"""	Add scores to the words in the list."""
	weighed_words = []
	for word in words:
		weighed_words.append((weigh_word(word, scores), word))
	weighed_words.sort(None, None, True)
	return weighed_words

def printout(weighed_words, show_weights = True):
	"""	Print out the list of words."""
	if show_weights:
		for pair in weighed_words:
			print "%-4s\t%s" % pair
	else:
		for _, word in weighed_words:
			print word

if __name__ == '__main__':
	import sys
	from getopt import getopt
	
	# Default values for parameters.
	dictionary = AspellDictionary()
	min_length, max_length = (2, 7)
	blank_symbol = '?'
	show_scores = True
	scores = SCORES
	
	# Definitions of switches.
	shorts = [ 'm:', 'M:', 'd:', 'D:', 'h', 'n', 'b:', 'a:']
	longs = [
		'min-length=', 'max-length=', 'dictionary-command=',
		'dicionary-file=', 'usage', 'no-scores', 'blank-symbol=',
		'alphabet='
	] 

	# Process user-supplied commandline parameters.
	opts, args = getopt(sys.argv[1:], ''.join(shorts), longs)
	for opt in opts:
		if opt[0] in ['-m', '--min-length']:
			min_length = int(opt[1])
		elif opt[0] in ['-M', '--max-length']:
			max_length = int(opt[1])
		elif opt[0] in ['-d', '--dictionary-command']:
			dictionary = AspellDicionary(opt[1])
		elif opt[0] in ['-D', '--dictionary-file']:
			dictionary = FileDictionary(opt[1])
		elif opt[0] in ['-a', '--alphabet']:
			scores = read_scores(opt[1])
		elif opt[0] in ['-b', '--blank-symbol']:
			blank_symbol = opt[1]
		elif opt[0] in ['-n', '--no-scores']:
			show_scores = False
		elif opt[0] in ['-h', '--usage']:
			usage(sys.argv[0])
			sys.exit(0)
		else:
			usage(sys.argv[0])
			sys.exit(1)
	
	# Process each of the aguments.
	for argument in args:
		words = generate(
			argument, dictionary, min_length, max_length, blank_symbol, scores
		)
		weighed_words = weigh(words, scores)
		printout(weighed_words, show_scores)

