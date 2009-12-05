#!/usr/bin/python

class SYMBOLS:
	POSITIONAL = {
		'I': 1, 'II': 2, 'III': 3, 'IIII': 4,
		'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'VIIII': 9,
		'X': 10, 'XX': 20, 'XXX': 30, 'XXXX': 40,
		'L': 50, 'LX': 60, 'LXX': 70, 'LXXX': 80, 'LXXXX': 90,
		'C': 100, 'CC': 200, 'CCC': 300, 'CCCC': 400,
		'D': 500, 'DC': 600, 'DCC': 700, 'DCCC': 800, 'DCCCC': 900,
		'M': 1000 
	}
	SUBTRACTIVE = {
		'I': 1, 'II': 2, 'III': 3, 'IV': 4, 
		'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 
		'X': 10, 'XX': 20, 'XXX': 30, 'XL': 40, 
		'L': 50, 'LX': 60, 'LXX': 70, 'LXXX': 80, 'XC': 90, 
		'C': 100, 'CC': 200, 'CCC': 300, 'CD': 400,
		'D': 500, 'DC': 600, 'DCC': 700, 'DCCC': 800, 'CM': 900, 
		'M': 1000 
	}
	BRACES = {
		'(': 3, ')': -3
	}

class MODES:
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

	# Select parsing mode
	alphabet = _select_alphabet(mode)
	modifiers = _select_modifiers(mode)
	all_symbols = _join_dicts(alphabet, modifiers)

	# Initial values.
	total, modifier, index = 0, 0, 0
	max_length = _max_len(all_symbols)
	string_length = len(string)
	symbols = []

	# Main loop for the parser.
	while index < string_length:
		fragment = string[index:index+max_length]
		matches = _find_matches(fragment, all_symbols) 
		match, match_length = _find_best_match(matches)
		total, modifier = _find_value(total, modifier, match, alphabet, modifiers)
		symbols.append(match)
 		index += match_length

	# XXX print all_symbols
	# XXX print symbols, total, mode
	return total

def of_int(number, mode = MODES.SUBTRACTIVE):
	pass

def _select_alphabet(mode):
	if mode == MODES.SUBTRACTIVE: 
		return SYMBOLS.SUBTRACTIVE
	elif mode == MODES.POSITIONAL:
		return SYMBOLS.POSITIONAL
	else:
		raise Exception("Unknown parser mode: " + mode)

def _select_modifiers(mode):
	if mode == MODES.SUBTRACTIVE: 
		return SYMBOLS.BRACES
	elif mode == MODES.POSITIONAL:
		return []
	else:
		raise Exception("Unknown parser mode: " + mode)

def _max_len(symbols):
	max = 0
	for symbol in symbols:
		length = len(symbol)
		if length > max:
			max = length
	return max

def _find_matches(string, alphabet):
	matches = []
	for symbol in alphabet:
		if string.startswith(symbol):
			matches.append(symbol)
	if matches == []:
		raise Exception("Illegal symbol in fragment: " + string)		
	return matches

def _find_best_match(matches):
	best_match = ""
	best_match_length = 0
	for match in matches:
		match_length = len(match)
		if match_length > best_match_length:
			best_match = match
			best_match_length = match_length
	return best_match, best_match_length

def _find_value(total, modifier, symbol, alphabet, modifiers):
	if symbol in modifiers:
		return total, modifier + modifiers[symbol]
	elif symbol in alphabet:
		return total + 10**modifier * alphabet[symbol], modifier
	else:
		raise Exception("Unknown symbol: " + symbol)

def _join_dicts(dict_a, dict_b):
	dict_r = {}
	for a in dict_a:
		dict_r[a] = dict_a[a]
	for b in dict_b:
		dict_r[b] = dict_b[b]
	return dict_r

if __name__ == '__main__':
	print parse('MDCCCCLXXXIIII', MODES.POSITIONAL)
