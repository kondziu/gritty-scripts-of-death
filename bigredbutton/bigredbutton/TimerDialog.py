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

# TODO play sound
# TODO save last chosen options

import sys
import os
import gtk
import time
from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record

from bigredbutton.bigredbuttonconfig import getdatapath

UNITS = {
    'hours': 60.*60.,
    'minutes': 60.,
    'seconds': 1.,
    'milliseconds': 1./1000.,
}

# CONSTANTS DEFINING ACTIONS
ON, OFF, TOGGLE = 'on', 'off', 'toggle'

class TimerDialog(gtk.Dialog):
    __gtype_name__ = "TimerBigredbuttonDialog"

    def __init__(self):
        pass

    def finish_initializing(self, builder):
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)
        
        self._delay = 0
        
        self._delay_entry = builder.get_object('delay')
        self._units = builder.get_object('units')
        self._status = builder.get_object('status')
        self._toggleradio = builder.get_object('buttontoggle')
        self._onradio = builder.get_object('buttonon')
        self._offradio = builder.get_object('buttonoff')
        self._stop = builder.get_object('stopaction')
        self._repeat = builder.get_object('repeataction')

        # Prep combo box.
        self._store=gtk.ListStore(str)
        for unit in UNITS:
            self._store.append([unit])
        self._units.set_model(self._store)
        self._units.set_active(1)
        rend = gtk.CellRendererText()
        self._units.pack_start(rend)
        self._units.add_attribute(rend, 'text', 0)

        self._remove_alpha(self._delay_entry)
        #self._remove_alpha(self._hours)
        #self._remove_alpha(self._minutes)
        #self._remove_alpha(self._seconds)

#        time.strftime("%S", time.localtime(time.time()))
                
    def ok(self, widget, data=None):
        #try:
#       print dir(self._units)
        #sprint self._units.get_child(self._units.get_active())
        print "model: %s" % self._units.get_model()
        print "active: %s" % self._units.get_active()
        print "len: %s" % len(self._units.get_model())
        print "unit: %s" % self._units.get_model()[self._units.get_active()][0]
        print "unit l: %s" % len(self._units.get_model()[self._units.get_active()])
        unit_s = self._units.get_model()[self._units.get_active()][0]
        unit = UNITS[unit_s]
        print "unit=%s: %s" % (unit_s, unit)
        delay = float(self._delay_entry.get_text())
        self._delay = delay * unit
        
        self._action = TOGGLE if self._toggleradio.get_active() else \
                       ON     if self._onradio.get_active() else \
                       OFF    if self._offradio.get_active() else \
                       None
                       
        self._repeat = self._repeat.get_active() # XXX what if neither or both?
                       
        print '%s * %s = %s' % (delay, unit, self._delay)
        #except:
        #    self._delay = None

    def cancel(self, widget, data=None):
        pass
        
    def get_delay(self):
        return self._delay
        
    def get_action(self):
        return self._action
        
    def get_repeat(self):
        return self._repeat

#   def delay_changed(self, widget, data=None):
#        print 'delay changed'
#        try:
#            delay = float(self._delay_entry.get_text())
#        except ValueError:
#            pass #TODO show error message on status bar

#    def units_changed(self, widget, data=None):
#        print 'units changed'

    def _remove_alpha(self, widget):
        def filter_numbers(entry, *args):
            text = entry.get_text().strip()
            entry.set_text(''.join([i for i in text if i in '0123456789,.'])) #TODO localize
        widget.connect('changed', filter_numbers)

def NewTimerDialog():
    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'TimerBigredbuttonDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    dialog = builder.get_object('timer_bigredbutton_dialog')
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewTimerDialog()
    dialog.show()
    gtk.main()

