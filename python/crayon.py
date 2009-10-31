#!/usr/bin/python
#
# Crayon
#
# A simple script to color your text and wotnot. This basically uses 
# \033-type sequences and color codes that may or may not work with your 
# shell.
#
# Parameters:
# 	-s STYLE | --style=STYLE		Specify a style (see list below).
# 	-c COLOR | --color=COLOR		Specify a color (see list below).
# 	-b COLOR | --background=COLOR	Specify a color (see list below).
# 	-k | --keep-style		Do not reset styles after echo-ing.
# 	-d | --default			Reset settings.
# 	-n | --no-newline		Do not append a new line to the result.
# 	-r | --raw				Print control sequences without applying them.
# 	-h | --help				Print usage information (this).
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

import sys
from getopt import getopt

# Styles.
BOLD = 1
UNDERLINE = 4
BLINK = 5
REVERSE = 7
CONCEALED = 8

# Colors.
BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7

# Color string to code map.
COLORS = {
	'black': BLACK,
	'red': RED,
	'green': GREEN,
	'yellow': YELLOW,
	'blue': BLUE,
	'magenta': MAGENTA,
	'cyan': CYAN,
	'white': WHITE,
}

# Style to string map.
STYLES = {
	'bold': BOLD,
	'underline': UNDERLINE,
	'blink': BLINK,
	'reverse': REVERSE,
	'concealed': CONCEALED,
}

def escape(string):
	r"""Change the \033 character to its sring representation."""
	return string.replace('\033', '\\033')

def command(c):
	"""Add the command character sequence to the specified code."""
	return '\033[%sm' % c

def style(s):
	"""Apply the given code as a style command sequence."""
	return command(s)

def fg(c):
	"""Apply the given code as a foreground color command sequence."""
	return command(30 + c)

def bg(c):
	"""Apply the given code as a background color command sequence."""
	return command(40 + c)

def default():
	"""Apply an empty command sequence - reset setting to default."""
	return command('')

def echo(style, out = sys.stdout):
	"""Print out the string to standard output or some other stream."""
	out.write(style)

def color_of_str(s):
	"""Translate the string to a color code."""
	if s.isdigit() and int(s) in COLORS.values():
		return int(s)
	if s.lower() in COLORS:
		return COLORS[s.lower()]
	raise Exception("Unrecognized color: %s" % s);

def style_of_str(s):
	"""Translate the string to a string code."""
	if s.isdigit() and int(s) in STYLES.values():
		return int(s)
	if s.lower() in STYLES:
		return STYLES[s.lower()]
	raise Exception("Unrecognized style: %s" % s);
	
def usage(command_name):
	"""Print script usage information."""
	print 'Usage: %s [OPTIONS] TEXT' % command_name
	print 'Options:'
	shorts = ['s:', 'c:', 'b:', 'r', 'd', 'h', 'k', 'n']
	longs = [
		'style=', 'color=', 'background=', 'keep-style', 
		'default', 'help=', 'raw', 'no-newline'
	]
	print "\t-s STYLE | --style=STYLE\tSpecify a style (see list below)." 
	print "\t-c COLOR | --color=COLOR\tSpecify a color (see list below)."
	print "\t-b COLOR | --background=COLOR\tSpecify a color (see list below)."
	print "\t-k | --keep-style\t\tDo not reset styles after echo-ing."
	print "\t-d | --default\t\t\tReset settings."
	print "\t-n | --no-newline\t\tDo not append a new line to the result."
	print "\t-r | --raw\t\t\tPrint control sequences without applying them."
	print "\t-h | --help\t\t\tPrint usage information (this)."
	print "Styles (use either names or codes):"
	for style in STYLES.items():
		print "\t%s - %s\t" % style
	print "Colors (use either names or codes):"
	for color in COLORS.items():
		print "\t%s - %s\t" % color

if __name__ == '__main__':
	shorts = ['s:', 'c:', 'b:', 'r', 'd', 'h', 'k', 'n']
	longs = [
		'style=', 'color=', 'background=', 'keep-style', 
		'default', 'help', 'raw', 'no-newline'
	]
	
	opts, args = getopt(sys.argv[1:], ''.join(shorts), longs)

	prefix = ''
	postfix = default()
	raw = False
	newline = True

	for opt in opts:
		if opt[0] in ['-c', '--color']:
			prefix += fg(color_of_str(opt[1]))
		elif opt[0] in ['-b', '--background']:
			prefix += bg(color_of_str(opt[1]))
		elif opt[0] in ['-s', '--style']:
			prefix += style(style_of_str(opt[1]))
		elif opt[0] in ['-k', '--keep-style']:
			postfix = ''
		elif opt[0] in ['-r', '--raw']:
			raw = True
		elif opt[0] in ['-d', '--default']:
			prefix = default()
			postfix = ''
		elif opt[0] in ['-n', '--no-newline']:
			newline = False
		else:
			usage(sys.argv[0])
			sys.exit(1)
		
	string = prefix + ' '.join(args) + postfix
	if raw:
		string = escape(string)
	if newline:
		string += "\n"
	echo(string)
