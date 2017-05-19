#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract symbols from a.out output of vasm.

Allows to get the value of various symbols in the lst output of `vasm`.
This script has been created because vasm does not build a listing file as
most z80 assemblers allowing to see sources and binary together (and thus values of labels).


Usage:
vasm_symbols fname [label]

"""

# imports
import sys
import re
import glob
import os

# code

def interactive_mode():
    """Launch the interactive mode.
    TODO find a way to use it
    """
    print 'Welcome to the interactive mode'
    print 'Type "?help" for list of commands'

    file_search = '*.lst'
    last_command = ''
    while True:
        command = raw_input('Command > ')

        if command.startswith('?'):
            if command == '?quit':
                break
            elif command.startswith('?os '):
                os.system(command[4:])
                continue
            elif command == '?file_search':
                print 'file_search = %s' % file_search
                print str(glob.glob(file_search))
                continue
            elif command.startswith('?set_file_search '):
                file_search = command[len('?set_file_search '):]
                continue

            elif command == '?help':
                print '?help\tDisplay help'
                print '?quit\tQuit the interpreter'
                print '?os <cmd>\tLaunch the command <cmd> from the os'
                print '?file_search\tDisplay the file search pattern'
                print '?set_file_search <pattern>\tChange the file search'
                print '<label>\tSearch the label in all the file search'
                continue
            elif command == '??':
                command = last_command

        for fname in glob.glob(file_search):
            treat_file(fname, command)

        last_command = command

def treat_file(fname, _filter=None):
    """Launch the research process for the required file.
    TODO move filter/display
    """ 
    f = open(fname)

    symbols = {}
    for line in f.readlines():

        if -1 != line.find(' LAB '):

            # Extract parts from line
            parts = line.split()


            # Get label
            label = parts[0]
            if parts[1] != 'LAB':
                label=label + '.' + parts[1]

            # Get value
            value = parts[parts.index('LAB')+1] 
            
            # Skip this one, it will be redifined later
            if value.startswith('sec='):
                continue
            if value.startswith('('):
                value = value[1:-1]
            value = int(value, 0)
        elif -1 != line.find("EXPR("):
            # Updated for vasm 1.8
            parts = line.split()
            if parts[-2] == 'INTERNAL' and parts[-1] == 'ABS': continue
            if parts[-2] == 'UNUSED' and parts[-1] == 'ABS': continue
            if parts[-1] == 'INTERNAL': continue


            expr_idx = 0
            while parts[expr_idx].find("EXPR(") ==-1:
                expr_idx += 1

            if expr_idx == 1:
                label = parts[0]
            else:
                label = ".".join(parts[:expr_idx]) 

            expr = parts[expr_idx]
            value = int(expr[len("EXPR("):expr.find("=")])
            label = label.strip()
        else:
            continue

        
        # Check duplicates
        if label in symbols:
            if symbols[label] != value:
                print 'LINE', parts
                print 'LABEL', label
                print 'VALUE', value
                print
                print "We have already met %s => %s "% (label, symbols[label])
                exit(-1)
            else:
                continue

        # Remove temporary labels
        if label[0] != '*' and label[-1] != '*':
            symbols[label] = value
        

    if _filter is not None: # Search according to a REGEX or a value
        try:
            search = re.compile(_filter)

            # Filter labels
            fname_printed = False

            for label in sorted(symbols.keys()):
                if re.search(search, label) or re.search(search, symbols[label]):
                    if not fname_printed:
                        print ';', fname
                        fname_printed = True
                    print "%s\tequ 0x%x" % (label, symbols[label])

        except:
            pass

    else: # Display all

        if symbols.keys():
            print ';', fname

        for label in sorted(symbols.keys()):
            print "%s\tequ 0x%x" % (label, symbols[label])



if __name__ == '__main__':
    if len(sys.argv) not in (1,2,3):
        sys.stderr.write('Error!\nUsage\t%s [filename [symbol]]\n' % sys.argv[0])
        exit(-1)


    if len(sys.argv) > 1:
        # We have selected at least one filename

        fname = sys.argv[1]
        if len(sys.argv) == 3:
            treat_file(fname, sys.argv[2])
        else:
            treat_file(fname)


    else:
        interactive_mode()

# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2013, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.com'
__status__ = 'Prototype'

