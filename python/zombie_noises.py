#!/usr/bin/python
 
# Copyright 2009 Konrad Siek.
# 
# This program is free software: you can redistribute it and/
# or modify it under the terms of the GNU General Public 
# License as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later 
# version.
# 
# This program is distributed in the hope that it will be 
# useful, but WITHOUT ANY WARRANTY; without even the implied 
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the GNU General Public License for more 
# details.
# 
# You should have received a copy of the GNU General Public 
# License along with this program. If not, see 
# <http://www.gnu.org/licenses/>. 

import sys
import time
import getopt
import random

# A list of generic noises for the zombie to use when nothing
# else is available, i.e., when there was no input.
GENERIC_NOISES = [
    'braaaains', 'coooffeee', 
    ':grunt:', ':groan:',  
    ':gurgle:', ':burp:', ':moan:'
]

# Characters that are easy for the zombie to elongate when 
# speaking, as 'a' in 'braaaains'.
ELONGATABLE = [
    'a', 'e', 'i', 'o', 'u', 'y', 'r', 's', 
    'A', 'E', 'I', 'O', 'U', 'Y', 'R', 'S',
    '!'
]

# Maximum number of allowed repeated characters.
MAX_ELONGATION = 6

# Characters which zombies make an effort to reproduce but 
# sometimes fail. Or maybe they do it for the slurrin effect.
# It's sometimes hard to tell with zombies.
SUBSTITUTABLE = {
    'n': 'ngh',   'N': 'NGH',
    'k': 'kh',   'K': 'KH',
    'g': 'gh',   'G': 'GH',
    '?': '!'
}

# Characters which zombies have trouble pronuning, so they 
# tend to drop them altogether. This is mostly punctuation.
REMOVABLE = [ 
    '.', ',', ';', '-',   '@', '#', '$', '%',
    '^', '&', '*', '(',   ')', '_', '+', '=',
    '{', '}', '[', ']',   ':', '"', '\', ''', 
    '|', '<', '>', '/',   '`', '~'      
]

# The odds deciding the chance of a character being mangled
# by a zombie. The higher the value of the second part, the 
# *less* likely the zombie is to touch a given character. The
# higher the value of the first part, the *more* likely the 
# zombie is to touch a given character. The value of one to 
# one will cause all opportunities to mangle to be utilized.
# The suggestion here, is to use values generally close to 
# one, especially in conversation mode.
ODD_FACTOR = (3, 4)

# Prompts used for interactive mode to represent the user's 
# input to the conversation and the zombie's reponses.
USER_PROMPT = 'You: '
ZOMBIE_PROMPT = 'Zombie: '

# Message used for interactive mode to indicate the time when
# the zombie is cogitating.
ZOMBIE_THINKS = "(zombie thinks)"

# The maximum amount of time for the zombie to conjure a
# response, mesaured in seconds. Should be greater or equal to
# one.
THINK_TIME = 6

# A dictionary to all the characters with manglers appropriate
# for their class. Intentionally left empty. This will fill up 
# later automatically. 
MANGLERS = {}

def zombify(string):
    """ Throughputs a string through a zombie producing a 
        mangled and more interesting alternative to the
        original input. 
 
        A certain class of characters can be removed, some 
        characters can be multiplied and some can be 
        substituted for other characters or phrases. And when 
        the input is empty, a random noise can be made.
 
        @param string before a zombie mangles it.
 
        @return string after a zombie mangles it.
    """
    # If there's nothing in the line, then there's an
    # opportunity to insert a generic word here. This is a
    # high-probability event, because we like zombies to say
    # 'braaaains' and ':grunt:' a lot.
    if len(string.strip()) == 0:
        if lottery():
            return random.choice(GENERIC_NOISES) + "\n"
        else:
            return string

    # Check out each character now, and try to apply some 
    # gruesome mangling to them, if odds allow. This is a 
    # typical probability event and uses odds. Also, if 
    # there is no mangler available for use, just ignore the 
    # character - opportunity wasted.
    result = ""
    for character in string:
        if lottery() and character in MANGLERS:
            # Select the appropriate class for the character
            # and use the function appropriate for that class.
            mangler = MANGLERS[character]
            result += mangler(character)
        else:
            result += character
    return result

def elongate(character):
    """ Elongate a character or string a random number of
        times.
        
        @param character to elongate.
        
        @return elongated string of characters.
    """
    return random.randint(2, MAX_ELONGATION) * character

def remove(character):
    """ Ignore a character.
        
        @param character to ignore.
        
        @return empty string.
    """
    return ''

def substitute(character):
    """ Replace a character with the defined substitution. 
        
        @throw in case the substitution is not present throw 
        a KeyError exception.
        
        @param character to replace with a string.
        
        @return replacement string.
    """
    return SUBSTITUTABLE[character]

