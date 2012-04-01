#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract symbols from a.out output of vasm.

Allows to get the value of various symbols in the `a.out` output of `vasm`.
This script has been created because vasm does not build a listing file as
most z80 assemblers allowing to see sources and binary together (and thus values of labels).


Usage:
vasm_symbols fname [label]

"""

# imports
import sys

# code
if __name__ == '__main__':
    if len(sys.argv) not in (2,3):
        sys.stderr.write('Error!\nUsage\t%s filename [symbol]\n' % sys.argv[0])
        exit(-1)


    fname = sys.argv[1]
    f = open(fname)

    symbols = {}
    for line in f.readlines():
        if -1 == line.find('symbol:'):
            continue

        # Extract parts from screen
        parts = line.split()
        # Get label
        if parts[3] == 'LAB':
            label = parts[2]
        else:
            label = parts[2]+parts[3]

        # Get value
        value = parts[-2]

        assert label not in symbols

        symbols[label] = value
        

    # TODO filter with regex (no need to type the whole label)
    if len(sys.argv) == 3:
        label = sys.argv[2]
        if label in symbols:
            print "%s\tequ %s" % (label, symbols[label][1:-1])
        else:
            sys.stderr.write('Label "%s" not present\n' % label)
    else:
        for label in sorted(symbols.keys()):
            print "%s\tequ %s" % (label, symbols[label][1:-1])
# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2013, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.com'
__status__ = 'Prototype'

