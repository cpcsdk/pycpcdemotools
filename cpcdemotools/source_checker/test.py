#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Manually test the syntax checker
"""
import z80_syntax_checker

# imports

# code
if __name__ == '__main__':

    print 'Macro errors'
    f = 'z80/macro_wrong.asm'
    z80_syntax_checker.check_source_file(f)

    print 'Syntax errors'
    f = 'z80/syntax_wrong.asm'
    z80_syntax_checker.check_source_file(f)


# metadata
__author__ = 'Krusty/Benediction'
__copyright__ = 'Copyright 2012, Benediction'
__credits__ = ['Krusty/Benediction']
__licence__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Krusty/Benediction'
__email__ = 'krusty@cpcscene.com'
__status__ = 'Prototype'

