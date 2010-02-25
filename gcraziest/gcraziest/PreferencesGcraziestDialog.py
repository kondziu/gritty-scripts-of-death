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

import sys
import os
import gtk
import gio
import dictclient

import gconf
import logging

from gcraziest import craziest
from gcraziest.gcraziestconfig import getdatapath

GCONF_GENERAL = '/apps/craziest/general'

def int_of_string(string, default = -1, if_empty = 0):
    try:
        return int(string)
    except:
        if not string.strip():
            return if_empty
        else:
            return default  

class PreferencesGcraziestDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesGcraziestDialog"
    __files = {}
    __dict_database = None
    
    def __init__(self):
        """__init__ - This function is typically not called directly.
        Creation of a PreferencesGcraziestDialog requires redeading the associated ui
        file and parsing the ui definition extrenally,
        and then calling PreferencesGcraziestDialog.finish_initializing().

        Use the convenience function NewPreferencesGcraziestDialog to create
        NewAboutGcraziestDialog objects.
        """

        pass

    def finish_initializing(self, builder):
        """finish_initalizing should be called after parsing the ui definition
        and creating a AboutGcraziestDialog object with it in order to finish
        initializing the start of the new AboutGcraziestDialog instance.
        """

        #get a reference to the builder and set up the signals
        self.builder = builder
        self.builder.connect_signals(self)
        
        #list store for DICT databases (stupid glade!)
        self.databases.set_model(gtk.ListStore(str))
        renderer = gtk.CellRendererText()
        self.databases.pack_start(renderer, True)
        self.databases.add_attribute(renderer, 'text', 0)
        self.databases.dictionary = {}
        
        #init gconf connector
        self.__gconf = gconf.client_get_default()
        self.__gconf.add_dir(GCONF_GENERAL, gconf.CLIENT_PRELOAD_NONE)   
             
        #pull all config from gconf and load it into the gui
        self.__load_preferences()

    def get_preferences(self):
        """get_preferences - returns a dictionary object that contain
        preferences for gcraziest.
        """
        preferences = {}
        
        preferences['min_length'] = self.minlength.get_value_as_int()
        preferences['max_length'] = self.maxlength.get_value_as_int()
        preferences['blank_symbol'] = self.blanksymbol.get_text()

        if self.aspelldictionary.get_active():
            command = self.dictionarycommand.get_text()
            preferences['dictionary'] = craziest.AspellDictionary(command)  
        elif self.filedictionary.get_active():
            path = self.__files['dictionary']
            preferences['dictionary'] = craziest.FileDictionary(path)

        if self.customalphabet.get_active():
            path = self.__files['alphabet']
