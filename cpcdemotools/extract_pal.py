#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract palette from a .PAL file
Krusty/Benediction 03/23/2011
"""

import sys

# Get the file
fname = sys.argv[1]
f = open(fname, "rb")

# Read the information
header = f.read(128) # skip header

mode = f.read(1)
animation = f.read(1)
delay = f.read(1)
palette = []
for i in range(17):
    palette.append(f.read(12))
excluded = f.read(16)
protected = f.read(16)
f.close()

# Display on screen
print '; %s' % fname
for i in range(12):
    print '; Palette position %d' % (i+1)
    for ink in palette:
        print '\tdb &%x' % ord(ink[i])
