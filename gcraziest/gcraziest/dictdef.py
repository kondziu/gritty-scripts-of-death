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

import dictclient

def get_definitions(dict_host, dict_port, dict_db, words):
    definitions = {}
    database = None    
    connection = dictclient.Connection(dict_host, dict_port)
    if connection.getdbdescs():
        database = connection.getdbobj(dict_db)      
    for word in words:
        definition = database.define(word)
        if definition:
            definitions[word] = '\n\n'.join((d.getdefstr() for d in definition))
            print definitions[word]
    return definitions
    
def format(definition):
    return definition

