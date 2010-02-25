# -*- coding: utf-8 -*-
### BEGIN LICENSE
# Copyright (C) 2010 Konrad Siek <konrad.siek@gmail.com>
#This program is free software: you can redistribute it and/or modify it 
#under the terms of the GNU General Public License version 3, as published 
#by the Free Software Foundation.
#
#This program is distributed in the hope that it will be useful, but 
#WITHOUT ANY WARRANTY; without even the implied warranties of 
#MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
#PURPOSE.  See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along 
#with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

# THIS IS Gcraziest CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch until you know what you're doing.
# you're warned :)

# where your project will head for your data (for instance, images and ui files)
# by default, this is ../data, relative your trunk layout
__gcraziest_data_directory__ = '../data/'

import os

class project_path_not_found(Exception):
    pass

def getdatapath():
    """Retrieve gcraziest data path

    This path is by default <gcraziest_lib_path>/../data/ in trunk
    and /usr/share/gcraziest in an installed version but this path
    is specified at installation time.
    """

    # get pathname absolute or relative
    if __gcraziest_data_directory__.startswith('/'):
        pathname = __gcraziest_data_directory__
    else:
        pathname = os.path.dirname(__file__) + '/' + __gcraziest_data_directory__

    abs_data_path = os.path.abspath(pathname)
    if os.path.exists(abs_data_path):
        return abs_data_path
    else:
        raise project_path_not_found

