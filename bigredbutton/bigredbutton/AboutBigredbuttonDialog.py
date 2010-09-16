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

import sys
import os
import gtk

from bigredbutton.bigredbuttonconfig import getdatapath

class AboutBigredbuttonDialog(gtk.AboutDialog):
    __gtype_name__ = "AboutBigredbuttonDialog"

    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a AboutBigredbuttonDialog requires redeading the associated ui
        file and parsing the ui definition extrenally, 
        and then calling AboutBigredbuttonDialog.finish_initializing().
    
        Use the convenience function NewAboutBigredbuttonDialog to create 
        NewAboutBigredbuttonDialog objects.
    
        """
        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutBigredbuttonDialog object with it in order to finish
        initializing the start of the new AboutBigredbuttonDialog instance.
    
        """
        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)

        #code for other initialization actions should be added here

def NewAboutBigredbuttonDialog():
    """NewAboutBigredbuttonDialog - returns a fully instantiated
    AboutBigredbuttonDialog object. Use this function rather than
    creating a AboutBigredbuttonDialog instance directly.
    
    """

    #look for the ui file that describes the ui
    from os.path import join
    ui_filename = join(getdatapath(), 'ui', 'AboutBigredbuttonDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)    
    dialog = builder.get_object("about_dialog")
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewAboutBigredbuttonDialog()
    dialog.show()
    gtk.main()

