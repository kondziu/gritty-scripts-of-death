#!/usr/bin/python
#
# Roman 
#
# A Roman numeral to-and-fro converter. 
#
# Parameters:
# 	-s | --subtractive		Represent four as IV, 2000 as (II), etc. (default)	
# 	-p | --positional		Represent four as IIII, 200 as MM, etc.
# 	-m | --mode=			Manually specify the mode of operation.
# 	-h | --usage			Print usage information (this).
#
# Author:
# 	Konrad Siek <konrad.siek@gmail.com>
#
# License:
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

def usage(program_name):
	print """USAGE:
	%s <OPTIONS> [ROMAN_NUMERAL [...]] [ARABIC_NUMERAL [...]]
OPTIONS:
	-s | --subtractive		Represent four as IV, 2000 as (II), etc. (default)	
	-p | --positional		Represent four as IIII, 200 as MM, etc.
	-m | --mode=			Manually specify the mode of operation.
 	-h | --usage			Print usage information (this).
	""" % program_name

class SYMBOLS:
	"""	Symbol alphabets for various modes of converter operation."""
	POSITIONAL = {
		'I': 1, 'II': 2, 'III': 3, 'IIII': 4,
		'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'VIIII': 9,
		'X': 10, 'XX': 20, 'XXX': 30, 'XXXX': 40,
		'L': 50, 'LX': 60, 'LXX': 70, 'LXXX': 80, 'LXXXX': 90,
		'C': 100, 'CC': 200, 'CCC': 300, 'CCCC': 400,
		'D': 500, 'DC': 600, 'DCC': 700, 'DCCC': 800, 'DCCCC': 900,
		'M': 1000, '': 0 
	}
	SUBTRACTIVE = {
		'I': 1, 'II': 2, 'III': 3, 'IV': 4, 
		'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 
		'X': 10, 'XX': 20, 'XXX': 30, 'XL': 40, 
		'L': 50, 'LX': 60, 'LXX': 70, 'LXXX': 80, 'XC': 90, 
		'C': 100, 'CC': 200, 'CCC': 300, 'CD': 400,
		'D': 500, 'DC': 600, 'DCC': 700, 'DCCC': 800, 'CM': 900, 
		'M': 1000, 'N': 0
	}
	BRACES = {
		'(': 3, ')': -3
	}

class MODES:
	""" Modes of converter operation, based on types of roman numeral notation.

	Subtractive notation is the more familiar mode of operation where a digit with
	a lower value L (limits apply) is placed in front of digit with a higher value
	H forming a combination with the value of H - L: e.g., 'I' has the value of 1 
	and 'V' has the value of 5, so 'IV' has the value of 5 - 1 = 4. This mode also
	uses parentheses to signify that he value of a number is multiplied by 1000: 
	e.g.: '(XI)' has the value of 11 * 1000 = 11000.

	Positional notation is the more natural and straightforward system, where each
	symbol is just multiplied to achieve any specific value. No subtractiv rules
	or multipliers apply: if you want to get 5000 in this system, it is necessary
	to write 'M', the symbol for 1000, five times: 'MMMMM'; similarily, if you
	want the value of 4, the symbol for 1 - 'I' - is written four times: 'IIII'.
	"""
	SUBTRACTIVE = 'subtractive'
	POSITIONAL = 'positional'

def parse(string, mode = MODES.SUBTRACTIVE):
	"""	Parse roman numeral in form of a string into an integer.
	
	The parser can run in two basic modes: subtractive or classical. 

	Subtractive mode (default) recognizes when I, X, or C are used before 
	V and X, L and C, or D and M, respectively, to indicate the second number
	is decreased by the value of the first number. It can also deal with
	parentheses indicating the surrounded number is multiplied 1000 times.

	Positional mode just adds up the values of encountered symbols, without
	any special cases considered. This is supposedly how the ancient Romans
	actually used the numerals.

	Parsing is done naively, without checking for proper order of the symbols.
	"""
	# Prep the string for parsing - turn in uppercase.
	string = string.upper()

	# Select parsing mode.
	alphabet = _select_alphabet(mode)
	modifiers = _select_modifiers(mode)
	all_symbols = _join_dicts(alphabet, modifiers)

	# Initial values of variables.
	total, modifier, index = 0, 0, 0
	max_length = _max_len(all_symbols)
	string_length = len(string)
	symbols = []

	# Main loop for the parser: cut out a fragment, match a symbol to it, convert
	# it to a numerical value and move to the next bit of the input string.
	while index < string_length:
		fragment = string[index:index+max_length]
		match = _find_match(fragment, all_symbols) 
		total, modifier = _find_value(total, modifier, match, alphabet, modifiers)
		symbols.append(match)
 		index += len(match)

	return total

def of_int(number, mode = MODES.SUBTRACTIVE, power = 3):
	# Init for input and output variables.
	alphabet = _reverse_dict(_select_alphabet(mode))
	modifiers = _reverse_dict(_select_modifiers(mode))
	symbols = []
	
	# If the whole thing is 0, then just serve the proper zero symbol.
	if number == 0:
		return alphabet[0] 

	# Numbers below zero are not supported.
	if number < 0:
		raise Exception('Cannot handle negative values')

	# Split the number into singles, tens, hundreds, and everything else.
	high_order, digits = _split(number, 10, power)
	
	# Take care of the part above the thousand.
	if high_order != 0:
		symbols += _process_high_order(high_order, mode, power, alphabet, modifiers)

	# Take care of the digits below the thousand.
	symbols += _process_digits(digits, alphabet)

	# Join and stringify.
	return ''.join(symbols)

