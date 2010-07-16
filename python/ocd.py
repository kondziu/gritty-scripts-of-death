#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Obsessive-compulsive daemon.
# 
# The obsessive-compulsive daemon for website checking. It checks the website
# religiously every three minutes so you don't have to! Never again do you have
# to toil in front of the monitor for week after that tricky exam just pressing 
# 'Refresh': employ our machine slaves to do it for you! No hassle*!
#
# The script is supposed to run in the background and download the webpage under
# scrutiny with a given frequency and compare it with the version it downloaded
# the first time. If a change is detected, the script runs a custom command.
#
# * Unless they organize a bloody revolution to overthrow their meaty
#   oppressors... and rightfully so.
#
# Depends:
#   µTidylib <apt:python-utidylib>
#
# Usage:
#   ocd [OPTIONS] URI
#
# Options:
#  -c COMMAND, --command=COMMAND
#                      Specify a command to run on change.
#  -f FORMAT, --format=FORMAT
#                      Specify how arguments are passed to the command.
#                      Available placeholders: %uri - the URI of the observed
#                      website, %old - original content, %new - changed
#                      content.
#  -x XPATH, --xpath=XPATH
#                      Provide a path to interesting elements in the observed
#                      document.
#  -s SECONDS, --sleep-time=SECONDS
#                      Set the time in seconds between checks (downloads).
#  --continue          Do not stop when change is detected. Instead run
#                      specified command and continue checking.
#  -u USER, --user=USER
#                      Specify a username for the website.
#  -P PASSWORD, --pass=PASSWORD, --password=PASSWORD
#                      Give a password for the website.
#  -p, --prompt        Prompt for login and password.
#  -v, --verbose       Print script progress information to stderr.
#  -h, --help          Show detailed usage information.
#
# Examples:
#   The simplest use-case: watch for changes in a webpage (as a whole) and check
#   it every minute. The ampersand will cause it to be run in the background in 
#   bash.
#
#   ./ocd.py http://www.example.com/ &
#
#   Debugging and such: same as above, but loudmouth mode.
#
#   ./ocd.py -v http://www.example.com/ &
#
#   Watch a page for changes in a specific table element, with a login and 
#   password, and checking it every 20 seconds.
#   
#   ./ocd.py -ps 20 -x "//td[@class='strong']/div/span" \
#          "https://usosweb.amu.edu.pl/kontroler.php?_action=actionx:dla_stud/studia/oceny/index()" &
#   
#   Run a specific command on change: here, speak that the URI changed.
#
#   ./ocd.py -c espeak -f "Changes found in resource: %uri" \
#           http://www.cs.put.poznan.pl/ksiek/SOP/resources/embrace_change.php &
#
#   Here's a hint: if you run something in the commandline in the background
#   using the ampersand you can then turn the terminal off by pressing CTRL + D.
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

# Internalization.
import gettext
from gettext import gettext as _
gettext.textdomain('ocd')

def _ssl_opener(uri, user, password):
    """ Prepare an open function to handle the specific URI with Basic 
    authentication with and user/password."""
    
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, uri, user, password)
    handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(handler)
    
    return opener.open

def download(uri, user=None, password=None):
    """ Dowloads the specified document and cleans it up."""
    
    import urllib2, tidy
    from StringIO import StringIO

    opener = urllib2.urlopen if None in [user, password] \
                             else _ssl_opener(uri, user, password)
    raw_resource = ''.join(opener(uri).readlines())
    tidy_doc = tidy.parseString(raw_resource, output_xhtml=1, add_xml_decl=1,
                                            indent=1, output_encoding='utf8')
    resource = StringIO()
    tidy_doc.write(resource)
    
    return resource.getvalue()

def downloadx(uri, xpath, user=None, password=None, getcontent=True):
    """ Downloads the specified xpath elements from the document.
    
    If getcontent is set to True, the element list will be converted to string
    before returning, otherwise a list of xmlNode objects is returned."""
        
    import libxml2
    
    resource = download(uri)
    document = libxml2.htmlParseDoc(resource, None)
    document.xpathNewContext()
    elements = document.xpathEval(xpath)
    
    if getcontent:
        return map(lambda e: e.get_content(), elements)
    else:
        return elements

def getcredentials(user=None):
    """ Prompt the user for whatever credentials are still missing.
    
    If the username is given then just a prompt for password is shown to the 
    user, nd otherwise, the user is asked for both the password and username."""
    
    from sys import stderr, stdin
    from getpass import getpass
    
    if user is None:
        stderr.write(_('Username: '))
        user = stdin.readline().strip()
    password = getpass(_('Password: '), stream=stderr)
    
    return user, password
    
def _print(string, verbose):
    """ A shorthand to print debugging information out if the verbose option is
    set to True. This pparticular implementation is a bit costly."""
    
    if verbose:
        from sys import stderr, argv
        from os.path import basename
        stderr.write("%s: %s\n" % (basename(argv[0]), string));
    