#            print self.customalphabetfile, path
            preferences['scores'] = craziest.read_scores(path)
        else:
            preferences['scores'] = craziest.SCORES
            
        preferences['dict_host'] = self.dicthost.get_text()
        preferences['dict_database'] = self.__dict_database
        preferences['dict_port'] = int_of_string(self.dictport.get_text(), 0, 2628)
        preferences['show_definitions'] = self.showdefinitions.get_active()
        
        return preferences
        
    def __load_preferences(self):
        """load_preferences - load setings from gconf. """
        #helper function
        def load(symbol, default, function):
            path = os.path.join(GCONF_GENERAL, symbol)        
            if self.__gconf.get_without_default(path):
                return function(path)
            else:
                return default
        gconf = self.__gconf
                
        #load raw value
        min_length = load('min_length', 2, gconf.get_int)
        max_length = load('max_length', 7, gconf.get_int)
        blank_symbol = load('blank_symbol', '?', gconf.get_string)
        dict_type = load('dictionary_type', 'command', gconf.get_string)   
        dict_file = load('dictionary_file', '', gconf.get_string)
        command = load('dictionary_command', 'aspell --lang=en dump master', gconf.get_string)
        custom_alphabet = load('custom_alphabet', False, gconf.get_bool)
        alphabet_file = load('custom_alphabet_file', '', gconf.get_string)
        dict_server = load('dict_host', 'dict.org', gconf.get_string)
        dict_port = load('dict_port', 2628, gconf.get_int)
        show_defs = load('show_definitions', True, gconf.get_bool)
        # Default: The Collaborative International English Dictionary
        dict_db = load('dict_db', 'gcide', gconf.get_string)
    
        #load preferences directly from gconf
        self.minlength.set_value(min_length)
        self.maxlength.set_value(max_length)
        self.blanksymbol.set_text(blank_symbol)
        self.dictionarycommand.set_text(command)
        self.dicthost.set_text(dict_server)
        self.dictport.set_text(str(dict_port))
        self.showdefinitions.set_active(show_defs)
        
        #variables not in gui
        self.__dict_database = dict_db
        
        #debug
        logging.debug('read configuration from gconf:')
        logging.debug(('min_length', min_length))
        logging.debug(('max_length', max_length))
        logging.debug(('blank_symbol', blank_symbol))
        logging.debug(('dictionary_file', dict_file))
        logging.debug(('dictionary_command', command))
        logging.debug(('custom_alphabet', custom_alphabet))
        logging.debug(('custom_alphabet_file', alphabet_file))        
        logging.debug(('dictionary_type', dict_type))
        logging.debug(('dict_server', dict_server))
        logging.debug(('dict_port', dict_port))
        logging.debug(('dict_db', dict_db))
        logging.debug(('show_defs', show_defs))        
  
        #dictionary needs extra attention             
        if dict_type == 'file':
             self.aspelldictionary.set_active(False)
             self.filedictionary.set_active(True)
        elif dict_type == 'command':
             self.aspelldictionary.set_active(True)
             self.filedictionary.set_active(False)
        else:
            raise Exception('Unknown dictionary type: ' + dict_type)
        if os.path.isfile(dict_file):
            gio_file = gio.File(dict_file)
            self.dictionaryfile.set_file(gio_file)
            self.__files['dictionary'] = gio_file.get_path()
        else:
            self.__files['dictionary'] = ''
            

        #alphabet also needs special treatment
        self.customalphabet.set_active(custom_alphabet)
        if os.path.isfile(alphabet_file):
            gio_file = gio.File(alphabet_file)
            self.customalphabetfile.set_file(gio_file)
            self.__files['alphabet'] = gio_file.get_path()
        else:
            self.__files['alphabet'] = ''
            
        logging.debug('state of files: %s' % self.__files)
        
        #update the combo box, pretty much by brute force
        self.dict_server_set(self.dicthost)
        #self.dict_database_set(self.databases)
        
    def __save_preferences(self):
        logging.debug('state of files: %s' % self.__files)
    
        #retrieve from GUI
        min_length = self.minlength.get_value_as_int()
        max_length = self.maxlength.get_value_as_int()
        blank_symbol = self.blanksymbol.get_text()
        dictionary_file = self.__files['dictionary']
        dictionary_command = self.dictionarycommand.get_text()
        custom_alphabet = self.customalphabet.get_active()
        custom_alphabet_file = self.__files['alphabet']
        dictionary_type = None
        if self.filedictionary.get_active():
            dictionary_type = 'file'
        elif self.aspelldictionary.get_active():
            dictionary_type = 'command'
        dict_server = self.dicthost.get_text()
        dict_port = int_of_string(self.dictport.get_text(), 0, 2628)
        dict_db = self.__dict_database
        show_defs = self.showdefinitions.get_active()
            
        #debug
        logging.debug('saved configuration to gconf:')
        logging.debug(('min_length', min_length))
        logging.debug(('max_length', max_length))
        logging.debug(('blank_symbol', blank_symbol))
        logging.debug(('dictionary_file', dictionary_file))
        logging.debug(('dictionary_command', dictionary_command))
        logging.debug(('custom_alphabet', custom_alphabet))
        logging.debug(('custom_alphabet_file', custom_alphabet_file))        
        logging.debug(('dictionary_type', dictionary_type))
        logging.debug(('dict_server', dict_server))
        logging.debug(('dict_port', dict_port))
        logging.debug(('dict_db', dict_db))
        logging.debug(('show_defs', show_defs))   

        #save config
        from os.path import join
        gconf = self.__gconf

        gconf.set_int(join(GCONF_GENERAL, 'min_length'), min_length)
        gconf.set_int(join(GCONF_GENERAL, 'max_length'), max_length)
        gconf.set_string(join(GCONF_GENERAL, 'blank_symbol'), blank_symbol)
        gconf.set_string(join(GCONF_GENERAL, 'dictionary_file'), dictionary_file)
        gconf.set_string(join(GCONF_GENERAL, 'dictionary_command'), dictionary_command)
        gconf.set_bool(join(GCONF_GENERAL, 'custom_alphabet'), custom_alphabet)
        gconf.set_string(join(GCONF_GENERAL,'custom_alphabet_file'), custom_alphabet_file)
        gconf.set_string(join(GCONF_GENERAL, 'dictionary_type'), dictionary_type)
        gconf.set_string(join(GCONF_GENERAL, 'dict_host'), dict_server)
        gconf.set_int(join(GCONF_GENERAL, 'dict_port'), dict_port)
        gconf.set_string(join(GCONF_GENERAL, 'dict_db'), dict_db)
        gconf.set_bool(join(GCONF_GENERAL, 'show_definitions'), show_defs)


    def ok(self, widget, data=None):
        """ok - The user has elected to save the changes.
        Called before the dialog returns gtk.RESONSE_OK from run().
        """

        #make any updates to self.__preferences here
        self.__save_preferences()

    def cancel(self, widget, data=None):
        """cancel - The user has elected cancel changes.
        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """

        #restore any changes to self.__preferences here
        self.__load_preferences()
        
    def dictionary_file_set(self, widget, data=None):
        path = self.dictionaryfile.get_filename()
        self.__files['dictionary'] = path
        logging.debug("Dictionary file set to '%s'" % path)
        
    def alphabet_file_set(self, widget, data=None):
        path = self.customalphabetfile.get_filename()
        self.__files['alphabet'] = path
        logging.debug("Alphabet file set to '%s'" % path)
        
    def dict_server_set(self, widget, data=None):
        logging.debug('setting DICT server.')
        try:
            self.serverstatus.hide()
            host = self.dicthost.get_text() 
            port = int(self.dictport.get_text())
            connection = dictclient.Connection(host, port)
