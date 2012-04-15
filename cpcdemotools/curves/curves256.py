#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Curve generator.

Build curves that fit in 256 bytes.
"""

# imports
import matplotlib.pyplot as plt
from numpy import pi,sin, cos
import sys

def scale_input(i):
    """Scale the input in order to move in range [0;255] and not [0;360]."""
    return i*pi*2/256.0

def get_value(a, exp):
    """Compute the value in the expression `expr` at indice `i`"""
    i = scale_input(a)
    return eval(exp)

def get_values(exp):
    """Compute all the values in the expression `expr` from 0 to 255"""
    values = [get_value(i, exp) for i in range(256)]
    return values

def validate_values(values):
    """Verify the validity of the values"""
    for value in values:
        assert value <= 255 , 'We cannot use numbers > 255'
        assert value >= -127, 'We cannot use numbers < -127'

def build_z80(exp, values):
    """Build the z80 source code of the sinus curve"""
    print '; %s' % exp
    for value in values:
        print '\tdb %d' % value
# code
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage\n\t%s function\n\nwith function a mathematical function with sin and cos with i as index.\nExemple: 30*sin(i)+30\n" % sys.argv[0])
        quit(-1)

    exp = sys.argv[1]
    values = get_values(exp)
    integers = [int(a) for a in values]

    plt.plot(values, label='real', linestyle=':')
    plt.plot(integers, label='integer', drawstyle='steps', linewidth=2)
    plt.xlim([0,256])
    plt.xlabel('Byte')
    plt.ylabel('Position')
    plt.legend()
    plt.show()

    validate_values(integers)
    build_z80(exp, integers)
# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2012, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.fr'
__status__ = 'Prototype'

