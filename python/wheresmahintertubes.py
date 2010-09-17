#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Where's Mah Intertubes?!
#
# A simple script that lets you know when your connection goes down or comes 
# back up with sounds. 
#
# Depends:
#   espeak                (if you don't want to use sound files)
#   pygame                (if you do)
#
# Options:
#   -h, --help            show this help message and exit
#   --speak               recite a message when connection goes on or off
#                         (default)
#   --off=AUDIO_OFF, --boo=AUDIO_OFF
#                         set a sound played when connection is lost
#   --on=AUDIO_ON, --yay=AUDIO_ON
#                         set a sound played when connection is back on
#   -t TIMEOUT, --timeout=TIMEOUT
#                         set timeout for checking if connection works (default:
#                         10s)
#   -d DELAY, --delay=DELAY
#                         set delay between connection checks (default: 30s)
#   -u URI, --uri=URI, --url=URI
#                         ping this URI to see if connection works (default:
#                         http://74.125.77.147)
#   -v, --verbose         display information about things done by the program
#
# Examples:
#   Let's say you want to check if you can connect and you're fine with the 
#   espeak dude to moan about it instead fo using a cool sound you can use one
#   of the following (let it run in the background):
#   
#   ./wheresmahintertubes.py &
#   ./wheresmahintertubes.py --speak &
#
#   If you want some proper fun sounds then all you need is point them out:
#
#   ./wheresmahintertubes.py --yay=file/for_on.ogg --boo=file/for_off.mp3 &
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

import time
import sys
import pygame

quiet = False
uri = "http://74.125.77.147"

def printerr(*args):
    if quiet:
        return
    from sys import argv, stderr
    from os.path import basename
    stderr.write("%s:" % basename(argv[0]))
    for arg in args:
        stderr.write(" %s" % arg)
    stderr.write("\n")

def printout(*args):
    if quiet:
        return
    from sys import argv, stdout
    from os.path import basename
    stdout.write("%s:" % basename(argv[0]))
    for arg in args:
        stdout.write(" %s" % arg)
    stdout.write("\n")

def can_has_connection(timeout):
    import urllib2    
    printout("Checking ping to", uri)
    try:
        urllib2.urlopen(uri, timeout=timeout) # Google
    except urllib2.URLError as error:
        return False
    return True

class Speaker:
    def __init__(self):
        self.library = {}

    def add_to_library(self, key, path):
        self.library[key] = path

    def play_from_library(self, key):
        if not key in self.library:
            return False
        self.play(self.library[key])
        return True

    def play(self, message):
        from os import system
        system('espeak %s' % message)

class PyGamePlayer:
    def __init__(self):
        pygame.init()
        self.library = {}

    def add_to_library(self, key, path):
        self.library[key] = path

    def play_from_library(self, key):
        if not key in self.library:
            return False
        self.play(self.library[key])
        return True

    def play(self, path):
        pygame.mixer.Sound(path).play()

class Checker:
    def __init__(self, delay, timeout):
        self.delay = delay
        self.timeout = timeout

    def run(self):
        connected = can_has_connection(self.timeout)
        printout('Initially the connection is', 'on' if connected else 'off')
        while True:
            time.sleep(self.delay)
            current = can_has_connection(self.timeout)
            if connected != current:
                connected = current
                self.react(connected)

    def react(self, connected):
        from threading import Thread
        printout('The connection just went', 'on' if connected else 'off')    
        def run():
            self.player.play_from_library(connected)
        thread = Thread()
        thread.run = run
        thread.start()

if __name__ == '__main__':
    from optparse import OptionParser
    from os.path import basename
    from sys import argv

    usage = '\n%s [OPTIONS] ' % basename(argv[0]) + \
        '--on=[SOUND FILE] --off=[SOUND FILE]\n' + \
        '\tplay a sound when network connection goes up or down' + \
        '\n%s [OPTIONS] ' % basename(argv[0]) + '--speak\n' + \
        '\trecite a message when network connection goes up or down (boring...)'

    description = 'Wait around and periodically check if the connection ' + \
        'went up or down, and if that happens play an appropriate sound to ' + \
        'indicate it to the user. Network connectivity is check by the ' + \
        'the simple method of connecting a specific host address, and ' + \
        'assuming that the entwork is down if it takes too much time for ' + \
        'that host to respond.'

    parser = OptionParser(usage=usage, description=description)

    parser.add_option('--speak', action='store_true', dest='speak', \
        help='recite a message when connection goes on or off (default)')
    parser.add_option('--off', '--boo', action='store', dest='audio_off', \
        help='set a sound played when connection is lost')
    parser.add_option('--on', '--yay', action='store', dest='audio_on', \
        help='set a sound played when connection is back on')
    parser.add_option('-t', '--timeout', action='store', dest='timeout', \
        help='set timeout for checking if connection works (default: 10s)', \
        default=10, type='int')
    parser.add_option('-d', '--delay', action='store', dest='delay', \
        help='set delay between connection checks (default: 30s)', \
        default=30, type='int')
    parser.add_option('-u', '--uri', '--url', action='store', dest='uri', \
        help='ping this URI to see if connection works (default: %s)' % uri, \
        default=uri)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', \
        help='display information about things done by the program')

    opts, args = parser.parse_args()

    quiet = not opts.verbose
    uri = opts.uri

    player = None

    if opts.speak or not opts.audio_on or not opts.audio_off:
        player = Speaker()
        player.add_to_library(True, "Connection just went up")
        player.add_to_library(False, "Connection just went down")
    else:
        player = PyGamePlayer()
        player.add_to_library(True, opts.audio_on)
        player.add_to_library(False, opts.audio_off)

    checker = Checker(delay=opts.delay, timeout=opts.timeout)
    checker.player = player

    try:
        checker.run()
    except (KeyboardInterrupt, SystemExit):        
        printout('Exiting...')
        running = False