#            print connection
            self.databases.get_model().clear()
            self.databases.dictionary = {}
            descriptions = connection.getdbdescs()
            index, reversed_dict = 0, {}
            for key in descriptions:
#                print index, key, descriptions[key]
                self.databases.append_text(descriptions[key])
                self.databases.dictionary[index] = key
                reversed_dict[key] = index
                index += 1
            if descriptions:
                if self.__dict_database in reversed_dict:
#                    print 'setting form rev dict: %s' % reversed_dict[self.__dict_database]
                    self.databases.set_active(reversed_dict[self.__dict_database])
                else:
#                    print 'setting active 0'
                    self.databases.set_active(0)
                    self.__dict_database = self.databases.dictionary[0]
        except Exception as e:
            self.databases.set_active(-1)
            self.databases.get_model().clear()
            self.serverstatus.show()
            logging.error(e)
        

    def dict_database_set(self, widget, data=None):
        active = self.databases.get_active()
#        print active, self.databases.dictionary
        if active >=0 and active in self.databases.dictionary:
#            print active, self.databases.dictionary[active]
            self.__dict_database = self.databases.dictionary[active]

def NewPreferencesGcraziestDialog():
    """NewPreferencesGcraziestDialog - returns a fully instantiated
    PreferencesGcraziestDialog object. Use this function rather than
    creating a PreferencesGcraziestDialog instance directly.
    """

    #look for the ui file that describes the ui
    ui_filename = os.path.join(getdatapath(), 'ui', 'PreferencesGcraziestDialog.ui')
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = gtk.Builder()
    builder.add_from_file(ui_filename)
    
    #grab GUI elements
    dialog = builder.get_object("preferences_gcraziest_dialog")
    dialog.minlength = builder.get_object("minlength")
    dialog.maxlength = builder.get_object("maxlength")
    dialog.blanksymbol = builder.get_object("blanksymbol")
    dialog.aspelldictionary = builder.get_object("aspelldictionary")
    dialog.dictionarycommand = builder.get_object("dictionarycommand")
    dialog.filedictionary = builder.get_object("filedictionary")
    dialog.dictionaryfile = builder.get_object("dictionaryfile")
    dialog.aspellcommand = builder.get_object("aspellcommand")
    dialog.customalphabet = builder.get_object("customalphabet")
    dialog.customalphabetfile = builder.get_object("customalphabetfile")
    dialog.dicthost = builder.get_object("dicthost")
    dialog.dictport = builder.get_object("dictport")
    dialog.databases = builder.get_object("databases")
    dialog.showdefinitions = builder.get_object("showdefinitions")
    dialog.serverstatus = builder.get_object("serverstatus")
    
    dialog.finish_initializing(builder)
    return dialog

if __name__ == "__main__":
    dialog = NewPreferencesGcraziestDialog()
    dialog.show()
    gtk.main()

