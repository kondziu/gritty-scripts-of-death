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

import gettext
from gettext import gettext as _

gettext.textdomain('bigredbutton')

class ValueDialog(gtk.Dialog):
    __gtype_name__ = "ValueBigredbuttonDialog"

    def __init__(self, on_value=0xFF, off_value=0x00):
        self.on_value = on_value
        self.off_value = off_value

    def finish_initializing(self, builder):
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.builder.connect_signals(self)
          
        # Values.
        self._on_bits = []
        self._off_bits = []
        for i in range(0, 8):
            self._on_bits.append(builder.get_object('bit%s' % i))
        for i in range(8, 16):
            self._off_bits.append(builder.get_object('bit%s' % i))

        self.set_value(self.on_value, self.off_value)
        print "len", len(self._on_bits), len(self._off_bits)
           
    def set_value(self, value_on, value_off):
        for bit in self._on_bits:
            bit.set_active(value_on % 2)
            value_on /= 2
        for bit in self._off_bits:
            bit.set_active(value_off % 2)
            value_off /= 2

    def get_value(self):
        return self.on_value, self.off_value

    def recalculate(self, widget, data=None):
        value_on = 0
        for i in range(0, len(self._on_bits)):
            bit = self._on_bits[i]
            if bit.get_active():
                value_on += 2 ** (i) 
        value_off = 0
        for i in range(0, len(self._off_bits)):
            bit = self._off_bits[i]
            if bit.get_active():
                value_off += 2 ** (i)

        self.on_value, self.off_value = value_on, value_off 
                           
    def ok(self, widget, data=None):
        print _("Off value:"), self.off_value
        print _("On value:"), self.on_value
    
    def cancel(self, widget, data=None):
        pass
                
def NewValueDialog(on_value, off_value):
    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'ValueBigredbuttonDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    dialog = builder.get_object('value_bigredbutton_dialog')
    dialog.finish_initializing(builder)
    dialog.set_value(on_value, off_value)
    return dialog

if __name__ == "__main__":
    dialog = NewValueDialog()
    dialog.show()
    gtk.main()