def _process_digits(digits, alphabet):
	"""	Translate the single, ten, and thousand digits to roman numeral 
	symbols.
	"""
	symbols = []
	digits_length = len(digits)
	
	for i in range(0, digits_length):
		if digits[i] == 0:
			continue
		symbols.append(alphabet[10 ** (digits_length - i - 1) * digits[i]])

	return symbols

def _process_high_order(high_order, mode, power, alphabet, modifiers):
	"""	Process a number above 1000, scaled down to singles."""
	symbols = []

	# Whether the mode is specified as recurrent or not, append the proper 
	# symbols.
	if _is_recurrent(mode):
		symbols.append(modifiers[+power])
		symbols.append(of_int(high_order, mode, power))
		symbols.append(modifiers[-power])
	else:
		symbols.append(alphabet[10 ** power] * high_order)

	return symbols

def _select_alphabet(mode):
	"""	Select a specific alphabet for the given mode."""
	if mode == MODES.SUBTRACTIVE: 
		return SYMBOLS.SUBTRACTIVE
	elif mode == MODES.POSITIONAL:
		return SYMBOLS.POSITIONAL
	else:
		raise Exception("Unknown parser mode: " + mode)

def _select_modifiers(mode):
	"""	Select an alphabet of modifiers for the given mode."""
	if mode == MODES.SUBTRACTIVE: 
		return SYMBOLS.BRACES
	elif mode == MODES.POSITIONAL:
		return {} 
	else:
		raise Exception("Unknown parser mode: " + mode)

def _is_recurrent(mode):
	"""	Check if the specified mode is parsed using the recurrent parser."""
	if mode == MODES.SUBTRACTIVE: 
		return True 
	elif mode == MODES.POSITIONAL:
		return False
	else:
		raise Exception("Unknown parser mode: " + mode)

def _max_len(symbols):
	"""	Check the length of all symbols in the alphabet and find the maximum."""
	max = 0
	for symbol in symbols:
		length = len(symbol)
		if length > max:
			max = length
	return max

def _find_match(string, alphabet):
	"""	Find the longest symbol in the alphabet that the string starts with.
	
	If no symbol matches, the fragment is considered illegal and an exception is
	raised.
	"""
	match = ""
	length = 0
	for symbol in alphabet:
		if string.startswith(symbol) and len(symbol) > length:
			length = len(symbol)
			match = symbol
	if length == 0:
		raise Exception("Illegal symbol in fragment: " + string)		
	return match

def _split(number, digit_base, limit):
	"""	Split the number into individual digits according to the specified base up
	to three given limit (push any digits above the limit into a single number).
	"""
	above_limit = number / (digit_base ** limit)
	within_limit = number % (digit_base ** limit)
	digits = []
	for i in range(0, limit):
		power = digit_base ** (limit - i - 1)
		digits.append(within_limit / power)
		within_limit = within_limit % power
	return above_limit, digits

def _find_value(total, modifier, symbol, alphabet, modifiers):
	"""	Establish the new total and the new modifier value.
	
	If an unknown symbol is found, an exception is raised.
	"""
	if symbol in modifiers:
		return total, modifier + modifiers[symbol]
	elif symbol in alphabet:
		return total + 10**modifier * alphabet[symbol], modifier
	else:
		raise Exception("Unknown symbol: " + symbol)

def _join_dicts(dict_a, dict_b):
	"""	Add two dictionaries together."""
	dict_r = {}
	for a in dict_a:
		dict_r[a] = dict_a[a]
	for b in dict_b:
		dict_r[b] = dict_b[b]
	return dict_r

def _reverse_dict(dict):
	"""	Swap the keys of the dicionary with its values."""
	new_dict = {}
	for key, value in dict.items():
		new_dict[value] = key
	return new_dict

if __name__ == '__main__':
	# Packages necessary for commandline work.
	import sys
	from getopt import getopt

	# Read options and arguments.
	shorts = ['s', 'p', 'm:', 'h']
	longs = ['subtractive', 'positional', 'mode=', 'usage']
	opts, args = getopt(sys.argv[1:], ''.join(shorts), longs)

	# Set default values.

	# Process options.
	mode = MODES.SUBTRACTIVE
	for opt, param in opts:
		if opt in ['-s', '--subtractive']:
			mode = MODES.SUBTRACTIVE
		elif opt in ['-p', '--positional']:
			mode = MODES.POSITIONAL
		elif opt in ['-m', '--mode=']:
			mode = param
		elif opt in ['-h', '--usage']:
			usage(sys.argv[0])
		else:
			usage(sys.argv[0])
	
	# Process arguments. 
	for arg in args:
		#try:
			if arg.isdigit():
				print of_int(int(arg), mode)
			else:
				print parse(arg, mode)
		#except Exception as exception:
		#	print exception


