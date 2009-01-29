#!/usr/bin/python
# 
# Copyright 2008 Konrad Siek 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os.path;
import getopt;
import sys;

sources = [];
empty = ["", "*", None];
startAt = 1;
output = sys.stdout;
sort = False;
ignore = False;
quiet = False;

def addSource (source):
    if os.path.exists(source):
        sources.append(source);
    elif not quiet:
         sys.stderr.write("Source: '" + source + 
                          "' does not exist. Skipping...\n");
         
def setLine (line):
    global startAt;
    try:
        number = int(line);
    except ValueError:
        if not quiet:
            sys.stderr.write("Line value: " + line + 
                             " is not a number. Ignoring...\n");
        return;
    if number <= 0:
        if not quiet:
            sys.stderr.write("Line value: " + line + 
                             " must be greater than 0. Ignoring...\n");
        return;
    startAt = number;
    return startAt;

def setOutput (path):
    """
    Sets the file, which will be used throughout the program to 
    write results. If this is not done, the module will write to
    sys.stdout instead.
        
    @param path: is the path to the file. 
    """
    global output;
    output = open(path, 'w');   
        
def setSort():
    global sort;
    sort = True;

def setQuiet():
    global quiet;
    quiet = True;
    
def setIgnore():
    global ignore;
    ignore = True;
        
def printUsage ():
    """
    Print usage information for the script.
    """
        
    sys.stdout.write("Usage:\n");
    sys.stdout.write("\t"+ sys.argv[0]
                    +" -s source [-s source ... ] "
                    +"[-l line ] target\n");
    sys.stdout.write("\t"+ sys.argv[0] +" -h\n");
    sys.stdout.write("\t-s source\t\t"
                    +"Select an output file to write to.\n");
    sys.stdout.write("\t-l line\t\t"
                    +"Select a line in the target to start from.\n");
    sys.stdout.write("\t-o path\t\t"
                    +"Output results to file, instead of stdout.\n");
    sys.stdout.write("\t-i \t\t\t"
                    +"Ignore if all sources have no values "
                    +"(or value of '*').\n");
    sys.stdout.write("\t-a \t\t\t"
                    +"Sort results.\n");
    sys.stdout.write("\t-q \t\t\t"
                    +"Quiet mode.\n");
    sys.stdout.write("\t-h \t\t\t"
                    +"Show this message.\n");
    sys.stdout.write("");
    sys.exit(0);
    
def fileToList(path):
    file = open(path, 'r');
    lines = file.readlines();
    file.close();        
    list = [];
    counter = 1;
    for line in lines:
        if (not line.startswith("#") and (len(line.strip())) > 0):
            line = line.rstrip("\n");
            key, separator, value = line.partition("=");            
            if value.find("=") >= 0:
                sys.stderr.write("Warning: value of line " 
                                 +str(counter) + " in " + path);
                sys.stderr.write(" contains an equals sign '=' (" 
                                 +line + ")\n");
            list.append((counter, key, value));
        counter += 1;              
    return list;
    
def loadSources():
    lists = {};
    for source in sources:
        lists[source] = fileToList(source);
    return lists;

def popByKey(target, list):
    for i in range(0, len(list)):
        line, key, value = list[i];
        if key == target:
            del list[i];
            return line, key, value;
    return None, None, None;

def dialog(property, sources):
    sys.stdout.write(property+"\n");
    for source, line, value in sources:
        sys.stdout.write("\t"+source+"\t("+str(line)+"): "
                         +str(value)+"\n");
    sys.stdout.write("$("+property+"):"); 
    
def save(results):
    if sort:
        results.sort();
        
    printout(results);
        
def control(property, value, results):
    line = sys.stdin.readline().strip();
    if line == "=stop":
        save(results);
        exit(0);
    elif line == "=skip":        
        pass
    elif line == "":        
        results.append((property, value));
        pass
    else:
        results.append((property, line));
        
def printout(list):
    global output;
    for key, value in list:
        output.write(key+"="+value+"\n");
        
def outOfScope(target, list):
    for i in range(0, len(list)):
        line, key, value = list[i];
        if key == target:
            return (line < startAt);
    return False;

def absent(occurances):
    for key, line, value in occurances:
        if empty.count(value.strip()) == 0:
            return False;
    return True;
        
def parse (target):
    sources = loadSources();
    workspace = fileToList(target);
    results = [];
    
    # Translate the lines, which were in the target    
    for line, key, value in workspace:
        if line < startAt:
            continue;
        occurances = [(target, line, value)];        
        for s in sources:
            list = sources[s];
            l, k, v = popByKey(key, list);
            occurances.append((s, l, v));
        if ignore and absent(occurances):
             continue;
        dialog(key, occurances);
        control(key, value, results);
        
    # Translate the lines, which were in the sources, but not the target
    for source in sources:
        for line, key, value in sources[source]:
            if not outOfScope(key, workspace):
                occurances = [(target, line, value)];        
                for s in sources:
                    if source != s:
                        list = sources[s];
                        l, k, v = popByKey(key, list);
                        occurances.append((s, l, v));
                dialog(key, occurances);
                control(key, results);
    
    save(results);

def resolveOptions (optionHandling, argumentHandler):
    """
    Handles all the options and parameters for the script with the 
    provided functions. 
    
    @param optionHandling: a dictionary, translating an option string 
    to a function.Depending on whether the function is parameterless 
    or has one parameter the option string will be just a letter or a 
    letter ending in a colon.
    
    @param argumentHandler: a function used to handle all the arguments  
    - it takes one parameter.
    """
    
    string = "".join(["%s" % (i) for i in optionHandling.keys()]);
    options, arguments = getopt.getopt(sys.argv[1:], string);
    
    # Handle options.
    for key, value in options :        
        if value != '':
            optionHandling[key[1:]+":"](value);
        else:
            optionHandling[key[1:]]();
          
    # Handle arguments.        
    if len(arguments) > 0 :
        for argument in arguments:
            argumentHandler(argument);

if __name__ == "__main__":
    options = {"s:": addSource, 
               "h": printUsage, 
               "l:": setLine, 
               "o:": setOutput,
               "a": setSort,
               "q": setQuiet,  
               "i": setIgnore}    
    
    resolveOptions(options, parse);