def run(uri, effect, user=None, password=None, verbose=False, xpath=None, 
        sleeptime=60, stopondifference=True, comparator=lambda x, y: x == y,
        prompt=False):
    """ The main part of the script: runs comparisons in a loop.
    
    Here, credentials are gathered, the original version of the observed 
    resource is downloaded, and the script sleeps for the specified time, 
    downloads and compares new versions of the resource and checks for changes.
    
    The URI specifies the address of the resource, or webpage, or whatever, that
    will be observed to find changes.
    
    The effect parameter is a function that will be run when a change is found.
    This should be a function that takes three arguments: URI, old content, and 
    new content. The old content and new content arguments may be of type List 
    (if xpath is used) or String (if it is not used).
    
    Sleep time may be specified in seconds, controlling the time the loop will 
    wait between downloading each new (potentially changed) version of the page.
    
    An XPath query can be given that specifies the elements that should be 
    compared with version changes instead of a whole page. (Information on 
    XPath: http://www.w3schools.com/XPath/.)
    
    If verbose is set, debugging messages are produced on stderr.
    
    If stopondifference is set, the script will stop running if a change is 
    found, otherwise, the changed version becomes the new original and checking
    is continued.
    
    If prompt is set, the user is asked for password and login if necessary; 
    otherwise the login and password are used as they are.
    
    A custom comparator may be specified. The comparator takes two arguments of 
    type list (if xpath is used) or string (if it isn't) and should return a
    boolean."""
    
    from time import sleep
    
    # Ask the user for password if necessary.        
    if prompt:
        getcredentials(user)
    
    # Prepare a shorthand function for downloading versions.
    def _retrieve():
        if xpath:
            return downloadx(uri, xpath, user, password)
        else:
            return download(uri, user, password)
    
    # Download the original version of the remote resource.
    _print(_("Downloading base version of resource %s.") % uri, verbose)
    comparison = _retrieve()
    
    print comparison
    
    if verbose and xpath:
        # Just print some stuff out to stderr.
        elements = ', '.join(map(lambda x: '"%s"' % x, comparison))
        _print(_("Elements at XPath %s: %s.") % (xpath, elements), verbose)
        
    while True:
        _print(_("Sleeping %s seconds.") % sleeptime, verbose)
        sleep(sleeptime)
        
        # Grab a more current version of the resource.
        _print(_("Downloading resource %s.") % uri, verbose)
        current = _retrieve()
        
        if verbose and xpath:
            # Just print some stuff out to stderr.
            elements = ', '.join(map(lambda x: '"%s"' % x, current))
            _print(_("Elements at XPath %s: %s.") % (xpath, elements), verbose)
            
        # Compare old and new version of the resource.
        if not comparator(comparison, current):
            # Run 
            _print(_("Resource changed!"), verbose)
            effect(uri, comparison, current)
            
            if stopondifference:
                break
            else:
                comparison = current
                continue
                
        _print(_("No changes."), verbose)
        
def create_handler_command(name, format):
    """ Create a function that wraps a command for use with the main loop."""
    
    from os import popen
    from sys import stdout
    
    def run_command(uri, old, new):
        formatted = format
        formatted = formatted.replace("%uri", str(uri))
        formatted = formatted.replace("%old", str(old))
        formatted = formatted.replace("%new", str(new))
        command = "%s %s" % (name, formatted)
        content = ''.join(popen(command).readlines())
        stdout.write(content)
        return content
        
    return run_command
    
if __name__ == '__main__':
    """ Parse commandline options and start checking for changes."""

    from optparse import OptionParser, OptionGroup
    from sys import argv, exit
    from os.path import basename
    
    # Prepare the parser.
    usage = '%s [OPTIONS] URI' % basename(argv[0])
    parser = OptionParser(usage=usage)
    
    # Options that control the process of checking the website.
    querying = OptionGroup(parser, 'Querying options')
    querying.add_option('-c', '--command',  metavar='COMMAND', dest='command',
        default='echo', help='Specify a command to run on change.')
    querying.add_option('-f', '--format',  metavar='FORMAT', dest='format',
         help='Specify how arguments are passed to the command. ' + 
        'Available placeholders: ' + '%uri - the URI of the observed website, '
        '%old - original content, ' + '%new - changed content.', default='%uri')
    querying.add_option('-x', '--xpath',  metavar='XPATH', dest='xpath', 
        help='Provide a path to interesting elements in the observed document.',
        default=None)
    querying.add_option('-s', '--sleep-time',  metavar='SECONDS', dest='sleep', 
        help='Set the time in seconds between checks (downloads).', default=60,
        type='float')
    querying.add_option('--continue', action='store_true',
        default=False, help='Do not stop when change is detected. Instead ' + 
            'run specified command and continue checking.', dest='notstop')    
    parser.add_option_group(querying)

    # SSL and authentication options.
    security = OptionGroup(parser, 'Security options')
    security.add_option('-u', '--user',  metavar='USER', dest="user", \
        default=None, help='Specify a username for the website.')
    security.add_option('-P', '--pass', '--password', metavar='PASSWORD', \
        dest="password", default=None, help='Give a password for the website.')
    security.add_option('-p', '--prompt', dest='prompt', action="store_true",
        default=False, help='Prompt for login and password.')
    parser.add_option_group(security)
    
    # Options that don't fit into other categories.
    other = OptionGroup(parser, "Other options")
    other.add_option('-v', '--verbose', dest='verbose', action="store_true",
        default=False, help='Print script progress information to stderr.')
    parser.add_option_group(other)
    
    opts, args = parser.parse_args()
    
    # Check arguments
    if len(args) < 1:
        _print(_("Nothing to check: quitting..."), opts.verbose)
        exit(0)      
          
    if len(args) > 1:
        arguments = ', '.join(args[1:])
        _print(_("Arguments %s are ignored.") % arguments, opts.verbose)
    
    # Let us begin to commence!
    try:
        run(
            args[0], create_handler_command(opts.command, opts.format),
            user=opts.user, password=opts.password, prompt=opts.prompt,
            verbose=opts.verbose, sleeptime=opts.sleep, 
            stopondifference=(not opts.notstop), xpath=opts.xpath
        )
    except (KeyboardInterrupt, SystemExit):
       _print(_("Closed by the user."), opts.verbose)
    
