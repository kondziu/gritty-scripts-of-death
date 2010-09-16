#!/usr/bin/python
# -*- coding: utf-8 -*-

from threading import Thread

def console(parallelport, verbose=False, on=0xff, off=0):
    from sys import stdin, stderr
    try:
        while True:
            # Get and ppreprocess the line.
            line = stdin.readline()
            if not line:
                break
            line = line.strip().lower()
            if not len(line):
                continue

            try:
                # Parse the value.
                value = to_int(line, on, off)

                # Send ot port.
                if value <= 0xff and value >= 0:
                    parallelport.setData(value)        
                else:
                    stderr.write('Can only send values between 0 and 255.\n')

            except ValueError:
                stderr.write('Cannot translate "%s" into a number\n' % line)
                
    except KeyboardInterrupt:
        pass

def to_int(string, on=0xff, off=0):
    if string == 'on':
        return on
    elif string == 'off':
        return off
    elif string.startswith('0x'):
        return int(string, 16) 
    else:
        return int(string)

def sequence(parallelport, args, verbose=False, delay=500, on=0xff, off=0):
    from time import sleep
    from sys import stderr

    try:
        sequence = map(lambda arg: to_int(arg, on=on, off=off), args)
        length = len(sequence)    
        for i in range(0, length):
            parallelport.setData(sequence[i])
            if i < length - 1:
                sleep(delay/1000.)

    except ValueError:
        stderr.write('Cannot translate at least one of %s into a number\n' \
                % ', '.join(map(lambda s: '"%s"' % s, set(args))))

def translate_unit(string):
    if unit_s in ['s', 'second', 'seconds', 'sec'] or not unit_s:
        return 1.        
    elif unit_s in ['m', 'minute', 'minutes', 'min']:
        return 60.
    elif unit_s in ['h', 'hour', 'hours', 'hrs']:
        return 60. * 60.
    elif unit_s in ['milli', 'millis', 'millisecond', 'milliseconds']:
        return 1. / 1000.
    else:
        return None

def translate_delay(string):
    string = string.strip()
    i, length = 0, len(string)
    while i < length:
        if string[i].isdigit or string[i] in ['.', ',', ' ']: # TODO get decimal point from locale
            break
        i += 1 
    number_s, unit_s = string[:i],  string[i:].strip().lower()
    number, unit = float(number_s), translate_unit(unit_s)

    return number * unit

class ButtonTimer(Thread):
    def __init__(self, delay, repeat=False):
        Thread.__init__(self)
        self._actions = []
        self._updates = []
        self._finals = []
        self._repeat = repeat
        self._delay = delay
        self.running = False

    def add_finish_action(self, action):
        self._actions.append(action)
        
    def add_final_action(self, action):
        self._finals.append(action)
        
    def add_update_action(self, action):
        self._updates.append(action)
        
    def run(self):
        print "Running thread: delay=%s, repeat=%s" % (self._delay, self._repeat)
        import time
        self.running = True
        delay = self._delay
        while self.running:
            print "loop: %s" % time.localtime() 
            if not delay:
                print "end"
                for action in self._actions:
                    print "running action: %s" % action
                    action()
                if not self._repeat:
                    print 'not repeat'
                    break
                else:
                    print 'repeat'
                    delay = self._delay
                    print 'repeat with delay %s' % delay
            for action in self._updates:
                print "running action: %s" % action
                action(delay, self._repeat) #TODO
            sleep_time = 1. if delay >= 1. else delay 
            print 'sleep=%s, delay=%s/%s' % (sleep_time, delay, self._delay)
            time.sleep(sleep_time)
            delay -= sleep_time
            print 'got to the end of loop: %s' % self.running
        for action in self._finals:
            print "final action: %s" % action
            action() #TODO
        print 'end thread'

    def stop(self):
        print 'timer stop'
        self.running = False