def lottery():
    """ A simple binary lottery, with odds of success equal 
        to ODD_FACTORY[0] in ODD_FACTOR[1].
        
        @return either True or False, in a random fashion.
    """
    return random.randint(ODD_FACTOR[0], ODD_FACTOR[1]) \
            in range(1, ODD_FACTOR[0] + 1)

def handle_pipe():
    """ Zombify individual lines, one by one, so a file or
        on-the-fly input can be processed. A method to work
        with large input.
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always True.
    """
    for line in sys.stdin:
        line = zombify(line)
        sys.stdout.write(line)
    sys.stdout.write("\n") 

    return True

def handle_interactive():
    """ Zombify input in a form of conversation with the
        user, with an additional effect of simulating a zombie
        in the process of conceptualizing. That process could 
        take a bit of time, so there is a delay introduced.
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always True.
    """
    # Secure in case amodifying user does not understand the 
    # concept of 'greater or equal'.
    if THINK_TIME < 1:
        sys.stderr.write("THINK_TIME, must be at least 1")
        return True
    
    # Continue conversation endlessly!
    while True:
        try:
            line = raw_input(USER_PROMPT)
            print(ZOMBIE_THINKS)
            think_time = random.randint(1, THINK_TIME)
            time.sleep(think_time) 
            response = zombify(line)
            print(ZOMBIE_PROMPT + response)
        except:
            print
            break

    return True

def handle_file(path):
    """ Zombify input taken directly from a named file. The
        file is processed one line after another and the 
        output is directed to stdout. It's a sort of batch-
        -processed zombie then.
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always False, unless an error appears, then True.
    """
    try:
        input_file = open(path)
        for line in input_file:
            line = zombify(line)
            sys.stdout.write(line)
        sys.stdout.write("\n")
    except:
        sys.stderr.write("Cannot open file: " + path + "\n"); 
        return True
    
    return False

def handle_word(word):
    """ Zombify a single word and continue processing. This 
        can be used in conjunction with other command, 
        although I can't imagine what for. 
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always False.
    """
    word = zombify(word)
    sys.stdout.write(word)
    sys.stdout.write("\n") 

    return False

def handle_params(params):
    """ Zombify all the parameters as individual lines. It's 
        the zombie's way of making fun of you typing in 
        incorrect parameters. This is also a way to work with
        the program arguments vector as input, if you want to
        do it that way.
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always True.
    """
    for param in params:
        param = zombify(param)
        sys.stdout.write(param)
        sys.stdout.write("\n") 

    return True

def print_usage():
    """ Prints usage information for the program.
 
        @return Generally, True if the processing should be 
        stopped afterwards and False if it should go on. Here,
        always False.
    """
    print(\
 """Usage:
    zombie_noises.py [parameters]
    
 Parameters:
    -p  process standard input (default for no parameters)
    -i  converse interactively
    -f  {filename}  process file (and continue)
    -w  {word}      process words (and continue)
    -h  show usage screen (and continue)
        
 Author:
    Konrad Siek <konrad.siek@gmail.com>
 
 License: 
    GNU General Public License
 """\
    )

    return False

def resolve_opts(opt_handlers, def_handler, arg_handler):
    """ Handles all the options and parameters for the script
        with the provided functions. 
    
        @param opt_handlers: a dictionary, translating an 
        option string to a function. Depending on whether the 
        function is parameterless or has one parameter the 
        option string will be just a letter or a letter ending 
        in a colon.
 
        @param def_handler: a function used to handle the 
        program when no parameters or arguments are present.
        This is a parameterless function.
    
        @param arg_handler: a function used to handle all 
        the arguments - it takes one parameter.
    """ 
    string = "".join(["%s" % (i) \
                            for i in opt_handlers.keys()])
    options, arguments = getopt.getopt(sys.argv[1:], string)

    # Handle options.
    for key, value in options:        
        if value != '':
            stop = opt_handlers[key[1:]+":"](value)
        else:
            stop = opt_handlers[key[1:]]()
        if stop:
            return
          
    # Handle arguments.     
    if len(arguments) > 0:
        arg_handler(arguments)
    
    # Handle when no arguments or params are present.
    elif len(options) == 0:
        def_handler()

# Execution starts here. Try to make out the arguments and
# run the appropriate function.
if __name__ == "__main__":
    # Join all the classes into one giant dictionary. This 
    # eliminates inconsistencies and makes manging functions
    # easy to grab in the code for individual characters.
    for character in ELONGATABLE:
        MANGLERS[character] = elongate
    for character in REMOVABLE:
        MANGLERS[character] = remove
    for character in SUBSTITUTABLE.keys():
        MANGLERS[character] = substitute

    # Define how to react to the various arguments.
    options = {
        "p" : handle_pipe,
        "i" : handle_interactive,
        "w:" : handle_word,
        "f:" : handle_file,
        "h" : print_usage
    }
    
    # Run the functions appropriate to the options.
    resolve_opts(options, options["p"], handle_params)
