#!/usr/bin/python
# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2010 Konrad Siek <konrad.siek@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

# TODO debug/print

import sys
import os
import gtk
import parallel
import gettext
import gobject
from threading import Thread
from gettext import gettext as _

gettext.textdomain('bigredbutton')

# Check if we are working in the source tree or from the installed 
# package and mangle the python path accordingly
if os.path.dirname(sys.argv[0]) != ".":
    if sys.argv[0][0] == "/":
        fullPath = os.path.dirname(sys.argv[0])
    else:
        fullPath = os.getcwd() + "/" + os.path.dirname(sys.argv[0])
else:
    fullPath = os.getcwd()
sys.path.insert(0, os.path.dirname(fullPath))

from bigredbutton.bigredbuttonconfig import getdatapath
from bigredbutton.nox import ButtonTimer
from bigredbutton.TimerDialog import ON, OFF, TOGGLE

class BigredbuttonWindow(gtk.Window):
    __gtype_name__ = "BigredbuttonWindow"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation a BigredbuttonWindow requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling BigredbuttonWindow.finish_initializing().

        Use the convenience function NewBigredbuttonWindow to create
        BigredbuttonWindow object.

        """
        pass

    def finish_initializing(self, builder, port, verbose=False, on=0xff, off=0):
        """finish_initalizing should be called after parsing the ui definition
        and creating a BigredbuttonWindow object with it in order to finish
        initializing the start of the new BigredbuttonWindow instance.

        """
        self._status = builder.get_object('status')
        self._context = self._status.get_context_id('bigredbutton')
        self._popup = builder.get_object('popup')
        self._timeron_button = builder.get_object('timeron')
        self._timeroff_button = builder.get_object('timeroff')
        self._thefrickinbutton = builder.get_object('bigbutton')
        
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)

        # All sorts of variables.
        self._verbose = verbose
        self._on = on
        self._off = off
        self._port = port

        # Reset signal.
        self._set_state(False)

    def quit(self, widget, data=None):
        """quit - signal handler for closing the BigredbuttonWindow"""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """on_destroy - called when the BigredbuttonWindow is close. """
        #clean up code for saving application state should be added here

        gtk.main_quit()
        
    def toggle(self, widget=None, data=None):
        print "Toggling button."
        self._set_state(not self._state)
        
    def on(self, widget=None, data=None):
        print "Making sure the button is on."
        if not self._state:
            #self._set_state(True)
            self._thefrickinbutton.clicked()
            
    def off(self, widget=None, data=None):
        print "Making sure the button is off."
        if self._state:
            #self._set_state(False)
            self._thefrickinbutton.clicked()

    def popup_menu(self, widget, event):
        # Left mouse button click.
        if event.button == 3: 
            # Right mouse button click.
            time = event.time
            self._popup.popup(None, None, None, event.button, time)
            
    def timer_on(self, widget, data=None):
        from bigredbutton import TimerDialog
        dialog = TimerDialog.NewTimerDialog()
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            delay, action = dialog.get_delay(), dialog.get_action()
            repeat = dialog.get_repeat()

            func =  self._thefrickinbutton.clicked if action == TOGGLE else \
                    self.on if action == ON else \
                    self.off if action == OFF else \
                    None
                    
#            print 'action: %s' % action
#            print 'func: %s' % func
#            print 'delay: %s' % delay
#            print 'repeat: %s' % repeat
            
            self._timer_thread = ButtonTimer(delay, repeat)
            self._timer_thread.add_final_action(self.timer_off)
            self._timer_thread.add_finish_action(func)
            #self._timer_thread.add_update_action() #TODO
            
            # Schedule thread.
            gobject.idle_add(self._timer_thread.start)
            
            self._timeron_button.set_visible(False)
            self._timeroff_button.set_visible(True)
            
        dialog.destroy()
        
    def timer_off(self, widget=None, data=None):
        print "Timer off"
        self._timeron_button.set_visible(True)
        self._timeroff_button.set_visible(False)
        self._timer_thread.stop() #TODO

    def _set_state(self, state):
        self._state = state
        descr, value = (_('on'), self._on) if state else (_('off'), self._off)
        
        self._port.setData(value)
        self._print_info(descr)

    def _print_info(self, description):
        if self._verbose:           
            sys.stdout.write(_('The device is %s.' + '\n') % description)        
        self._status.push(self._context, _('The device is %s.') % description)

    def open_about(self, widget, data=None):
        from bigredbutton import AboutBigredbuttonDialog
        about = AboutBigredbuttonDialog.NewAboutBigredbuttonDialog()
        response = about.run()
        about.destroy()

    def open_value(self, widget, data=None):
        from bigredbutton import ValueDialog
        dialog = ValueDialog.NewValueDialog(self._on, self._off)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self._on, self._off = dialog.get_value()
        dialog.destroy()

def NewBigredbuttonWindow(parallelport, verbose=False, on=0xff, off=0):
    """NewBigredbuttonWindow - returns a fully instantiated
    BigredbuttonWindow object. Use this function rather than
    creating a BigredbuttonWindow directly.
    """

    #look for the ui file that describes the ui
    basic_path = os.path.join(getdatapath(), 'ui')
    ui_filename = os.path.join(getdatapath(), 'ui', 'BigredbuttonWindow.ui')
    
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    #builder.add_from_file(about_filename)
    window = builder.get_object("bigredbutton_window")
    window.finish_initializing(builder, on=on, off=off, verbose=verbose, \
            port=parallelport)
    return window
